from django.http.response import HttpResponse
from django.shortcuts import render
from recipe.models import *
from user.models import *
import json
from hashlib import sha256
from django.http import JsonResponse


def register_user(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = sha256(request.POST['password'].encode())
        user = User(mobile=mobile, email=email, password=password.hexdigest())
        response = {}
        if User.objects.filter(email=email).exists():
            response = {'status':'fail'}
        elif User.objects.filter(mobile=mobile).exists():
            response = {'status':'fail'}
        else:
            user.save()
            response = {'status':'pass'}
        return HttpResponse(json.dumps(response))

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = sha256(request.POST['password'].encode())
        if User.objects.filter(email=email, password=password.hexdigest()).exists():
            response = {'status':'pass'}
        else:
            response = {'status':'fail'}
        return JsonResponse(response, safe=False)



def get_all_recipe_category(request):
    if request.method == "GET":
        category = list(RecipeCategory.objects.values().order_by('name'))
        return JsonResponse(category, safe=False)