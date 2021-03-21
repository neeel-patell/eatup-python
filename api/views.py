from django.shortcuts import render
from recipe.models import *
from django.http import HttpResponse

def get_recipe_category(request):
    if request.method == "GET":
        category = RecipeCategory.objects.all()
        return HttpResponse("")