from django.db.models import *
from product.models import *

class RecipeCategory(Model):

    name = CharField(max_length=25, unique=True, null=False)
    
    class Meta:
        db_table = "recipe_category"

    def __str__(self):
        return self.name

class Recipe(Model):
    name = CharField(max_length=30, null=False)
    category = ForeignKey(RecipeCategory, on_delete=DO_NOTHING)
    duration = DurationField(null=False)
    description = TextField(null=False)
    rating = DecimalField(null=False, default=0, max_digits=1, decimal_places=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "recipe"

    def __str__(self):
        return self.name

class RecipeSteps(Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    index = DecimalField(null=False, max_digits=2, decimal_places=0)
    min_wait = DecimalField(null=False, default=0, max_digits=2, decimal_places=0)
    sec_wait = DecimalField(null=False, default=0, max_digits=2, decimal_places=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_steps"
    
    def __str__(self):
        return self.recipe.name

class RecipePrecaution(Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=DO_NOTHING)
    message = CharField(null=False, max_length=100)
    time_before = DurationField(null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_precaution"
    
    def __str__(self):
        return self.recipe.name