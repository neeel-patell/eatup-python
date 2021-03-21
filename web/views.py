from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from recipe.models import *
from django.urls import reverse
from django.urls.resolvers import URLResolver
import os

def home(request):
    return render(request, "home.html")

''' Recipe Category functions start '''

def recipe_category(request):
    if request.method == "GET":
        categories = RecipeCategory.objects.order_by('name')
        return render(request, "recipe_category.html", {'categories':categories})
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

''' Recipe Category functions finish '''



''' Product Category functions start '''

def upload_product_image(f, id):  
    with open("media/images/product_category/"+str(id)+".jpg", 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def add_product_category(request):
    if request.method == "POST":
        name = request.POST['name']
        category = ProductCategory(name=name)
        category.save()
        # id = ProductCategory.objects.latest('id')
        # image = request.FILES['image']
        # upload_product_image(image, id.id)
        return redirect(reverse('view_product_category'))

def view_product_category(request):
    if request.method == "GET":
        categories = ProductCategory.objects.order_by('name')
        return render(request, "product_category.html", {'categories':categories})

def delete_product_category(request, id):
    if request.method == "GET":
        category = ProductCategory.objects.get(pk=id)
        category.delete()
        # os.remove("media/images/product_category/"+str(id)+".jpg")
        return redirect(reverse('view_product_category'))

def update_product_category(request, id):
    if request.method == "POST":
        type = request.POST['type']
        # if type == "image_change":
        #     image = request.FILES['image']
        #     if os.path.exists("media/images/product_category/"+str(id)+".jpg"):
        #         os.remove("media/images/product_category/"+str(id)+".jpg")
        #     upload_product_image(image, id)
        if type == "name_change":
            name = request.POST['name']
            ProductCategory.objects.filter(id=id).update(name=name)
        return redirect(reverse('view_product_category_single', kwargs={'id': id}))

def view_product_category_single(request, id):
    if request.method == "GET":
        category = ProductCategory.objects.get(pk=id)
        return render(request, "product_category_single.html", {'category':category})

''' Product Category functions finish '''


''' Product functions start '''

def view_product(request):
    if request.method == "GET":
        products = Product.objects.order_by('name')
        categories = ProductCategory.objects.order_by('name')
        return render(request, "product.html", {'products':products, 'categories':categories})

def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']

        category_obj = ProductCategory.objects.get(pk=category)
        product = Product(name=name, category=category_obj)
        product.save()
        product_obj = Product.objects.latest('id')
        add_price(product_obj, price)
        change_quantity(product_obj, quantity)
        return redirect(reverse('view_product'))

def add_price(product_obj, price):
    ProductPrice.objects.filter(product = product_obj).update(is_current=False)
    price_obj = ProductPrice(price=price, product=product_obj)
    price_obj.save()

def change_quantity(product_obj, quantity):
    ProductQuantity.objects.update_or_create(product=product_obj, defaults={'quantity': quantity})
    
def delete_product(request, id):
    if request.method == "GET":
        product = Product.objects.get(pk=id)
        ProductPrice.objects.filter(product=product).delete()
        ProductQuantity.objects.filter(product=product).delete()
        product.delete()
        return redirect(reverse('view_product'))


def update_product(request, id):
    if request.method == "POST":
        if request.POST['type'] == "details_change":
            name = request.POST['name']
            quantity = request.POST['quantity']
            price = request.POST['price']
            Product.objects.filter(id=id).update(name=name)
            product = Product.objects.get(pk=id)
            change_quantity(product, quantity)
            add_price(product, price)
            return redirect(reverse('view_product_single', kwargs={'id':id}))

def view_product_single(request, id):
    if request.method == "GET":
        product = Product.objects.get(pk=id)
        price = ProductPrice.objects.get(product=product, is_current=True)
        quantity = ProductQuantity.objects.get(product=product)
        return render(request, "product_single.html", {'product':product, 'price':price, 'quantity':quantity})

''' Product functions finish '''