from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import createUserForm, fooditemForm, addUserFooditem, addExercise, FoodIntakeForm
from .models import Customer, Category, FoodItem, UserFooditem, Exercise, UserProfile, Meal
from .filters import FoodItemFilter
from datetime import date
from django.http import HttpResponse
from django.db.models import Sum
from .forms import *
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from .models import Category, Customer
from .forms import CalorieNeedsForm  # If needed for updating calorie goals  # Assuming you have a utility function for calorie calculation

 # Assuming calculate_calories is a function that calculates the needs
def calculate_calories(age, height=None, weight=0, activity_level='moderate', gender='male', goal='maintain'):
    """
    Calculate daily calorie needs based on user input.
    :param age: Age of the person (years)
    :param height: Height of the person (cm, default: 180 for males, 170 for females)
    :param weight: Weight of the person (kg)
    :param activity_level: Activity level ('low', 'moderate', 'high')
    :param gender: Gender ('male', 'female')
    :param goal: Weight goal ('maintain', 'lose', 'gain')
    :return: Daily calorie needs (int)
    """
    if age <= 0 or weight <= 0:
        raise ValueError("Age and weight must be positive values.")
    if activity_level not in ['low', 'moderate', 'high']:
        raise ValueError("Invalid activity level. Choose 'low', 'moderate', or 'high'.")
    if goal not in ['maintain', 'lose', 'gain']:
        raise ValueError("Invalid goal. Choose 'maintain', 'lose', or 'gain'.")
    if gender not in ['male', 'female']:
        raise ValueError("Invalid gender. Choose 'male' or 'female'.")

    # Default height based on gender
    height = height or (180 if gender == 'male' else 170)

    # BMR calculation (Basic Metabolic Rate)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust BMR for activity level
    activity_multiplier = {
        'low': 1.2,
        'moderate': 1.55,
        'high': 1.9
    }
    calorie_needs = bmr * activity_multiplier[activity_level]

    # Adjust for weight goal
    if goal == 'lose':
        calorie_needs -= 500
    elif goal == 'gain':
        calorie_needs += 500

    return int(calorie_needs)

# Home view to update calorie needs for each user
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer

@login_required

def home(request):
    user = request.user

    # Retrieve the user's profile and calorie needs, create profile if not exists
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    calorie_needs = user_profile.calorie_needs  # Get the calorie_needs or None if not set

    context = {
        'user': request.user,
        'calorie_needs': calorie_needs,  # Pass the calorie_needs to the template
    }

    return render(request, 'main.html', context)


def fooditem(request):
    breakfast = Category.objects.filter(name='breakfast')[0].fooditems.all()
    lunch = Category.objects.filter(name='lunch')[0].fooditems.all()
    dinner = Category.objects.filter(name='dinner')[0].fooditems.all()
    snacks = Category.objects.filter(name='snacks')[0].fooditems.all()

    context = {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
    }
    return render(request, 'fooditem.html', context)

# views.py
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import createUserForm
from .models import Customer

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import createUserForm  # Assuming you have this form for validation
from .models import Customer  # Assuming you have a Customer model

def registerPage(request):
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            role = form.cleaned_data['role']

            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists. Please choose a different one.')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists. Please choose a different one.')
                return redirect('register')

            # Create the user and associate the password
            user = User.objects.create_user(username=username, email=email, password=password1)
            UserProfile.objects.create(user=user, role=role)
            # If the user is not an admin, create a customer profile
            if role != 'admin':
                Customer.objects.create(
                    user=user,
                    name=username,
                    email=email,
                    calorie_limit =None, 

                        # Default calorie limit, adjust as necessary
                )
                user.is_staff=False
                user.save()
            
            # If the user is an admin, assign the is_staff flag
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
    
                
                  # Save the user object after role assignment
            user.save()
           


            # Success message
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after successful registration

        else:
            # If form is invalid, show error messages
            messages.error(request, 'There was an error with your registration. Please try again.')

    else:
        form = createUserForm()  # Initialize an empty form if GET request

    return render(request, 'register.html', {'form': form})

def createfooditem(request):
    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'createfooditem.html', context)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customer
from .forms import *
from django.contrib.auth.forms import AuthenticationForm  # Assuming LoginForm is your form class

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Customer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import Customer
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

def loginPage(request):
    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({'message': 'No data provided'}, status=400)

            # Parse the JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username and password:
                # Authenticate the user
                user = authenticate(username=username, password=password)

                if user is not None:
                    # Log the user in
                    login(request, user)

                    # Check if the user is an admin
                    if user.is_staff:
                        # Redirect to the admin dashboard
                        return JsonResponse({
                            'message': 'Redirecting to admin dashboard...',
                            'redirect': '/admin_dashboard/',  # Provide full URL for admin dashboard
                        })
                    else:
                        # Redirect to the home page or user dashboard
                        return JsonResponse({
                            'message': 'Redirecting to home...',
                            'redirect': '/home/',  # Provide full URL for home page
                        })
                else:
                    return JsonResponse({'message': 'Invalid credentials'}, status=400)
            else:
                return JsonResponse({'message': 'Username and password are required'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    # Handle GET request: Render the login page
    return render(request, 'login.html')

def userpage(request):
    user = request.user
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = None
    exercises = Exercise.objects.filter(user=customer)
    total_exercise_calories = sum(exr.calorie for exr in exercises)
    exercise_count = exercises.count()

    food_items = FoodItem.objects.all()
    food_filter = FoodItemFilter(request.GET, queryset=food_items)
    filtered_food_items = food_filter.qs

    user_food_items = UserFooditem.objects.filter(customer=customer)
    food_count = user_food_items.count()

    final_food_items = []
    for food in user_food_items:
        final_food_items.extend(food.fooditem.all())

    total_food_calories = sum(food.calorie for food in final_food_items)
    calorie_limit = customer.calorie_limit
    net_calories = total_food_calories - total_exercise_calories
    calories_left = calorie_limit - net_calories

    context = {
        'Setlimit': calorie_limit,
        'CalorieLeft': calories_left,
        'totalCalories': net_calories,
        'foodlist': final_food_items,
        'fooditem': filtered_food_items,
        'myfilter': food_filter,
        'exercise': exercises,
        'etotal': total_exercise_calories,
        'ecnt': exercise_count,
        'food_count': food_count,
    }

    return render(request, 'user.html', context)

def viewresult(request):
    user = request.user
    cust = user.customer
    exercise = Exercise.objects.filter(user=cust)
    total_exercise_calories = sum(exr.calorie for exr in exercise)

    user_food_items = UserFooditem.objects.filter(customer=cust)
    querysetFood = []
    for food in user_food_items:
        querysetFood.append(food.fooditem.all())
    finalFoodItems = [food_item for items in querysetFood for food_item in items]

    total_food_calories = sum(foods.calorie for foods in finalFoodItems)
    net_calories = total_food_calories - total_exercise_calories
    calorie_limit = cust.calorie_limit
    CalorieLeft = calorie_limit - net_calories

    context = {
        'Setlimit': calorie_limit,
        'CalorieLeft': CalorieLeft,
        'totalCalories': total_food_calories,
        'foodlist': finalFoodItems,
        'exercise': exercise,
        'etotalCalories': total_exercise_calories,
    }
    return render(request, 'result.html', context)

def addFooditem(request):
    user = request.user
    cust = user.customer
    if request.method == "POST":
        form = addUserFooditem(request.POST)
        if form.is_valid():
            food_items = form.cleaned_data.get('fooditem_list')
            ufi, created = UserFooditem.objects.get_or_create(customer=cust)
            ufi.fooditem.add(*food_items)
            return redirect('home')
    form = addUserFooditem()
    context = {'form': form}
    return render(request, 'addUserFooditem.html', context)

def setcalorie(request):
    if request.method == 'POST':
        form = CalorieNeedsForm(request.POST)
        if form.is_valid():
            # Update the calorie_goal for the logged-in user
            customer = request.user.customer
            customer.calorie_goal = form.cleaned_data['calorie_goal']
            customer.save()

            messages.success(request, 'Your calorie goal has been updated successfully!')
            return redirect('home')  # Redirect to the homepage after updating the goal
    else:
        form = CalorieNeedsForm()

    return render(request, 'setcalorie.html')
@login_required
def set_calorie_goals(request):
    print("Request received. Method:", request.method)  # Debug log

    if request.method == 'POST':
        print("POST request received.")  # Debug log
        form = CalorieNeedsForm(request.POST)
        print("Form initialized.")  # Debug log

        if form.is_valid():
            print("Form validation passed.")  # Debug log
            try:
                # Extract data
                age = form.cleaned_data['age']
                height = form.cleaned_data['height']
                weight = form.cleaned_data['weight']
                activity_level = form.cleaned_data['activity_level']
                gender = form.cleaned_data['gender']
                goal = form.cleaned_data['goal']
                print(f"Form Data - Age: {age}, Height: {height}, Weight: {weight}, Activity Level: {activity_level},Gender: {gender}, Goal: {goal}")  # Debug log

                # Calculate calorie needs
                calorie_needs = calculate_calories(age, height, weight, activity_level,gender, goal)
                print(f"Calorie needs calculated: {calorie_needs}")  # Debug log

                # Update or create user profile
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                print(f"Profile for user {request.user.username}: Created={created}")  # Debug log
                user_profile.age = age
                user_profile.height = height
                user_profile.weight = weight
                user_profile.calorie_needs = calorie_needs
                user_profile.save()
                print("User profile updated.")  # Debug log

                messages.success(request, 'Your calorie goal has been updated successfully!')
                print("Redirecting to home.")  # Debug log
                return redirect('home')  # Redirect

            except Exception as e:
                print(f"Error during processing: {e}")  # Debug log
                messages.error(request, "An error occurred while processing your request.")
        else:
            print("Form validation failed. Errors:", form.errors)  # Debug log
            messages.error(request, "There were errors in your form submission.")
    else:
        print("GET request received.")  # Debug log

    form = CalorieNeedsForm()
    print("Rendering the form.") 
    print("Form POST data:",request.POST) # Debug log
    return render(request, 'set_calorie_goal.html', {'form': form})


def profilePage(request):
    return render(request, 'profile.html')

    
    

def check_calorie_needs(user):
    customer = user.customer  # Assuming there's a related `customer` field for the user
    daily_intake = customer.daily_intake if customer.daily_intake is not None else 0
    calorie_goal = customer.calorie_goal if customer.calorie_goal is not None else 'maintain'

    # Map calorie_goal to numeric values for comparison
    if calorie_goal == 'maintain':
        calorie_goal_value = 2000  # For example, assuming 2000 is the maintenance goal
    elif calorie_goal == 'lose':
        calorie_goal_value = 1500  # For example, assuming 1500 is the weight loss goal
    elif calorie_goal == 'gain':
        calorie_goal_value = 2500  # For example, assuming 2500 is the weight gain goal
    else:
        calorie_goal_value = 2000  # Default to 'maintain' if value is unexpected

    # Now perform the comparison
    if daily_intake > calorie_goal_value:
        feedback = "You need to reduce your daily intake."
    elif daily_intake < calorie_goal_value:
        feedback = "You need to increase your daily intake."
    else:
        feedback = "Your daily intake is on track."

    return feedback

def profile_view(request):
    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return HttpResponse("Customer not found", status=404)
    today = date.today()
    feedback = check_calorie_needs(customer, today)

    return render(request, 'profile.html', {'userprofile':customer, 'feedback': feedback})

def get_total_calories(customer, date):
    total_calories = Meal.objects.filter(customer=customer, date=date).aggregate(Sum('calories'))
    return total_calories['calories__sum'] or 0  # Return 0 if no meals recorded

def setexercise(request):
    if request.method == 'POST':
        form = addExercise(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user.customer
            exercise.save()
            return redirect('home')
    form = addExercise()
    context = {'form': form}
    return render(request, 'setexercise.html', context)

from .models import FoodItem
from .filters import FoodItemFilter

from django.shortcuts import render
from .models import FoodItem
from .filters import FoodItemFilter  # Ensure you have the correct filter class

def viewfood(request):
    # Fetch all FoodItem objects
    fooditems = FoodItem.objects.all()
    
    # Instantiate the filter with request GET data and the queryset
    myfilter = FoodItemFilter(request.GET, queryset=fooditems)
    
    # Get the filtered queryset
    filtered_fooditems = myfilter.qs
    
    # Context to pass to the template
    context = {
        'fooditems': fooditems,  # filtered food items
        'myfilter': myfilter,  # the filter instance to render in the template
    }
    
    return render(request, 'viewfood.html', context)

# Logout view
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def update_daily_intake(request):
    if request.method == "POST":
        intake = request.POST.get('daily_intake')
        customer = Customer.objects.get(user=request.user)
        customer.daily_intake = intake  # Update intake
        customer.save()
        return redirect('profile')

from django.shortcuts import render
from .forms import FoodIntakeForm
from .models import Customer
from .views import calculate_calories  # assuming you have a utility function for this

def food_intake_view(request):
    if request.method == 'POST':
        form = FoodIntakeForm(request.POST)
        if form.is_valid():
            # Get the current user
            user_profile = request.user.customer

            # Get the selected food items
            breakfast = form.cleaned_data['breakfast']
            lunch = form.cleaned_data['lunch']
            snacks = form.cleaned_data['snacks']
            dinner = form.cleaned_data['dinner']

            # Calculate total calories for the user based on their intake
            total_calories = breakfast.calorie + lunch.calorie + snacks.calorie + dinner.calorie

            # Calculate the calorie needs (based on the user's profile)
            calorie_needs = calculate_calories(user_profile.age, user_profile.gender, user_profile.activity_level)

            # Store the calculated intake for the user
            user_profile.calorie_intake = total_calories
            user_profile.calorie_needs = calorie_needs

            # Provide feedback based on the intake
            if total_calories > calorie_needs:
                user_profile.feedback = "You are exceeding your calorie goal!"
            elif total_calories < calorie_needs:
                user_profile.feedback = "You are under your calorie goal."
            else:
                user_profile.feedback = "You are meeting your calorie goal."

            # Save the updated user profile
            user_profile.save()

            return render(request, 'feedback.html', {'feedback': user_profile.feedback, 'calories': total_calories})

    else:
        form = FoodIntakeForm()

    return render(request, 'food_intake.html', {'form': form})
def food_list(request):
    fooditem = FoodItem.objects.all()
    return render(request, 'viewfood.html', {'fooditem': fooditem})

def preview_calorie_needs(request):
    calorie_needs = None

    if request.method == 'POST':
        form = CalorieNeedsForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            age = form.cleaned_data['age']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            activity_level = form.cleaned_data['activity_level']
            goal = form.cleaned_data['goal']

            # Calculate the calorie needs
            calorie_needs = calculate_calories(age, height, weight, activity_level, goal)

    else:
        form = CalorieNeedsForm()

    context = {
        'form': form,
        'calorie_needs': calorie_needs,  # Display the preview of calorie needs
    }

    return render(request, 'preview_calorie_needs.html', context)


@login_required
def preview_and_update_calorie_needs(request):
    user = request.user
    user_profile = None
    calorie_needs = None

    try:
        user_profile = UserProfile.objects.get(user=user)
        calorie_needs = user_profile.calorie_needs  # Retrieve current calorie needs
    except UserProfile.DoesNotExist:
        calorie_needs = None  # If no user profile exists, set calorie_needs to None

    if request.method == 'POST':
        form = CalorieNeedsForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            age = form.cleaned_data['age']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            activity_level = form.cleaned_data['activity_level']
            goal = form.cleaned_data['goal']

            # Calculate the calorie needs
            new_calorie_needs = calculate_calories(age, height, weight, activity_level, goal)

            context = {
                'form': form,
                'calorie_needs': new_calorie_needs,  # Display the updated calorie needs as preview
                'current_calorie_needs': calorie_needs,  # Show the current calorie needs
            }
            return render(request, 'preview_calorie_needs.html', context)
    else:
        form = CalorieNeedsForm()

    context = {
        'form': form,
        'calorie_needs': calorie_needs,  # Display the current calorie needs
    }
    
    return render(request, 'preview_calorie_needs.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def delete_user(request, user_id=None):
    if request.method == "POST":
        if user_id:  # Admin is deleting another user
            if request.user.is_staff:  # Check if the user is an admin
                user_to_delete = get_object_or_404(User, id=user_id)
                user_to_delete.delete()
                messages.success(request, f"User {user_to_delete.username} has been deleted successfully.")
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                messages.error(request, "You are not authorized to delete this user.")
                return redirect('home')  # Redirect to home if not admin
        else:  # Regular user deleting their own account
            user = request.user
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('login')  # Redirect to login page after account deletion

    else:  # If it's a GET request, show the confirmation page
        if user_id:  # Admin is deleting another user
            if request.user.is_staff:  # Check if the user is an admin
                user_to_delete = get_object_or_404(User, id=user_id)
                return render(request, 'delete_user.html', {'user': user_to_delete})
            else:
                messages.error(request, "You are not authorized to delete this user.")
                return redirect('home')  # Redirect to home if not admin
        else:  # Regular user deleting their own account
            return render(request, 'delete_user.html', {'user': request.user})  # Show confirmation for the current user

def admin_required(user):
    return user.is_staff

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    documents = Document.objects.all()
    users = UserProfile.objects.select_related('user').filter(user__is_staff=False)
    return render(request, 'admin_dashboard.html',{'users': users, 'documents':documents})


import jwt
from django.conf import settings
from django.http import JsonResponse

def some_protected_view(request):
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        return JsonResponse({'message': 'Unauthorized'}, status=401)
    
    try:
        # Decode the JWT token (assuming it's a JWT token)
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        # Proceed with your logic, knowing the token is valid
        # For example, you can access user info from the decoded token:
        user_id = decoded_token.get('user_id')
        # Perform the protected action, such as fetching user data
        # return JsonResponse({'message': 'Action successful'})
    
    except jwt.ExpiredSignatureError:
        return JsonResponse({'message': 'Token expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'message': 'Invalid token'}, status=401)

import os
from django.conf import settings
import os
import openpyxl
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from .models import UserProfile 
from .utils import * # Adjust import as per your model location

from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.core.management import call_command
import os
from .management.commands.download_customer_details import Command as DownloadCustomerDetailsCommand

def download_customer_details(request):
    if not request.user.is_staff:
        return redirect('home')

    
    # Define the path to the Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, 'customer_details.xlsx')


    if not os.path.exists(file_path):
        return HttpResponse("Excel file not found.",status=404)
    # Set HTTP response to serve the Excel file for download
    return FileResponse(open(file_path,'rb'), as_attachment=True,filename='customer_details.xlsx')

from django.shortcuts import render
from .models import Document

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Replace with your desired success URL
    else:
        form = DocumentForm()

    return render(request, 'upload_document.html', {'form': form})


from django.http import FileResponse
def pdf_download(request):
    # Fetch the documents from the database
    documents = Document.objects.all()
    
    context = {
        'documents': documents,
    }
    
    return render(request, 'pdf_download.html', context)

def auto_download_page(request):
    return render(request, 'auto_download.html')