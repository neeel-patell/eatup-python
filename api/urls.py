from django.urls import path
from .views import *

urlpatterns = [
    path('user/register', register_user, name="register_user"),
    path('user/login/email', login_user_via_email, name="login_user_via_email"),
    path('user/login/mobile', login_user_via_mobile, name="login_user_via_mobile"),

    path('recipe/category/all', get_all_recipe_category, name='get_all_recipe_category'),
]
