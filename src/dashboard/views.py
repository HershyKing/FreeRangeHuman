from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tag, Ingredient
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, PreferencesForm
from .models import Preferences
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect


# Create your views here.
class TagListView(LoginRequiredMixin, generic.ListView):
	model = Tag

class IngredientListView(LoginRequiredMixin, generic.ListView):
	model = Ingredient	

def url_redirect(request):
    return HttpResponsePermanentRedirect("/dashboard")

# class DashView(LoginRequiredMixin, generic.ListView):
# 	# Count of tags and ingredients
# 	num_tags=Tag.objects.all().count()
# 	num_ing = Ingredient.objects.all().count()

# 	# Number of visits to this view, as counted in the session variable.
# 	num_visits=request.session.get('num_visits', 0)
# 	request.session['num_visits'] = num_visits+1

# 	render(	request,'index.html',context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits})

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

def index(request):

	# Count of tags and ingredients
	num_tags=Tag.objects.all().count()
	num_ing = Ingredient.objects.all().count()

	# Number of visits to this view, as counted in the session variable.
	num_visits=request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits+1

	return render(
		request,
		'index.html',
		context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits})