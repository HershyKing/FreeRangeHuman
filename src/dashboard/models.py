from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Represents the meals selected for a certain day
class DailyMealPlan(models.Model):
	# Fields
	meal_plan_id = models.AutoField(primary_key=True)
	# date = models.DateField()
	meal1 = models.ForeignKey('Recipe', related_name="meal1", on_delete=models.CASCADE)
	meal2 = models.ForeignKey('Recipe', related_name="meal2", on_delete=models.CASCADE)
	meal3 = models.ForeignKey('Recipe', related_name="meal3", on_delete=models.CASCADE)

	def __str__(self):
		return str(self.meal_plan_id)

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
		return str(self.instruct_id)
		
#Extend user class by using a one to one relation between the two
class Preferences(models.Model):
	#Fields
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	calorie_Goal = models.IntegerField(blank=True, null=True)
	fat_Goal = models.IntegerField(blank=True, null=True)
	carb_Goal = models.IntegerField(blank=True, null=True)
	protein_Goal = models.IntegerField(blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True)
	ingredients = models.ManyToManyField(Ingredient, blank=True)

	def __str__(self):
		return str(self.user.id)

# @receiver(post_save, sender=DailyMealPlan)
# def createCalendar(sender, instance, created, **kwargs):
# 	if created:
# 		Calendar.objects.create(user=instance)

#After call to save function of user then check if need to save preferences by updating or creating a new object
@receiver(post_save, sender=User)
def create_user_Preferences(sender, instance, created, **kwargs):
    if created:
        Preferences.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_Preferences(sender, instance, **kwargs):
    instance.preferences.save()

class Calendar(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField()
	meal_plans = models.ForeignKey('DailyMealPlan', on_delete=models.CASCADE)

	class Meta:
		unique_together = (('date', 'user'),)


# def validate_unique(self, exclude=None):
# 	qs = Calendar.objects.filter(date=self.date)
# 	if qs.filter(meal_plans__id=self.meal_plans.id).exists():
# 		raise ValidationError('Must be unique meal plan for day')

	def save(self, *args, **kwargs):
		self.validate_unique()
		super(Calendar, self).save(*args, **kwargs)

	def __str__(self):
		return(str(self.id))


#class GroceryList(models.Model):

#class Pantry(models.Model):
