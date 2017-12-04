from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from dashboard.views import index, signup, update_preferences, TagListView, IngredientListView, RecipeView, recipe
from django.test import Client
from dashboard.forms import *   # import all forms
from dashboard.models import Recipe, Tag, Ingredient

class SetUp_Class(TestCase):

	def setUp(self):
		self.user = User.objects.create(username='test_user')
		self.user.set_password('abcde12345')
		self.user.save()

class ValidForm_Test(TestCase):

		# Valid Form Data
	def test_SignUp_valid(self):
		form = SignUpForm(data={'username': "test", 'password1': "abcde12345", 'password2': "abcde12345",
			 'calorie_Goal': "", 'fat_Goal': "", 'carb_Goal' : "", 'protein_Goal': "", 'tags': "", 'ingredients': "", })
		self.assertTrue(form.is_valid())

	def test_UserForm_valid(self):
		form = UserForm(data={'email': "user@fake.com", 'last_name': "test", 'first_name': "user"})
		self.assertTrue(form.is_valid())

	def test_PreferencesForm_valid(self):
		form = PreferencesForm(data={'calorie_Goal': "", "fat_Goal": "", "carb_Goal": "", 'protein_Goal': "", 
			'tags': "", 'ingredients': ""})
		self.assertTrue(form.is_valid())

class User_Views_Test(SetUp_Class):

    def test_home_view(self):
        user_login = self.client.login(username="test_user", password="abcde12345")
        self.assertTrue(user_login)
        response = self.client.get("/")
        #301 because permanently set dashboard to root url redirection
        self.assertEqual(response.status_code, 301)

class HomeTests(TestCase):

	def setUp(self):
		url = reverse('index')
		self.response = self.client.get(url)

	def test_home_view_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/dashboard/')
		self.assertEquals(view.func, index)

	def test_home_view_contains_link_to_index_page(self):
		self_url = reverse('index')
		self.assertContains(self.response, 'href="{0}"'.format(self_url))

	def test_home_view_contains_link_to_tag_page(self):
		tag_url = reverse('tags')
		self.assertContains(self.response, 'href="{0}"'.format(tag_url))

	def test_home_view_contains_link_to_ingredient_page(self):
		ingredient_url = reverse('ingredients')
		self.assertContains(self.response, 'href="{0}"'.format(ingredient_url))

	def test_home_view_contains_link_to_recipes_page(self):
		recipe_url = reverse('recipes')
		self.assertContains(self.response, 'href="{0}"'.format(recipe_url))

	#These links for the url redirect to dashboard right after so need to explciitly define that behavior
	def test_home_view_contains_link_to_login_page(self):
		login_url = reverse('login')
		self.assertContains(self.response, 'href="{0}"'.format(login_url+"?next=/dashboard/"))

	def test_home_view_contains_link_to_register_page(self):
		register_url = reverse('signup')
		self.assertContains(self.response, 'href="{0}"'.format(register_url+"?next=/dashboard/"))

class SignUpTest(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_index_view_success_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_index_url_resolves_index_view(self):
		view = resolve('/dashboard/signup/')
		self.assertEquals(view.func, signup)

class RecipesTest(TestCase):
	def setUp(self):
		url = reverse('recipes')
		self.response = self.client.get(url)

	def test_recipe_view_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_recipe_url_resolves_recipe_view(self):
		view = resolve('/dashboard/recipes')
		self.assertEquals(view.func, RecipeView)

class RecipeTests(TestCase):
	def setUp(self):
		tag = Tag.objects.create(tag_name="Vegan")
		tag.save()
		ing = Ingredient.objects.create(ing_name="Carrot", ing_num=1)
		ing.save()
		recipe = Recipe.objects.create(recipe_id=1, recipe_name='Django', calories=50, servings=2, fat=8, carb=7, protein=9)
		recipe.save()
		recipe.tags.add(tag)
		recipe.ingredients.add(ing)
		recipe.save()


	def test_board_topics_view_success_status_code(self):
		url = reverse('recipe', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_board_topics_view_not_found_status_code(self):
		url = reverse('recipe', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_board_topics_url_resolves_board_topics_view(self):
		view = resolve('/recipe/1/')
		self.assertEquals(view.func, recipe)
