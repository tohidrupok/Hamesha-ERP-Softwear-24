from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
)

class Zone(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"Zone: {self.name}, District: {self.district}, Thana: {self.thana}, Area: {self.area}"

class Shop(models.Model):
    shop_name = models.CharField(max_length=200, verbose_name="Shop Name")
    shop_owner = models.CharField(max_length=200, verbose_name="Shop Owner")
    shop_phone = models.CharField(max_length=15, verbose_name="Shop Phone")
    shop_nid = models.CharField(max_length=20, verbose_name="Shop NID")
    shop_email = models.EmailField(max_length=254, verbose_name="Shop Email")
    shop_address = models.TextField(verbose_name="Shop Address")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="Shop Zone")

    def __str__(self):
        return self.shop_name 
    


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name="Department/Company Name")

    def __str__(self):
        return self.name

class Product(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Dept/Company")
    
    name = models.CharField(max_length=200, verbose_name="Product Name")
    product_code = models.CharField(max_length=100, verbose_name="Product Code")
    product_dp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product DP")  
    product_tp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product TP")  
    product_mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product MRP")  
    product_sku = models.CharField(max_length=100, verbose_name="Product SKU")  
    product_factor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Factor")
    product_details = models.TextField(verbose_name="Product Details", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.product_code}"


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Shop" )

    def __str__(self):
        return f'{self.customer}-{self.name}'


