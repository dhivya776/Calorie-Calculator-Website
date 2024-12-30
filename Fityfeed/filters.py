import django_filters
from .models import FoodItem

class FoodItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Food Name')
    category = django_filters.CharFilter(lookup_expr='icontains', label='Category')  # Assuming a category field
    calories = django_filters.NumberFilter(lookup_expr='lte', label='Calories')  # Filter by calorie limit

    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'calories']
