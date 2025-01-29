from rest_framework import serializers
from ahaar.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'image_url', 'description', 'cuisine', 'course', 'diet', 'prep_time', 'ingredients', 'instructions']
