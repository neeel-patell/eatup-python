import decimal
from typing import Text
from user.models import Home, User
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
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "recipe"

    def __str__(self):
        return self.name

class RecipeDescription(Model):
    recipe = OneToOneField(Recipe, on_delete=CASCADE)
    description = TextField(null=False)
    
    class Meta:
        db_table = "recipe_description"

    def __str__(self):
        return self.recipe.name

class RecipeSteps(Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    index = DecimalField(null=False, max_digits=2, decimal_places=0)
    description = TextField(null=False)
    min_wait = DecimalField(null=False, default=0, max_digits=4, decimal_places=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_steps"
    
    def __str__(self):
        return self.recipe.name

class RecipePrecaution(Model):
    recipe = OneToOneField(Recipe, on_delete=CASCADE)
    message = CharField(null=False, max_length=100)
    time_before = DurationField(null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_precaution"
    
    def __str__(self):
        return self.recipe.name

class RecipeProductName(Model):
    name = CharField(max_length=25, null=False, unique=True)

    class Meta:
        db_table = "recipe_product_name"
    
    def __str__(self):
        return self.name

class RecipeIngredient(Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    recipe_product_name = ForeignKey(RecipeProductName, on_delete=RESTRICT)
    quantity = DecimalField(default=1, max_digits=2, decimal_places=0)
    weight = DecimalField(default=0, max_digits=6, decimal_places=3)
    litre = DecimalField(default=0, max_digits=6, decimal_places=3)
    spoon = DecimalField(default=0, max_digits=5, decimal_places=3)
    cup = DecimalField(default=0, max_digits=5, decimal_places=2)

    class Meta:
        db_table = "recipe_ingredient"
    
    def __str__(self):
        return self.recipe.name
        
class RecipeSchedule(Model):
    recipe = ForeignKey(Recipe, on_delete=RESTRICT)
    home = ForeignKey(Home, on_delete=CASCADE)
    date = DateField(null=False)
    meal = DecimalField(null=False, max_digits=1, decimal_places=0)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_schedule"

    def __str__(self):
        return "{} - {}".format(self.user.name, self.recipe.name)

class RecipeRating(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    rating = DecimalField(max_digits=1, decimal_places=0)
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    feedback = CharField(max_length=150)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipe_rating"

    def __str__(self):
        return "{} - {}".format(self.user.name, self.recipe.name)