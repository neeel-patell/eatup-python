from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("recipe/category/", recipe_category, name="recipe_category"),
    path("recipe/category/<int:id>/", recipe_category_single, name="recipe_category_single"),
]
