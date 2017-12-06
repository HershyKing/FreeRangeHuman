from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Ingredient, Recipe, Instruction, DailyMealPlan
from .models import Preferences

#doesn't require all these fields except the user field
class SignUpForm(UserCreationForm):
    calorie_Goal = forms.IntegerField(required=False, help_text='Optional. In KCals.')
    fat_Goal = forms.IntegerField(required=False, help_text='Optional. In g.')
    carb_Goal = forms.IntegerField(required=False, help_text='Optional. In g.')
    protein_Goal = forms.IntegerField(required=False, help_text='Optional. In g.')
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required = False, help_text='Optional. Choose all that apply')
    ingredients = forms.ModelMultipleChoiceField(Ingredient.objects.all(), required = False, help_text='Optional. Choose all that apply')


    class Meta:
        model = User
        fields = ('username', 'calorie_Goal', 'fat_Goal', 'carb_Goal', 'protein_Goal', 'tags', 'ingredients', 'password1', 'password2')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('calorie_Goal', 'fat_Goal', 'carb_Goal', 'protein_Goal', 'tags', 'ingredients')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'calories', 'servings', 'carb', 'fat', 'protein', 'ingredients', 'tags')

class DailyMealPlanForm(forms.ModelForm):
    class Meta:
        model = DailyMealPlan
        fields = ('date', 'meal1', 'meal2', 'meal3')

# IngredientFormSet = inlineformset_factory(Recipe, Ingredient)
# InstructionFormSet = inlineformset_factory(Recipe, Instruction)
# TagFormSet = inlineformset_factory(Recipe, Tag)

class InstructionsForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ('step_num', 'instruction')


