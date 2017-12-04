from django.conf.urls import url
from django.contrib import admin
from dashboard import views

urlpatterns = [
	# url(r'^$', views.DashView.as_view(), name='index'),
	url(r'tags', views.TagListView.as_view(), name='tags'),
	url(r'ingredients', views.IngredientListView.as_view(), name='ingredients'),
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^preferences/$', views.update_preferences, name='preferences'),
	url(r'recipes', views.RecipeView, name='recipes')
]
