from django.urls import path
from .views import *

urlpatterns = [
    path('user/register', register_user, name="register_user"),
    path('user/login', login_user, name="login_user"),

    path('recipe/category/all', get_all_recipe_category, name='get_all_recipe_category'),
]
