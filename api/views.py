from django.http.response import HttpResponse
from django.shortcuts import render
from recipe.models import *
from user.models import *
import json
from hashlib import sha256
from django.http import JsonResponse
import datetime


def register_user(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        user = User(mobile=mobile, email=email, password=password)
        response = {}
        if User.objects.filter(email=email).exists():
            response = {'status':'1'}
        elif User.objects.filter(mobile=mobile).exists():
            response = {'status':'2'}
        else:
            user.save()
            response = {'status':'0'}
        return JsonResponse(response, safe=False)

def login_user_via_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email, password=password).exists():
            response = {'status':'pass'}
        else:
            response = {'status':'fail'}
        return JsonResponse(response, safe=False)

def login_user_via_mobile(request):
    if request.method == 'POST':
        mobile = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(mobile=mobile, password=password).exists():
            response = {'status':'pass'}
        else:
            response = {'status':'fail'}
        return JsonResponse(response, safe=False)


def get_all_recipe_category(request):
    if request.method == "GET":
        category = list(RecipeCategory.objects.values().order_by('name'))
        return JsonResponse({'data':category}, safe=False)

def get_recipe_by_category(request, category):
    if request.method == "GET":
        queryset = Recipe.objects.filter(category_id=category).order_by('created_at').reverse()
        recipies = []
        for recipe in queryset:
            total = int(recipe.duration.total_seconds())
            hour = total // 60 // 60
            minute = total // 60 % 60
            second = total % 60
            if hour > 0:
                duration = "{} Hour {} Minutes".format(hour, minute)
            else:
                duration = "{} Minute {} Seconds".format(minute, second)
            recipies.append({'id':recipe.id, 'name':recipe.name.upper(), 'rating':recipe.rating, 'duration':duration})

        return JsonResponse({'data':recipies}, safe=False)

    else:
        return JsonResponse({'data':[]}, safe=False)