from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, Order, Zone, Shop
from .forms import ProductForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users
# Create your views here.


@login_required(login_url='user-login')
def index(request):
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()

    zones = Zone.objects.values('name').distinct()
    shops = None
    selected_shop = None
    shop_orders = None
    form = OrderForm()

    # Handle GET request for filtering shops based on zone criteria
    if request.method == 'GET':
        zone_name = request.GET.get('zone_name')
        zone_district = request.GET.get('zone_district')
        zone_thana = request.GET.get('zone_thana')
        zone_area = request.GET.get('zone_area')

        if zone_name:
            # Filter shops based on zone criteria
            filtered_zones = Zone.objects.filter(
                name=zone_name,
                district=zone_district,
                thana=zone_thana,
                area=zone_area
            )
            shops = Shop.objects.filter(zone__in=filtered_zones)
            

        # Retrieve selected shop from session if available
        if 'selected_shop_id' in request.session:
            try:
                selected_shop = Shop.objects.get(id=request.session['selected_shop_id'])
                shop_orders = Order.objects.filter(shop=selected_shop, customer=request.user)
            except Shop.DoesNotExist:
                selected_shop = None
                shop_orders = None

    # Handle POST request for placing orders
    if request.method == 'POST':
        form = OrderForm(request.POST)
        selected_shop_id = request.POST.get('selected_shop')

        if selected_shop_id:
            try:
                selected_shop = Shop.objects.get(id=selected_shop_id)
                shop_orders = Order.objects.filter(shop=selected_shop, customer=request.user)
                request.session['selected_shop_id'] = selected_shop_id  # Store in session
                # print(selected_shop)  # Test output
                # print(shop_orders)    # Test output
            except Shop.DoesNotExist:
                selected_shop = None

        if form.is_valid() and selected_shop:
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.shop = selected_shop  
            obj.save()
            return redirect('dashboard-index')

    context = {
        'form': form,
        'order': order,
        'product': product,
        'product_count': product_count,
        'order_count': order_count,
        'customer_count': customer_count,
        'zones': zones,
        'shops': shops,
        'selected_shop': selected_shop,
        'shop_orders': shop_orders,
    }
    # print(selected_shop)  # Test output
    # print(shop_orders)    # Test output

    return render(request, 'dashboard/index.html', context)



from django.http import JsonResponse

def get_districts(request):
    zone_name = request.GET.get('zone_name')
    if zone_name:
        districts = Zone.objects.filter(name=zone_name).values_list('district', flat=True).distinct()
        return JsonResponse({'districts': list(districts)})
    return JsonResponse({'districts': []})

def get_thanas(request):
    district_name = request.GET.get('district_name')
    if district_name:
        thanas = Zone.objects.filter(district=district_name).values_list('thana', flat=True).distinct()
        return JsonResponse({'thanas': list(thanas)})
    return JsonResponse({'thanas': []})

def get_areas(request):
    thana_name = request.GET.get('thana_name')
    if thana_name:
        areas = Zone.objects.filter(thana=thana_name).values_list('area', flat=True).distinct()
        return JsonResponse({'areas': list(areas)})
    return JsonResponse({'areas': []})










@login_required(login_url='user-login')
def products(request):
    product = Product.objects.all()
    product_count = product.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    product_quantity = Product.objects.filter(name='')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-products')
    else:
        form = ProductForm()
    context = {
        'product': product,
        'form': form,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/products.html', context)


@login_required(login_url='user-login')
def product_detail(request, pk):
    context = {

    }
    return render(request, 'dashboard/products_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def customers(request):
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'customer': customer,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    } 
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def customer_detail(request, pk):
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    context = {
        'customers': customers,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,

    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def product_edit(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/products_edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-products')
    context = {
        'item': item
    }
    return render(request, 'dashboard/products_delete.html', context)


@login_required(login_url='user-login')
def order(request):
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/order.html', context)
