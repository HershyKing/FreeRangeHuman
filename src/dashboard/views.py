from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Ingredient
from django.views import generic
# Create your views here.
class TagListView(generic.ListView):
	model = Tag

def index(request):

	num_tags=Tag.objects.all().count()

	num_ing = Ingredient.objects.all().count()

	return render(
		request,
		'index.html',
		context={'num_tags':num_tags, 'num_ing':num_ing})