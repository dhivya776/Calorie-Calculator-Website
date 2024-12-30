from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FoodItem, UserFooditem, Exercise, Customer, Meal, Document
from django.forms import modelformset_factory

# User Creation Form
class createUserForm(UserCreationForm):
    email = forms.EmailField()
    ROLE_CHOICES = [
        ('user','User'),
        ('admin','Admin')
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True,widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','role']

# Food Item Form
class fooditemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'carbohydrate', 'fats', 'protein', 'calories', 'meal_type']

# Add User Food Item Form
class addUserFooditem(forms.Form):
    fooditem_list = forms.ModelMultipleChoiceField(queryset=FoodItem.objects.all(), widget=forms.CheckboxSelectMultiple)

# Add Exercise Form
class addExercise(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'calorie', 'time']

# Set Calorie Goal Form
class FoodIntakeForm(forms.Form):
    daily_intake = forms.FloatField(label='Enter Your Daily Calorie Intake', required=True)

    def clean_daily_intake(self):
        daily_intake = self.cleaned_data['daily_intake']
        if daily_intake <= 0:
            raise forms.ValidationError("Calorie intake must be a positive number.")
        return daily_intake

# Meal Form (For adding meal-related data)
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['customer', 'fooditems']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

from django import forms
from .models import Customer

class CalorieNeedsForm(forms.Form):
    GENDER_CHOICES = [ ('male','Male'),('female','Female'),]
    age = forms.IntegerField(min_value=1, required=True)
    height = forms.IntegerField(min_value=1, required=True)
    weight = forms.IntegerField(min_value=1, required=True)
    activity_level = forms.ChoiceField(choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
                                       required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    goal = forms.ChoiceField(choices=[('lose', 'Lose Weight'), 
                                      ('maintain', 'Maintain Weight'),
                                      ('gain', 'Gain Weight')],
                             required=True)
    


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'file')