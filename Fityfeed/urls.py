from django.urls import path, include
from django.shortcuts import redirect
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',lambda request: redirect('login')),
    path('login/',views.loginPage,name='login'),
    path('home/', views.home, name='home'),
    path('fooditem/', views.fooditem, name='fooditem'),
    path('register/', views.registerPage, name='register'),
    path('createfooditem/', views.createfooditem, name='createfooditem'),
    path('login/', views.loginPage, name='login'),
    path('user/', views.userpage, name='user'),
    path('viewresult/', views.viewresult, name='viewresult'),
    path('addFooditem/', views.addFooditem, name='addFooditem'),
    path('setcalorie/', views.setcalorie, name='setcalorie'),
    path('set_calorie_goals/', views.set_calorie_goals, name='set_calorie_goals'),
    path('profile/', views.profilePage, name='profile'),
    path('food-items/', views.food_list, name='food_list'),
    path('viewfood/', views.food_list, name='viewfood'),
    path('logout/', views.logoutUser, name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('download_customer_details/',download_customer_details,name='download_customer_details'),
    path('documents/', document_list, name='document_list'),
    path('upload_document/',upload_document, name='upload_document'),
    path('download_pdfs/',pdf_download, name='pdf_download'),
    path('auto_download/',auto_download_page,name='auto_download'),
]


if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
