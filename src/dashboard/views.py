from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Tag, Ingredient, Recipe, Calendar
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, PreferencesForm, RecipeForm, InstructionsForm, DailyMealPlanForm, CalendarForm
from .models import Preferences, DailyMealPlan
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum

redirectUrl = '../../dashboard'

# Create your views here.
class TagListView(LoginRequiredMixin, generic.ListView):
	model = Tag

class IngredientListView(LoginRequiredMixin, generic.ListView):
	model = Ingredient	

def splash(request):
    # Count of tags and ingredients
    num_tags = Tag.objects.all().count()
    num_ing = Ingredient.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        # 'theme/test.html')
        'theme/splash.html')

def dash(request):
    # Count of tags and ingredients
    num_tags=Tag.objects.all().count()
    num_ing = Ingredient.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        # 'theme/test.html')
        'theme/dashboard.html')

@login_required
def RecipeView(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})


@login_required
@transaction.atomic
def pref(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        Preferences_form = PreferencesForm(request.POST, instance=request.user.preferences)
        if user_form.is_valid() and Preferences_form.is_valid():
            user_form.save()
            Preferences_form.save()
            messages.success(request, 'Your preferences were successfully updated!')
            return redirect(redirectUrl)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        Preferences_form = PreferencesForm(instance=request.user.preferences)
    return render(request, 'theme/preferences.html', context={
        'user_form': user_form,
        'Preferences_form': Preferences_form
    })

def url_redirect(request):
    return HttpResponseRedirect("/dashboard")

@login_required
def recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe.html', {'recipe': recipe})

@login_required
def meal_plan(request, pk):
    meal = get_object_or_404(Calendar, id=pk)
    #Calendar.objects.get(id=pk).meal_plans.aggregate(Sum(''))
    # meal_plans = Calender.objects.all().values_list('meal_plans__pk', flat=True)
    # DailyMealPlan.objects.filter(pk__in=meal_plans).values_list('meal1__pk')
    calories = (Calendar.objects.filter(id=pk).values_list('meal_plans__meal1__calories', flat=True)[0] 
        + Calendar.objects.filter(id=pk).values_list('meal_plans__meal2__calories', flat=True)[0]
        + Calendar.objects.filter(id=pk).values_list('meal_plans__meal3__calories', flat=True)[0])
    calGoalDelta = request.user.preferences.calorie_Goal - calories
    return render(request, 'meal.html', {'meal': meal, 'calories': calories, 'calGoalDelta':calGoalDelta})

# class DashView(LoginRequiredMixin, generic.ListView):
# 	# Count of tags and ingredients
# 	num_tags=Tag.objects.all().count()
# 	num_ing = Ingredient.objects.all().count()

# 	# Number of visits to this view, as counted in the session variable.
# 	num_visits=request.session.get('num_visits', 0)
# 	request.session['num_visits'] = num_visits+1

# 	render(	request,'index.html',context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits})

#If clicked signup, else hits first and opens the SignUpForm, when they fill it out via Post then save, clean and scrape preference attributes
#Then resaves the user
#Login after signing_up
#Redirects to the main dashboard index page
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.preferences.calorie_Goal = form.cleaned_data.get('calorie_Goal')
            user.preferences.fat_Goal = form.cleaned_data.get('fat_Goal')
            user.preferences.carb_Goal = form.cleaned_data.get('carb_Goal')
            user.preferences.protein_Goal = form.cleaned_data.get('protein_Goal')
            user.preferences.tags = form.cleaned_data.get('tags')
            user.preferences.ingredients = form.cleaned_data.get('ingredients')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(redirectUrl)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#When logged in, only one person per account could update preferences
#Opens userform and preferences in sequence as different forms, but still renderd by the page
#Cehcks that both forms were returned filled out valid and then saves the user settings and preferences
#Redirects to dashboard home page 
@login_required
@transaction.atomic
def update_preferences(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        Preferences_form = PreferencesForm(request.POST, instance=request.user.preferences)
        if user_form.is_valid() and Preferences_form.is_valid():
            user_form.save()
            Preferences_form.save()
            messages.success(request, 'Your preferences were successfully updated!')
            return redirect(redirectUrl)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        Preferences_form = PreferencesForm(instance=request.user.preferences)
    return render(request, 'preferences.html', context={
        'user_form': user_form,
        'Preferences_form': Preferences_form
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        #instructions_form = InstructionsForm(request.POST)
        if recipe_form.is_valid(): 
        #and instructions_form.is_valid():
            recipe_form.save()
        #    instructions_form.save()
            messages.success(request, 'Your recipe was successfully updated!')
            return redirect(redirectUrl)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        recipe_form = RecipeForm()
    #    instructions_form = InstructionsForm(request.POST)
    return render(request, 'recipe_form.html', context={
        'recipe_form': recipe_form,
    #    'instructions_form': instructions_form
    })

@login_required
def add_MealPlan(request):
    if request.method == 'POST':
        meal_plan = DailyMealPlanForm(request.POST)
        Calendar_date = CalendarForm(request.POST)
        if meal_plan.is_valid() and Calendar_date.is_valid():
            mp = meal_plan.save()
            mp.refresh_from_db()
            c = Calendar(user_id=request.user.id, meal_plans=mp, date=Calendar_date.cleaned_data.get('date'))
            c.save()
            messages.success(request, 'Your meal_plan was successfully updated!')
            return redirect(redirectUrl)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        meal_plan = DailyMealPlanForm()
        Calendar_date = CalendarForm()
    return render(request, 'meal_plan.html', context={
        'meal_plan': meal_plan,
        'Calendar_date': Calendar_date,
    })

# def index(request):

#     # Count of tags and ingredients
#     num_tags = Tag.objects.all().count()
#     num_ing = Ingredient.objects.all().count()

#     #Last 7 meals
#     meal_plans = Calendar.objects.filter(user_id=request.user.id).order_by('-meal_plans__date')[:7]
#     # mp = DailyMealPlan.objects.filter().values_list('sale__pk', flat=True)
#     # DailyMealPlan.objects.filter(pk__in=lost_sales_id).annotate(Sum('qty'))


#     # Number of visits to this view, as counted in the session variable.
#     num_visits=request.session.get('num_visits', 0)
#     request.session['num_visits'] = num_visits+1

#     return render(
#     request,
#     'index.html',
#     context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits, 'meal_plans': meal_plans})

def main(request):

    # Count of tags and ingredients
    num_tags = Tag.objects.all().count()
    num_ing = Ingredient.objects.all().count()

    #Last 7 meals
    #startdate = datetime.today() - timedelta(days=3)
    startdate = datetime.today()
    #enddate = datetime.today() + timedelta(days=3)
    enddate = datetime.today() + timedelta(days=6)
    meal_plans = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate,enddate]).order_by('-date')


    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
    request,
    'main.html',
    context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits, 'meal_plans': meal_plans})

# def PantryView(request):

#     startdate = datetime.today() - timedelta(days=6)
#     enddate = datetime.today()
#     ingredients = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate,enddate]).values('meal_plans__meal1__ingredients__ing_name', 'meal_plans__meal2__ingredients__ing_name', 'meal_plans__meal3__ingredients__ing_name')
#     #ingredients = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate,enddate]).values('meal_plans__meal1')

#     ingredient = []
#     for ing in ingredients:
#         for name in ing.values():
#             if name not in ingredient:
#                 ingredient.append(name)

#     return render(
#     request,
#     'pantry.html',
#     context={'ingredients':ingredient, })

# def GroceryView(request):

#     startdate = datetime.today() + timedelta(days=1)
#     enddate = startdate + timedelta(days=6)
#     ingredients = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate,enddate]).values('meal_plans__meal1__ingredients__ing_name', 'meal_plans__meal2__ingredients__ing_name', 'meal_plans__meal3__ingredients__ing_name')
#     #ingredients = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate,enddate]).values('meal_plans__meal1')

#     ingredient = []
#     for ing in ingredients:
#         for name in ing.values():
#             if name not in ingredient:
#                 ingredient.append(name)

#     return render(
#     request,
#     'grocery.html',
#     context={'ingredients':ingredient, })

def KitchenView(request):
    startdate1 = datetime.today() + timedelta(days=1)
    enddate1 = startdate1 + timedelta(days=6)
    ingredients1 = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate1,enddate1]).values('meal_plans__meal1__ingredients__ing_name', 'meal_plans__meal2__ingredients__ing_name', 'meal_plans__meal3__ingredients__ing_name')

    groceries = []
    for ing in ingredients1:
        for name in ing.values():
            if name not in groceries:
                groceries.append(name)

    startdate2 = datetime.today() - timedelta(days=6)
    enddate2 = datetime.today()
    ingredients2 = Calendar.objects.filter(user__id=request.user.id).filter(date__range=[startdate2,enddate2]).values('meal_plans__meal1__ingredients__ing_name', 'meal_plans__meal2__ingredients__ing_name', 'meal_plans__meal3__ingredients__ing_name')

    pantry = []
    for ing in ingredients2:
        for name in ing.values():
            if name not in pantry:
                pantry.append(name)

    return render(
    request,
    'kitchen.html',
    context={'groceries':groceries, 'pantry': pantry, })