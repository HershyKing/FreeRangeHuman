from django.shortcuts import render

# Create your views here.
from .models import DailyMealPlan, Ingredient, Tag, Recipe, Instruction
# from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_meal_plans=DailyMealPlan.objects.all().count()
    num_ingredients=Ingredient.objects.all().count()
    num_tags=Tag.objects.all().count()
    # num_recipes=Recipe.all().count()
    # num_instruction=Instruction.objects.all().count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        # context={'num_meal_plans':num_meal_plans, 'num_ingredients':num_ingredients, 'num_tags':num_tags, 'num_recipes':num_recipes, 'num_instruction':num_instruction},
        context={'num_meal_plans':num_meal_plans, 'num_ingredients':num_ingredients, 'num_tags':num_tags},
    )