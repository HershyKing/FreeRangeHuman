from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Represents the meals selected for a certain day
class DailyMealPlan(models.Model):
	# Fields
	meal_plan_id = models.AutoField(primary_key=True)
	date = models.DateField()
	meal1 = models.ForeignKey('Recipe', related_name="meal1", on_delete=models.CASCADE)
	meal2 = models.ForeignKey('Recipe', related_name="meal2", on_delete=models.CASCADE)
	meal3 = models.ForeignKey('Recipe', related_name="meal3", on_delete=models.CASCADE)

	def __str__(self):
		return self.meal_plan_id

	def mealNutrition():
		return []

# Represents an ingrendient in a recipe
class Ingredient(models.Model):
	# Fields
	ing_id = models.AutoField(primary_key=True)
	ing_name = models.CharField(max_length=60)
	ing_num = models.IntegerField()

	def __str__(self):
		return self.ing_name

# Repesents a tag of a recipe
class Tag(models.Model):
	# Fields
	tag_id = models.AutoField(primary_key=True)
	tag_name = models.CharField(max_length=30)

	def __str__(self):
		return self.tag_name

# Represents a single recipe for a meal
class Recipe(models.Model):
	# Fields
	recipe_id = models.AutoField(primary_key=True)
	recipe_name = models.CharField(max_length=50)
	calories = models.IntegerField()
	servings = models.IntegerField()
	fat = models.IntegerField()
	carb = models.IntegerField()
	protein = models.IntegerField()

	# Recipes can have multiple ingrients or tags
	ingredients = models.ManyToManyField(Ingredient)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.recipe_name

	def addNew(details):
		return False

# Represents an instruction for a recipe
class Instruction(models.Model):
	# Fields
	instruct_id = models.AutoField(primary_key=True)
	step_num = models.IntegerField()
	instruction = models.CharField(max_length=100)
	
	# Foreign key
	recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE)

	def __str__(self):
		return self.instruct_id

class Preferences(models.Model):
	#Fields
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	calorie_Goal = models.IntegerField(blank=True, null=True)
	fat_Goal = models.IntegerField(blank=True, null=True)
	carb_Goal = models.IntegerField(blank=True, null=True)
	protein_Goal = models.IntegerField(blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True)
	ingredients = models.ManyToManyField(Ingredient, blank=True)

@receiver(post_save, sender=User)
def create_user_Preferences(sender, instance, created, **kwargs):
    if created:
        Preferences.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_Preferences(sender, instance, **kwargs):
    instance.preferences.save()

#class GroceryList(models.Model):

#class Pantry(models.Model):
