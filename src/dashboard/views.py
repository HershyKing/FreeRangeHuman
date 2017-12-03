from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Ingredient
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TagListView(LoginRequiredMixin, generic.ListView):
	model = Tag

class IngredientListView(LoginRequiredMixin, generic.ListView):
	model = Ingredient	

# class DashView(LoginRequiredMixin, generic.ListView):
# 	# Count of tags and ingredients
# 	num_tags=Tag.objects.all().count()
# 	num_ing = Ingredient.objects.all().count()

# 	# Number of visits to this view, as counted in the session variable.
# 	num_visits=request.session.get('num_visits', 0)
# 	request.session['num_visits'] = num_visits+1

# 	render(	request,'index.html',context={'num_tags':num_tags, 'num_ing':num_ing, 'num_visits':num_visits})

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