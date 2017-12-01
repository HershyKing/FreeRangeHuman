from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import DailyMealPlan, Ingredient, Tag, Recipe, Instruction, Preferences

# Allows admin site to view models
admin.site.register(DailyMealPlan)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Instruction)

class PreferencesInline(admin.StackedInline):
	model = Preferences
	can_delete = False

class UserAdmin(BaseUserAdmin):
	inlines = (PreferencesInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)