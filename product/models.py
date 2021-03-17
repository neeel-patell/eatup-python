from django.db.models import *

# Create your models here.
class ProductCategoryImage(Model):
    image = ImageField(upload_to="images/product_category/")

    class Meta:
        db_table = "product_category_image"

    def __str__(self):
        return self.id

class ProductCategory(Model):
    name = CharField(max_length=25, unique=True, null=False)
    image = ForeignKey(ProductCategoryImage, on_delete=CASCADE)

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

class ProductImage(Model):

    product = ForeignKey(Product, on_delete=CASCADE)
    is_main = BooleanField(default=False)
    image = ImageField(upload_to="images/product")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_image"

    def __str__(self):
        return self.product.name