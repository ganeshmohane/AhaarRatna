from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.TextField()
    cuisine = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)
    prep_time = models.CharField(max_length=100)  # You could use IntegerField for time if you want to store time in minutes
    ingredients = models.TextField()  # Assuming ingredients are stored as plain text, you could split into multiple fields if necessary
    instructions = models.TextField()

    def __str__(self):
        return self.name