from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("recipe/category/", recipe_category, name="recipe_category"),
    path("recipe/category/<int:id>/", recipe_category_single, name="recipe_category_single"),

    path("product/category/", view_product_category, name="view_product_category"),
    path("product/category/add", add_product_category, name="add_product_category"),
    path("product/category/<int:id>/delete", delete_product_category, name="delete_product_category"),
    path("product/category/<int:id>/update", update_product_category, name="update_product_category"),
    path("product/category/<int:id>", view_product_category_single, name="view_product_category_single"),

    path("product/<int:category_id>", view_product, name="view_product"),
    path("product/<int:category_id>/add", add_product, name="add_product"),
    path("product/<int:id>/delete", delete_product, name="delete_product"),
    path("product/<int:id>/update", update_product, name="update_product"),
    path("product/<int:id>/view", view_product_single, name="view_product_single"),

    path("recipe/<int:category_id>", view_recipe, name="view_recipe"),
    path("recipe/<int:category_id>/add", add_recipe, name="add_recipe"),
    path("recipe/<int:id>/delete", delete_recipe, name="delete_recipe"),
    path("recipe/<int:id>/update", update_recipe, name="update_recipe"),
    path("recipe/<int:id>/view", view_recipe_single, name="view_recipe_single"),
    path("recipe/<int:recipe_id>/add_description", add_recipe_description, name="add_recipe_description"),
    path("recipe/<int:recipe_id>/add_precaution", add_recipe_precaution, name="add_recipe_precaution"),
    path("recipe/<int:recipe_id>/add_recipe_step", add_recipe_step, name="add_recipe_step"),
    path("recipe/<int:recipe_step_id>/remove_recipe_step", remove_recipe_step, name="remove_recipe_step"),
    path("recipe/<int:recipe_id>/add_recipe_ingredient", add_recipe_ingredient, name="add_recipe_ingredient"),
    path("recipe/<int:ingredient_id>/remove_recipe_ingredient", remove_recipe_ingredient, name="remove_recipe_ingredient"),

    path("recipe/product", view_recipe_product, name="view_recipe_product"),
    path("recipe/product/add", add_recipe_product, name="add_recipe_product"),
    path("recipe/product/<int:id>/delete", delete_recipe_product, name="delete_recipe_product"),
]
