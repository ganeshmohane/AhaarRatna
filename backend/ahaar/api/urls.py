from django.urls import path
from .views import (
    get_recipes,
    search_recipes,
    recommend_recipes,
 )
urlpatterns = [

    # API Endpoints
    path('recipes/', get_recipes, name='get_recipes'),
    path('search/', search_recipes, name='search_recipes'),
    path('recommend/', recommend_recipes, name='recommend_recipes'),
]