from django.db import models

# Represents the meals selected for a certain day
class DailyMealPlan(models.Model):
	# Fields
	meal_plan_id = models.IntegerField(primary_key=True)
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
	ing_id = models.IntegerField(primary_key=True)
	ing_name = models.CharField(max_length=60)

	def __str__(self):
		return self.ing_name

# Repesents a tag of a recipe
class Tag(models.Model):
	# Fields
	tag_id = models.IntegerField(primary_key=True)
	tag_name = models.CharField(max_length=30)

	def __str__(self):
		return self.tag_name

# Represents a single recipe for a meal
class Recipe(models.Model):
	# Fields
	recipe_id = models.IntegerField(primary_key=True)
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
	instruct_id = models.IntegerField(primary_key=True)
	step_num = models.IntegerField()
	instruction = models.CharField(max_length=100)
	
	# Foreign key
	recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE)

	def __str__(self):
		return self.instruct_id



