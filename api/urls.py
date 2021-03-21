from django.urls import path
from .views import *


urlpatterns = [
    path("recipe_category/",get_recipe_category)
]
