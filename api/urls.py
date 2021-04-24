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

    path('expense/add/amount/<int:schedule_id>', add_amount_to_expense, name='add_amount_to_expense'),
    path('expense/get/<int:user_id>', get_expense, name='get_expense'),

    path('home/create', create_home, name='create_home'),
    path('home/get/<int:user_id>', get_user_home, name='get_user_home'),
    path('home/create', create_home, name='create_home'),
    path('home/join', join_home, name='join_home'),
    path('home/user/add', add_user_to_home, name='add_user_to_home'),
    path('home/user/remove/<int:user_id>', remove_user_from_home, name='remove_user_from_home'),
    path('home/user/role/check/<int:user_id>', check_user_role, name='check_user_role'),
    path('home/exit/<int:user_id>', exit_home, name='exit_home'),
]
