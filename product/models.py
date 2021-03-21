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