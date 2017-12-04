from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Ingredient
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