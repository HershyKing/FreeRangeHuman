from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from dashboard.views import index, signup, update_preferences, TagListView, IngredientListView
from django.test import Client
from dashboard.forms import *   # import all forms

# class Setup_Class(TestCase):

    # def setUp(self):
    #     self.user = User.objects.create(username="test_user", password1="password", password2='password')

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