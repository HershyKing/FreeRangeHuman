from django.conf.urls import url
from django.contrib import admin
from dashboard import views

urlpatterns = [
	# url(r'^$', views.DashView.as_view(), name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'tags', views.TagListView.as_view(), name='tags'),
	url(r'ingredients', views.IngredientListView.as_view(), name='ingredients'),
	url(r'^preferences/$', views.update_preferences, name='preferences'),
	url(r'recipes', views.RecipeView, name='recipes'),
	url(r'^recipe/(?P<pk>\d+)/$', views.recipe, name='recipe'),
	url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
	url(r'^add_meal/$', views.add_MealPlan, name='add_mealplan'),
	url(r'^meal/(?P<pk>\d+)/$', views.meal_plan, name='meal_plan'),
	url(r'^pref', views.pref, name='pref'),
	url(r'^dash', views.main, name='main'),
	url(r'^$', views.main, name='main'),
	url(r'kitchen', views.KitchenView, name='kitchen'),
	# url(r'pantry', views.PantryView, name='pantry'),
	# url(r'groceries', views.GroceryView, name='groceries'),
	# url(r'^$', views.index, name='index'),
	# url(r'^dash', views.index, name='db'),
	# url(r'^$', views.dash, name='index'),

]
