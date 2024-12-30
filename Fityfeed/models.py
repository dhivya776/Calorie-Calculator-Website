from django.db import models
from django.db.models import Index
from django.contrib.auth.models import User
# Define a function to get the default category
def get_default_category():
    return Category.objects.first()  # Or another logic to fetch a category
GOAL_CHOICES=[('maintain', 'Maintain'),
    ('lose', 'Lose Weight'),
    ('gain', 'Gain Weight'),]
# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')
    calorie_limit = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=10, choices=[('lose', 'Lose'), ('gain', 'Gain'), ('maintain', 'Maintain')])
    calorie_intake = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    activity_level = models.CharField(max_length=10, choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')])
    calorie_goal=models.CharField(max_length=100, choices=GOAL_CHOICES, default='maintain')
    calorie_needs=models.IntegerField(null=True,blank=True)
    daily_intake = models.FloatField(blank=True, null=True) 
    def __str__(self):
        return self.user.username

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# FoodItem Model
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    # Inside your model
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default=get_default_category)
    carbohydrate = models.FloatField(max_length=100,default=0)
    fats= models.FloatField(max_length=100,default=0)
    protein = models.FloatField(max_length=100,default=0)

    calories = models.PositiveIntegerField(default=0)
    meal_type = models.CharField(max_length=20,choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], default='Breakfast')
    def __str__(self):
        return self.name

# UserFooditem Model
class UserFooditem(models.Model):
    def get_default_user_id():
        user = User.objects.first()  # Fetch the first User
        return user.id if user else None  # Return the ID if a user exists, otherwise None

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=get_default_user_id)

    fooditem = models.ManyToManyField(FoodItem)

    def __str__(self):
        return f"{self.customer.name} - FoodItems"

# Exercise Model
class Exercise(models.Model):
    def get_default_user_id():
        user = User.objects.first()  # Fetch the first User
        return user.id if user else None  # Return the ID if a user exists, otherwise None

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=get_default_user_id)

    name = models.CharField(max_length=255)
    calorie = models.IntegerField()
    time = models.TimeField()
    def __str__(self):
        return f"{self.user.username if self.user else 'No User'} - {self.name}"

# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    age = models.IntegerField(null = True, blank = True)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    role = models.CharField(max_length = 20, choices=[('user','User'),('admin','Admin')],default='user') # No default
    calorie_needs = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.user.username
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Save the user profile when the user is saved
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
# Meal Model
class Meal(models.Model):
    def get_default_user_id():
        user = User.objects.first()  # Fetch the first User
        return user.id if user else None  # Return the ID if a user exists, otherwise None

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=get_default_user_id)

    date = models.DateField(auto_now_add=True)
    fooditems = models.ManyToManyField(FoodItem)

    def __str__(self):
        return f"Meal for {self.customer.name} on {self.date}"


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


