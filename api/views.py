from recipe.models import *
from user.models import *
from expense.models import *
from hashlib import sha256
from django.http import JsonResponse
from eatup_api import views as main_view
from datetime import date, datetime

'''user login start '''

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
            response = {'status':'0', 'user_id':User.objects.latest('id')}
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
            user = User.objects.get(email=email)
            response = {'status':'pass', 'user_id':user.id}
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

'''user login end '''

''' recipe start '''

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
                
            recipies.append({'id':recipe.id, 'name':recipe.name.upper(), 'duration':duration})

        return JsonResponse({'data':recipies}, safe=False)

    else:
        return JsonResponse({'data':[]}, safe=False)

def get_single_recipe(request, recipe_id, user_id):

    if request.method == "GET":
        steps = []
        schedules = []
        ingredients = []

        recipe_query = Recipe.objects.get(pk=recipe_id)
        description_query = RecipeDescription.objects.get(recipe=recipe_query)
        steps_query = RecipeSteps.objects.filter(recipe=recipe_query).order_by('index')
        if HomeUser.objects.filter(user_id=user_id).exists() == True:
            home = HomeUser.objects.get(user_id=user_id)
            schedule_query = RecipeSchedule.objects.filter(recipe=recipe_query, home_id=home.home_id, date__gte=date.today()).order_by('date')
        else:
            schedule_query = []
        ingredient_query = RecipeIngredient.objects.filter(recipe=recipe_query)
        total_rating = RecipeRating.objects.filter(recipe=recipe_query).count()
        average_rating = RecipeRating.objects.filter(recipe=recipe_query).aggregate(average=Avg('rating'))
        
        if RecipeRating.objects.filter(recipe=recipe_query, user_id=user_id).exists():
            user_rating = RecipeRating.objects.get(recipe=recipe_query, user_id=user_id)
            rating = {'rating':user_rating.rating, 'feedback':user_rating.feedback}
        else:
            rating = {'rating':0, 'feedback':""}

        total = int(recipe_query.duration.total_seconds())
        hour = total // 60 // 60
        minute = total // 60 % 60
        second = total % 60
        if hour > 0:
            duration = "{} Hour".format(hour) if minute == 0 else "{} Hour {} Minute".format(hour, minute)
        else:
            duration = "{} Minute".format(minute) if second == 0 else "{} Minute {} Seconds".format(minute, second)

        for step in steps_query:
            steps.append({'index':step.index, 'description':step.description, 'wait':step.min_wait})

        for schedule in schedule_query:
            if schedule.meal == 0:
                meal = "Breakfast"
            elif schedule.meal == 1:
                meal = "Lunch"
            else:
                meal = "Dinner"

            schedules.append({'description': "* Scheduled on {} for {}".format(schedule.date.strftime("%d %B %Y"), meal)})

        for ingredient in ingredient_query:
            weight = ""
            if ingredient.weight != 0:
                if(ingredient.weight < 0):
                    weight = weight + str(int(ingredient.weight*1000)) + " Grams"
                else:
                    weight = weight + "{} Kilo".format(ingredient.weight)
            elif ingredient.litre != 0:
                if(ingredient.litre < 0):
                    weight = weight + str(int(ingredient.litre*1000)) + " ML"
                else:
                    weight = weight + "{} L".format(ingredient.litre)
            elif ingredient.spoon != 0:
                weight = weight + "{} Spoon".format(ingredient.spoon)
            elif ingredient.cup != 0:
                weight = weight + "{} Cup".format(ingredient.cup)
            elif ingredient.quantity:
                weight = weight + "{} Pieces".format(ingredient.quantity)

            ingredients.append({'name':ingredient.recipe_product_name.name, 'weight':weight})

        return JsonResponse({
            'schedule':schedules,
            'step':steps,
            'recipe':{
                'name':recipe_query.name, 
                'duration':duration, 
                'description':description_query.description,
                'rating': average_rating['average'] if average_rating['average'] != None else 0,
                'total_rating':total_rating
            },
            'rating':rating,
            'ingredient':ingredients
        }, safe=False)

def add_recipe_rating(request, recipe_id, user_id):
    if request.method == "POST":
        rating = request.POST['rating']
        feedback = request.POST['feedback']
        if(RecipeRating.objects.filter(recipe_id=recipe_id, user_id=user_id).exists()):
            RecipeRating.objects.filter(recipe_id=recipe_id, user_id=user_id).update(rating=rating, feedback=feedback)
        else:
            recipe_rating = RecipeRating(rating=rating, feedback=feedback, recipe_id=recipe_id, user_id=user_id)
            recipe_rating.save()
        return JsonResponse({'status':1}, safe=False)

def schedule_recipe(request):
    if request.method == "POST":
        home_user = HomeUser.objects.get(user_id=request.POST['user'])
        home = Home.objects.get(pk=home_user.home_id)
        recipe = Recipe.objects.get(pk=request.POST['recipe'])
        meal = request.POST['meal']
        date = request.POST['date']

        user_index = 0
        user_list = []
        while True:
            if "user"+str(user_index) in request.POST.keys():
                user_list.append(request.POST['user'+str(user_index)])
                user_index = user_index + 1
            else:
                break

        recipe_schedule = RecipeSchedule(home=home, recipe=recipe, meal=meal, date=date)
        recipe_schedule.save()

        expense = Expense(schedule=recipe_schedule, user=home_user.user, amount=0)
        expense.save()

        for user in user_list:
            expense_user = ExpenseUser(expense=expense, user=User.objects.get(email=user))
            expense_user.save()
        
        return JsonResponse({'status':1}, safe=False)

def get_recipe_schedule(request, user_id):
    schedule_list = []
    if request.method == "GET":
        if HomeUser.objects.filter(user_id=user_id).exists() == True:
            home = Home.objects.get(id = HomeUser.objects.get(user_id=user_id).home_id)

            today = date.today()
            schedule_query = RecipeSchedule.objects.filter(home=home, date__gte = today).order_by('date')
        else:
            schedule_query = []

        for schedule in schedule_query:
            meal = ""
            if schedule.meal == 0:
                meal = "Breakfast"
            elif schedule.meal == 1:
                meal = "Lunch"
            else:
                meal = "Dinner"
            schedule_list.append({'id':schedule.id, 'recipe_name':schedule.recipe.name, 'date':schedule.date.strftime("%d %B %Y"), 'meal':meal})
        
        return JsonResponse({'schedule':schedule_list}, safe=False)

def remove_recipe_schedule(request, schedule_id):
    if request.method == "GET":
        expense = Expense.objects.get(schedule_id=schedule_id)
        ExpenseUser.objects.filter(expense=expense).delete()
        Expense.objects.filter(pk=expense.id).delete()
        RecipeSchedule.objects.filter(pk=schedule_id).delete()
        return JsonResponse({'status':1}, safe=False)

''' recipe end '''

''' home start '''

def create_home(request):
    if request.method == "POST":
        name = request.POST['name']
        user_id = request.POST['user']

        if Home.objects.filter(name=name).exists() == True:
            response = {'status':0}
        
        else:
            home = Home(name=name, user_id=user_id)
            home.save()
            response = {'status':1}

        JsonResponse(response, safe=False)

def get_user_home(request, user_id):
    if request.method == "GET":
        user_list = []
        home_list = {}

        if HomeUser.objects.filter(user_id=user_id).exists():
            home_user = HomeUser.objects.get(user_id=user_id)
            if home_user.is_root == True:
                response = {'root':1, 'home_exist':1}
            else:
                response = {'root':0, 'home_exist':1}
            users = HomeUser.objects.filter(home_id=home_user.home_id)

            for user in users:
                user_list.append({'id':user.user_id, 'email':user.user.email, 'mobile':user.user.mobile})

            if Home.objects.filter(pk=home_user.home_id).exists():
                home = Home.objects.get(pk=home_user.home_id)
                home_list.update({'name':home.name})
            else:
                home_list.update({'name':""})
        
            response.update({'user':user_list, 'home':home_list})
        else:
            response = {'home_exist':0}
        
        return JsonResponse(response, safe=False)

def join_home(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['user'])
        home = Home.objects.get(name=request.POST['home'])
        response = {}
        if(Home.objects.filter(pk=home.id).exists() == False):
            response.update({'status':0})
        else:
            home_user = HomeUser(user=user, home=home)
            home_user.save()
            response.update({'status':1})
        return JsonResponse(response, safe=False)

def create_home(request):
    if request.method == "POST":
        name = request.POST['name']
        user = User.objects.get(pk=request.POST['user'])

        response = {}

        if(Home.objects.filter(name=name).exists()):
            response.update({'status':0})
        else:
            home = Home(name=name, root_user=user)
            home.save()

            home_user = HomeUser(user=user, home=home, is_root=True)
            home_user.save()

            response.update({'status':1, 'home':home.id})

        return JsonResponse(response, safe=False)

def add_user_to_home(request):
    if request.method == "POST":
        response = {}
        if User.objects.filter(email=request.POST['email'], mobile=request.POST['mobile']).exists():
            user = User.objects.get(email=request.POST['email'], mobile=request.POST['mobile'])
            if HomeUser.objects.filter(user=user).exists():
               response = {'status':2}
            else: 
                adder_user = User.objects.get(pk=request.POST['user_id'])
                home = HomeUser.objects.get(user=adder_user).home
                home_user = HomeUser(home=home, user=user)
                home_user.save()
                response = {'status':1}

        else:
            response = {'status':0}

        return JsonResponse(response, safe=False)

def remove_user_from_home(request, user_id):
    if request.method == "GET":
        HomeUser.objects.filter(user_id=user_id).delete()
        return JsonResponse({'status':1}, safe=False)

def check_user_role(request, user_id):
    if request.method == "GET":
        home_user = HomeUser.objects.get(user_id=user_id)
        return JsonResponse({'is_root':home_user.is_root}, safe=False)

def exit_home(request, user_id):
    if request.method == "GET":
        user_home = HomeUser.objects.get(user_id=user_id)
        home_id = user_home.home.id
        user_home.delete()
        response = {}
        if user_home.is_root:
            if(HomeUser.objects.filter(home_id=home_id).exists() == False):
                Home.objects.filter(pk=home_id).delete()
                response = {'status':1}
            else:
                new_home_root = HomeUser.objects.filter(home_id=home_id).earliest("created_by")
                HomeUser.objects.filter(home_id=home_id, user=new_home_root.user).update(is_root=True)
                response = {'status':1}
        else:
            HomeUser.objects.filter(user_id=user_id).delete()
            response = {'status':1}

        return JsonResponse(response, safe=False)
''' home end '''

''' expense splitter start '''

def get_expense(request, user_id):
    if request.method == "GET":
        user_expense = {}
        expense_list = []
        start_date, end_date = "", ""
        today = datetime.now()
        date_range = []
        if(today.day <= 15):
            date_range = [str(today.year)+"-"+str(today.month)+"-01", str(today.year)+"-"+str(today.month)+"-15"]
            start_date = "01-"+str(today.month)+"-"+str(today.year)
            end_date = "15-"+str(today.month)+"-"+str(today.year)
        else:
            if(today.month in [1,3,5,7,8,10,12]):
                date_range = [str(today.year)+"-"+str(today.month)+"-16", str(today.year)+"-"+str(today.month)+"-31"]
                start_date = "16-"+str(today.month)+"-"+str(today.year)
                end_date = "31-"+str(today.month)+"-"+str(today.year)
            elif(today.month in [4,6,9,11]):
                date_range = [str(today.year)+"-"+str(today.month)+"-16", str(today.year)+"-"+str(today.month)+"-30"]
                start_date = "16-"+str(today.month)+"-"+str(today.year)
                end_date = "30-"+str(today.month)+"-"+str(today.year)
            else:
                if(today.year % 4 == 0):
                    date_range = [str(today.year)+"-"+str(today.month)+"-16", str(today.year)+"-"+str(today.month)+"-29"]
                    start_date = "16-"+str(today.month)+"-"+str(today.year)
                    end_date = "29-"+str(today.month)+"-"+str(today.year)
                else:
                    date_range = [str(today.year)+"-"+str(today.month)+"-16", str(today.year)+"-"+str(today.month)+"-28"]
                    start_date = "16-"+str(today.month)+"-"+str(today.year)
                    end_date = "28-"+str(today.month)+"-"+str(today.year)

        home = HomeUser.objects.get(user_id=user_id).home
        schedule = RecipeSchedule.objects.filter(date__gte=date_range[0], date__lte=date_range[1], home=home)
        expense_obj = Expense.objects.filter(schedule__in=schedule)

        for obj in expense_obj:
            expense_user_obj = ExpenseUser.objects.filter(expense = obj)
            individual = obj.amount / expense_user_obj.count()
            for user in expense_user_obj:
                if user.user_id in user_expense.keys():
                    user_expense[user.user_id] += individual
                else:
                    user_expense[user.user_id] = individual

        for id in user_expense:
            expense_list.append({
                'email' : User.objects.get(pk=id).email,
                'amount' : user_expense[id]
            })
        return JsonResponse({
            'expense':expense_list,
            'date' : start_date + " to " + end_date
            }, safe=False)


def add_amount_to_expense(request, schedule_id):
    if request.method == "POST":
        amount = request.POST['amount']
        Expense.objects.filter(schedule_id=schedule_id).update(amount=amount)
        return JsonResponse({'status':1}, safe=False)

def load_remaining_amount(request, user_id):
    if request.method == "GET":
        response = []
        home = HomeUser.objects.get(user_id=user_id).home
        schedule = RecipeSchedule.objects.filter(home=home)
        expenses = Expense.objects.filter(schedule__in=schedule, amount=0)

        for expense in expenses:
            response.append({
                'recipe':expense.schedule.recipe.name,
                'date': "{}-{}-{}".format(expense.schedule.date.day,expense.schedule.date.month,expense.schedule.date.year),
                'schedule_id':expense.schedule.id,
            })
        return JsonResponse({'expense':response}, safe=False)

''' expense splitter end '''

''' home page starts '''
def index(request, user_id):
    if request.method == "GET":
        # logistic regression should be implemented to find recipe visible to user
        recipe = list(Recipe.objects.all().values('id', 'name'))
        return JsonResponse({
            'recipe':recipe,
            'banner':"1.jpg", # banner path will be fetched from database and will sent to android
            }, safe=False)

''' home page ends '''