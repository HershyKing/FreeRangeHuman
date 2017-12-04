from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import DailyMealPlan, Ingredient, Tag, Recipe, Instruction
from .models import Preferences


# Allows admin site to view models
admin.site.register(DailyMealPlan)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Instruction)

class PreferencesInline(admin.StackedInline):
    model = Preferences
    can_delete = False
    verbose_name_plural = 'Preferences'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (PreferencesInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)