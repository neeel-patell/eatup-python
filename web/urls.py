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
    path("product/", view_product, name="view_product"),
    path("product/add", add_product, name="add_product"),
    path("product/<int:id>/delete", delete_product, name="delete_product"),
    path("product/<int:id>/update", update_product, name="update_product"),
    path("product/<int:id>", view_product_single, name="view_product_single"),
]
