from django.db import models, JSONField

class Recipes(models.Model):
	
    name = models.CharField(max_length=50)
	instructions = JSONField()
	ingredients = JSONField()
	tags = JSONField()
	nut_info = JSONField()

	def add_new_recipe(self, parameters):
		r = Recipes(parameters)
		r.save()
		return True

class NutritionInfo(models.Model):
	
    calories = models.IntegerField()
	servings = models.IntegerField()
	Nutrients = JSONField()
	Vitamins = JSONField()

class Account(models.Model):
	
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    cal = JSONField()

    def validate_user(self, email, password):
    	return False

    def reset_password(self, new_pass):
    	return False

    def create_account(self, email, password):
    	a = Recipes(self.email=email, self.password = password)
		a.save()
    	return False

class Preferences(models.Model):
	tags = JSONField()
	ingredients = JSONField()
    calorie_goal = models.IntegerField()
    vitamin_goal = models.IntegerField()
	nutrient_goal = models.IntegerField()
	num_meals = models.IntegerField()