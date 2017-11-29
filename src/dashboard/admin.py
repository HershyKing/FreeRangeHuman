from django.contrib import admin
from .models import DailyMealPlan, Ingredient, Tag, Recipe, Instruction

# Allows admin site to view models
admin.site.register(DailyMealPlan)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Instruction)