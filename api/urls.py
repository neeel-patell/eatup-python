from django.urls import path
from .views import *

urlpatterns = [
    path('user/register', register_user, name="register_user"),
    path('user/login/email', login_user_via_email, name="login_user_via_email"),
    path('user/login/email/nomail', login_user_via_email_without_mail, name="login_user_via_email_without_mail"),
    path('user/login/mobile', login_user_via_mobile, name="login_user_via_mobile"),
    path('user/password/forgot/<int:mobile>', forgot_password_mobile, name="forgot_password_mobile"),
    path('user/password/forgot/<str:email>', forgot_password_email, name="forgot_password_email"),
    
    path('recipe/category/all', get_all_recipe_category, name='get_all_recipe_category'),
    path('recipe/<int:category>', get_recipe_by_category, name='get_recipe_by_category'),
    path('recipe/view/<int:recipe_id>/<int:user_id>', get_single_recipe, name='get_single_recipe'),
    path('recipe/schedule', schedule_recipe, name='schedule_recipe'),
    path('recipe/schedule/get/<int:user_id>', get_recipe_schedule, name='get_recipe_schedule'),
    path('recipe/schedule/remove/<int:schedule_id>', remove_recipe_schedule, name='remove_recipe_schedule'),
    path('recipe/rating/add/<int:recipe_id>/<int:user_id>', add_recipe_rating, name='add_recipe_rating'),

    path('expense/splitter/get/<int:user_id>', get_expense_splitter, name='get_expense_splitter'),

    path('home/create', create_home, name='create_home'),
    path('home/get/<int:user_id>', get_user_home, name='get_user_home'),
    path('home/create', create_home, name='create_home'),
    path('home/join', join_home, name='join_home'),
]
