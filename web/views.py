from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from recipe.models import *
from django.urls import reverse
import os
import datetime
from django.db.models import F

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
        upload_recipe_category_image(image, id.id)
        return redirect(reverse('recipe_category'))

def upload_recipe_category_image(f, id):  
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
            upload_recipe_category_image(image, id)
        elif type == "name_change":
            name = request.POST['name']
            RecipeCategory.objects.filter(id=id).update(name=name)
        return redirect(reverse('recipe_category_single', kwargs={'id': id}))

''' Recipe Category functions finish '''



''' Product Category functions start '''

def upload_product_category_image(f, id):  
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
        # upload_product_category_image(image, id.id)
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
        #     upload_product_category_image(image, id)
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

def view_product(request, category_id):
    if request.method == "GET":
        category = ProductCategory.objects.get(pk=category_id)
        products = Product.objects.filter(category=category).order_by('name')
        return render(request, "product.html", {'products':products, 'category':category})

def add_product(request, category_id):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']

        category_obj = ProductCategory.objects.get(pk=category_id)
        product = Product(name=name, category=category_obj)
        product.save()
        product_obj = Product.objects.latest('id')
        add_price(product_obj, price)
        change_quantity(product_obj, quantity)
        return redirect(reverse('view_product', kwargs={'category_id':category_id}))

def add_price(product_obj, price):
    ProductPrice.objects.filter(product = product_obj).update(is_current=False)
    price_obj = ProductPrice(price=price, product=product_obj)
    price_obj.save()

def change_quantity(product_obj, quantity):
    ProductQuantity.objects.update_or_create(product=product_obj, defaults={'quantity': quantity})
    
def delete_product(request, id):
    if request.method == "GET":
        product = Product.objects.get(pk=id)
        category_id = product.category_id
        ProductPrice.objects.filter(product=product).delete()
        ProductQuantity.objects.filter(product=product).delete()
        product.delete()
        return redirect(reverse('view_product', kwargs={'category_id':category_id}))


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

''' Recipe function starts '''

def upload_recipe_image(f, id):  
    with open("media/images/recipe/"+str(id)+".jpg", 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def view_recipe(request, category_id):
    if request.method == "GET":
        category = RecipeCategory.objects.get(pk=category_id)
        recipies = Recipe.objects.filter(category=category).order_by('name')
        return render(request, "recipe.html", {'recipies':recipies, 'category':category})

def add_recipe(request, category_id):
    if request.method == "POST":
        name = request.POST['name']
        minute = int(request.POST['minute'])
        second = int(request.POST['second'])
        duration = datetime.timedelta(minutes=minute, seconds=second)
        category = RecipeCategory.objects.get(pk=category_id)
        recipe = Recipe(category=category, duration=duration, name=name)
        recipe.save()
        id = Recipe.objects.latest('id')
        image = request.FILES['image']
        upload_recipe_image(image, id.id)
        return redirect(reverse('view_recipe', kwargs={'category_id':category_id}))
        
def update_recipe(request, id):
    if request.method == "POST":
        if request.POST['type'] == "description_change":
            description = request.POST['description']
            RecipeDescription.objects.filter(recipe_id=id).update(description=description)
        elif request.POST['type'] == "message_change":
            message = request.POST['message']
            hour = int(request.POST['hour'])
            minute = int(request.POST['minute'])
            duration = datetime.timedelta(hours=hour, minutes=minute)
            RecipePrecaution.objects.filter(recipe_id=id).update(message=message, time_before=duration)
        elif request.POST['type'] == "image_change":
            image = request.FILES['image']
            if os.path.exists("media/images/recipe/"+str(id)+".jpg"):
                os.remove("media/images/recipe/"+str(id)+".jpg")
            upload_recipe_image(image, id)
        return redirect(reverse('view_recipe_single', kwargs={'id':id}))

def delete_recipe(request, id):
    pass

def view_recipe_single(request, id):
    if request.method == "GET":
        recipe = Recipe.objects.get(pk=id)
        minutes = recipe.duration.seconds // 60
        seconds = recipe.duration.seconds % 60
        if RecipeDescription.objects.filter(recipe=recipe).exists() :
            recipe_description = RecipeDescription.objects.get(recipe=recipe)
        else:
            recipe_description = None
        if RecipePrecaution.objects.filter(recipe=recipe).exists() :
            recipe_precaution = RecipePrecaution.objects.get(recipe=recipe)
            precaution_hour = recipe_precaution.time_before.seconds // 3600
            precaution_minute = recipe_precaution.time_before.seconds // 60 % 60
        else:
            recipe_precaution = None
            precaution_hour = 0
            precaution_minute = 0
        if RecipeSteps.objects.filter(recipe=recipe).exists() :
            recipe_steps = RecipeSteps.objects.filter(recipe=recipe).order_by('index')
        else:
            recipe_steps = None
        recipe_ingredients = RecipeIngredient.objects.filter(recipe_id=id)
        recipe_dummy_products = RecipeProductName.objects.all()
        return render(request, "recipe_single.html", {
            'recipe':recipe,
            'minutes':minutes,
            'seconds':seconds,
            'recipe_description':recipe_description,
            'recipe_precaution':recipe_precaution,
            'recipe_steps':recipe_steps,
            'precaution_hour':precaution_hour,
            'precaution_minute':precaution_minute,
            'recipe_ingredients':recipe_ingredients,
            'recipe_dummy_products':recipe_dummy_products,
            })

def add_recipe_description(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=recipe_id)
        description = request.POST['description']
        recipe_description = RecipeDescription(recipe=recipe, description=description)
        recipe_description.save()
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))

def add_recipe_precaution(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=recipe_id)
        hour = int(request.POST['hour'])
        minute = int(request.POST['minute'])
        time_before = datetime.timedelta(hours=hour, minutes=minute)
        message = request.POST['message']
        recipe_precaution = RecipePrecaution(recipe=recipe, message=message, time_before=time_before)
        recipe_precaution.save()
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))

def add_recipe_step(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=recipe_id)
        index = request.POST['index']
        recipe_step_index_currector(recipe_id, index)
        description = request.POST['description']
        min_wait = int(request.POST['min_wait'])
        recipe_steps = RecipeSteps(recipe=recipe, index=index, min_wait=min_wait, description=description)
        recipe_steps.save()
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))

def remove_recipe_step(request, recipe_step_id):
    if request.method == "GET":
        recipe_step = RecipeSteps.objects.get(pk=recipe_step_id)
        step_index = recipe_step.index
        recipe_id = recipe_step.recipe_id
        recipe_step.delete()
        RecipeSteps.objects.filter(recipe_id=recipe_id, index__gt=step_index).update(index=F('index')-1)
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))

def recipe_step_index_currector(recipe_id, index):
    if RecipeSteps.objects.filter(index=index, recipe_id=recipe_id).exists():
        RecipeSteps.objects.filter(recipe_id=recipe_id, index__gte=index).update(index=F('index')+1)   

def add_recipe_ingredient(request, recipe_id):
    if request.method == "POST":
        product = RecipeProductName.objects.get(pk=request.POST['product'])
        weight = request.POST['weight']
        litre = request.POST['litre']
        spoon = request.POST['spoon']
        cup = request.POST['cup']
        quantity = request.POST['quantity']
        recipe_ingredient = RecipeIngredient(recipe_id=recipe_id, recipe_product_name=product, weight=weight, litre=litre, spoon=spoon, cup=cup, quantity=quantity)
        recipe_ingredient.save()
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))

def remove_recipe_ingredient(request, ingredient_id):
    if request.method == "GET":
        recipe_ingredient = RecipeIngredient.objects.get(pk=ingredient_id)
        recipe_id = recipe_ingredient.recipe_id
        recipe_ingredient.delete()
        return redirect(reverse('view_recipe_single', kwargs={'id':recipe_id}))


''' Recipe function finish '''


''' Recipe Product name function finish '''

def view_recipe_product(request):
    if request.method == "GET":
        products = RecipeProductName.objects.all()
        return render(request, 'recipe_product.html', {'products':products})

def add_recipe_product(request):
    if request.method == "POST":
        name = request.POST['name']
        product_name = RecipeProductName(name=name)
        product_name.save()
        return redirect(reverse('view_recipe_product'))

def delete_recipe_product(request, id):
    if request.method == "GET":
        product_name = RecipeProductName.objects.get(pk=id)
        product_name.delete()
        return redirect(reverse('view_recipe_product'))

''' Recipe Product name function finish '''