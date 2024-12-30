import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calorieCalc.settings')
django.setup()
import csv
from django.core.management.base import BaseCommand
from Fityfeed.models import FoodItem

class Command(BaseCommand):
    help = 'Import food items from a CSV file into the database'

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        file_path = 'media/food_items.csv'  # Adjust path as needed

        # Open the CSV file
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            
            # Loop through each row and create a FoodItem
            for row in reader:
                FoodItem.objects.create(
                    name=row['FoodItem'],
                    calories=row['Calories'],
                    carbohydrate=row['Carbs'],
                    fats=row['Fats'],
                    protein=row['Proteins']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported food items'))
