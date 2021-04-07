from django.shortcuts import render
from recipe.models import *
from user.models import *
from hashlib import sha256
from django.http import JsonResponse, response
from eatup_api import views as main_view

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
            email_html = """\
            <h4 style='text-align: center'>New on EatUP</h4>
            <h6>
                Thank you for registering on EatUP, You will enjoy the recipe recommendation and taste of recipe 
                shown in our app, please provide feedback on recipe so we can deliver more better than this...
            </h6>
            """
            main_view.send_mail(email, "Registration", html=email_html)
        return JsonResponse(response, safe=False)

def login_user_via_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email, password=password).exists():
            response = {'status':'pass'}
            email_html = """\
            <h4 style='text-align: center'>New Login</h4>
            <h6>
                Someone has logged in with email <span style="color:red">{}</span>, If you've not logged in than kindly change your password from profile section
            </h6>
            """.format(email)
            main_view.send_mail(email, "Login attempt", html=email_html)
        else:
            response = {'status':'fail'}
        return JsonResponse(response, safe=False)

def login_user_via_email_without_mail(request):
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

def forgot_password_email(request, email):
    if request.method == "GET":
        if User.objects.filter(email=email).exists() == False:
            return JsonResponse({'status':0}, safe=False) # email or mobile not registered 
        
        user = User.objects.get(email=email)
        ForgotPasswordToken.objects.filter(user=user).delete()

        token = main_view.get_random_string(32)
        while(ForgotPasswordToken.objects.filter(token=token).exists()):
            token = main_view.get_random_string(32)
        
        password_token = ForgotPasswordToken(token=token, user=user)
        password_token.save()

        email_html = """\
            <h4 style='text-align: center'>Forgot Password</h4>
            <h6>
                The below is link to change your password for your user account on EatUP, You can change password from there and Ignore email
                if you have not sent the forgot password reset link, It will be valid for next 30 Minutes ...

                <a href="http://3.6.100.169/user/password/forgot/{token}">http://3.6.100.169/user/password/forgot/{token}</a>
            </h6>
        """.format(token=token)
        main_view.send_mail(email, "Password Change", html=email_html)
        
        return JsonResponse({'status':1}, safe=False)


def forgot_password_mobile(request, mobile):
    if request.method == "GET":
        if User.objects.filter(mobile=mobile).exists() == False:
            return JsonResponse({'status':0}, safe=False) # email or mobile not registered 
        
        user = User.objects.get(mobile=mobile)
        ForgotPasswordToken.objects.filter(user=user).delete()

        token = main_view.get_random_string(32)
        while(ForgotPasswordToken.objects.filter(token=token).exists()):
            token = main_view.get_random_string(32)
        
        password_token = ForgotPasswordToken(token=token, user=user)
        password_token.save()

        email_html = """\
            <h4 style='text-align: center'>Forgot Password</h4>
            <h6>
                The below is link to change your password for your user account on EatUP, You can change password from there and Ignore email
                if you have not sent the forgot password reset link, It will be valid for next 30 Minutes ...

                <a href="http://3.6.100.169/user/password/forgot/{token}">http://3.6.100.169/user/password/forgot/{token}</a>
            </h6>
        """.format(token=token)
        main_view.send_mail(user.email, "Password Change", html=email_html)
        
        return JsonResponse({'status':1}, safe=False)


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
                duration = "{} Hour".format(hour) if minute == 0 else "{} Hour {} Minute".format(hour, minute)
            else:
                duration = "{} Minute".format(minute) if second == 0 else "{} Minute {} Seconds".format(minute, second)
                
            recipies.append({'id':recipe.id, 'name':recipe.name.upper(), 'rating':recipe.rating, 'duration':duration})

        return JsonResponse({'data':recipies}, safe=False)

    else:
        return JsonResponse({'data':[]}, safe=False)