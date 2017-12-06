from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Tag, Ingredient, Recipe, Calendar
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, PreferencesForm, RecipeForm, InstructionsForm, DailyMealPlanForm
from .models import Preferences, DailyMealPlan
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here.
class TagListView(LoginRequiredMixin, generic.ListView):
	model = Tag

class IngredientListView(LoginRequiredMixin, generic.ListView):
	model = Ingredient	

@login_required
def RecipeView(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

# class CreateRecipe(CreateView):
#     model = Recipe
#     fields = ['first_name', 'last_name']
#     success_url = reverse_lazy('profile-list')

#     def get_context_data(self, **kwargs):
#         data = super(ProfileFamilyMemberCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['familymembers'] = FamilyMemberFormSet(self.request.POST)
#         else:
#             data['familymembers'] = FamilyMemberFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         familymembers = context['familymembers']
#         with transaction.atomic():
#             self.object = form.save()

#             if familymembers.is_valid():
#                 familymembers.instance = self.object
#                 familymembers.save()
#         return super(ProfileFamilyMemberCreate, self).form_valid(form)

def url_redirect(request):
    return HttpResponsePermanentRedirect("/dashboard/")

@login_required
def recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe.html', {'recipe': recipe})

@login_required
def meal_plan(request, pk):
    meal = get_object_or_404(Calendar, id=pk)
    return render(request, 'meal.html', {'meal': meal})

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
            return redirect('../../dashboard')
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
            return redirect('../../dashboard')
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
        instructions_form = InstructionsForm(request.POST)
        if recipe_form.is_valid() and instructions_form.is_valid():
            recipe_form.save()
            instructions_form.save()
            messages.success(request, 'Your recipe was successfully updated!')
            return redirect('../../dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        recipe_form = RecipeForm(request.POST)
        instructions_form = InstructionsForm(request.POST)
    return render(request, 'recipe_form.html', context={
        'recipe_form': recipe_form,
        'instructions_form': instructions_form
    })

@login_required
def add_MealPlan(request):
    if request.method == 'POST':
        meal_plan = DailyMealPlanForm(request.POST)
        if meal_plan.is_valid():
            mp = meal_plan.save()
            mp.refresh_from_db()
            c = Calendar(user_id=request.user.id, meal_plans=mp)
            c.save()
            messages.success(request, 'Your recipe was successfully updated!')
            return redirect('../../dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        meal_plan = DailyMealPlanForm(request.POST)
    return render(request, 'meal_plan.html', context={
        'meal_plan': meal_plan
    })

def index(request):

    # Count of tags and ingredients
    num_tags = Tag.objects.all().count()
    num_ing = Ingredient.objects.all().count()

    #Last 7 meals
    meal_plans = Calendar.objects.filter(user_id=request.user.id).order_by('-meal_plans__date')[:7]

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
    request,
    'index.html',
    context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits, 'meal_plans': meal_plans})