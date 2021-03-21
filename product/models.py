from django.db.models import *

class ProductCategory(Model):
    name = CharField(max_length=25, unique=True, null=False)
    
    class Meta:
        db_table = "product_category"

    def __str__(self):
        return self.name

class Product(Model):
    name = CharField(max_length=25, null=False)
    category = ForeignKey(ProductCategory,  on_delete=DO_NOTHING)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name

class ProductQuantity(Model):
    product = OneToOneField(Product, on_delete=CASCADE)
    quantity = DecimalField(max_digits=4, decimal_places=0, null=False, default=0)
    
    class Meta:
        db_table = "product_quantity"

    def __str__(self):
        return self.product.name

class ProductPrice(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    price = DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    is_current = BooleanField(default=True)
    updated_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "product_price"

    def __str__(self):
        return self.product.name

class ProductDescription(Model):
    product = OneToOneField(Product, on_delete=CASCADE)
    description = TextField()

    class Meta:
        db_table = "product_description"

    def __str__(self):
        return self.product.name