from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from recipe.models import *
from django.urls import reverse
import os

def home(request):
    return render(request, "home.html")

''' Recipe functions '''

def recipe_category(request):
    if request.method == "GET":
        categories = RecipeCategory.objects.order_by('name')
        return render(request, "recipe.html", {'categories':categories})
    elif request.method == "POST":
        name = request.POST['name']
        category = RecipeCategory(name=name)
        category.save()
        id = RecipeCategory.objects.latest('id')
        image = request.FILES['image']
        upload_recipe_image(image, id.id)
        return redirect(reverse('recipe_category'))

def upload_recipe_image(f, id):  
    with open("media/images/recipe_category/"+str(id)+".jpg", 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def recipe_category_single(request, id):
    if request.method == "GET":
        if 'action' in request.GET:
            if request.GET['action'] == "delete":
                category = RecipeCategory.objects.get(pk=id)
                category.delete()
                os.remove("media/images/recipe_category/"+str(id)+".jpg")
                return redirect(reverse('recipe_category'))
        else:
            category = RecipeCategory.objects.get(pk=id)
            return render(request, "recipe_category_single.html", {'category':category})

    elif request.method == "POST":
        type = request.POST['type']
        if type == "image_change":
            image = request.FILES['image']
            if os.path.exists("media/images/recipe_category/"+str(id)+".jpg"):
                os.remove("media/images/recipe_category/"+str(id)+".jpg")
            upload_recipe_image(image, id)
        elif type == "name_change":
            name = request.POST['name']
            RecipeCategory.objects.filter(id=id).update(name=name)
        return redirect(reverse('recipe_category_single', kwargs={'id': id}))

