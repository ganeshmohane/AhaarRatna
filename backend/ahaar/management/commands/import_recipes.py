import csv
from django.core.management.base import BaseCommand
from ahaar.models import Recipe

class Command(BaseCommand):
    help = 'Import recipes from CSV file'

    def handle(self, *args, **kwargs):
        with open('cuisines.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Recipe.objects.create(
                    name=row['name'],
                    image_url=row['image_url'],
                    description=row['description'],
                    cuisine=row['cuisine'],
                    course=row['course'],
                    diet=row['diet'],
                    prep_time=row['prep_time'],
                    ingredients=row['ingredients'],
                    instructions=row['instructions']
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported recipes'))
