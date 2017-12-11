from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Ingredient, Recipe, Instruction, DailyMealPlan, Calendar
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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        # form-control
    # def as_p(self):
    #     return self._html_output(
    #         normal_row = u'<p%(html_class_attr)s>%(label)s</p><h1>WHAT</h1> %(field)s%(help_text)s',
    #         error_row = u'%s',
    #         row_ender = '</p>',
    #         help_text_html = u' <span class="helptext">%s</span>',
    #         errors_on_separate_row = True)

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)

    #     self.helper = FormHelper()
    #     self.helper.form_action = reverse_lazy('movie_add')
    #     self.helper.form_method = "POST"

    #     self.helper.layout = layout.Layout(
    #         layout.Fieldset("Movie data",
    #             layout.Field("title"),
    #             layout.Field("year"),
    #             layout.Div(
    #                 bootstrap.PrependedText('rating',
    #                     """<span class="glyphicon glyphicon-thumbs-up"></span>""",
    #                     css_class="inputblock-level",
    #                     placeholder="Rating"
    #                 )
    #             ),
    #             bootstrap.FormActions(
    #                 layout.Submit("submit", "Save", css_class="btn-success"),
    #             )
    #         )
    #     )

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('calorie_Goal', 'fat_Goal', 'carb_Goal', 'protein_Goal', 'tags', 'ingredients')

    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)
        self.fields['calorie_Goal'].widget.attrs['class'] = 'form-control'
        self.fields['fat_Goal'].widget.attrs['class'] = 'form-control'
        self.fields['carb_Goal'].widget.attrs['class'] = 'form-control'
        self.fields['protein_Goal'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['ingredients'].widget.attrs['class'] = 'form-control'

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'calories', 'servings', 'carb', 'fat', 'protein', 'ingredients', 'tags')
    
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['recipe_name'].widget.attrs['class'] = 'form-control'
        self.fields['calories'].widget.attrs['class'] = 'form-control'
        self.fields['servings'].widget.attrs['class'] = 'form-control'
        self.fields['carb'].widget.attrs['class'] = 'form-control'
        self.fields['fat'].widget.attrs['class'] = 'form-control'
        self.fields['protein'].widget.attrs['class'] = 'form-control'
        self.fields['ingredients'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-control'


class DailyMealPlanForm(forms.ModelForm):
    class Meta:
        model = DailyMealPlan
        fields = ('meal1', 'meal2', 'meal3')

# IngredientFormSet = inlineformset_factory(Recipe, Ingredient)
# InstructionFormSet = inlineformset_factory(Recipe, Instruction)
# TagFormSet = inlineformset_factory(Recipe, Tag)

class InstructionsForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ('step_num', 'instruction')

class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ('date',)
