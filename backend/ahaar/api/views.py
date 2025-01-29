from rest_framework.response import Response
from rest_framework.decorators import api_view
from ahaar.models import Recipe
from .serializers import RecipeSerializer
from ahaar.apps import AhaarConfig
from django.apps import apps


# Get all recipes
@api_view(['GET'])
def get_recipes(request):
    # Query the first 5 recipes from the database
    recipes = Recipe.objects.all()[:10]
    serializer = RecipeSerializer(recipes, many=True)
    print(serializer)
    return Response(serializer.data)


# Search
@api_view(['GET'])
def search_recipes(request):
    query = request.GET.get('search', '')
    if query:
        results = Recipe.objects.filter(name__icontains=query) | Recipe.objects.filter(ingredients__icontains=query)
        serialized_data = RecipeSerializer(results, many=True)
        return Response(serialized_data.data)
    return Response({"message": "No query provided or no results found."}, status=400)

@api_view(['GET'])
def recommend_recipes(request):
    query = request.GET.get('search', '').strip()
    print('got query',query)
    if not query:
        return Response({"message": "No query provided."}, status=400)

    try:
        # Access pickle files and data from the app configuration
        ahaar_app = apps.get_app_config('ahaar')
        data = ahaar_app.data
        similarity = ahaar_app.similarity

        # Check if the query dish exists in the database
        matching_recipes = Recipe.objects.filter(name__icontains=query)
        if not matching_recipes.exists():
            return Response({"message": f"No recipes found for '{query}'."}, status=404)

        # Use the first matching recipe as the base for recommendations
        reference_recipe = matching_recipes.first()
        recipe_index = data[data['name'] == reference_recipe.name].index[0]

        # Calculate similarity scores and sort
        distances = similarity[recipe_index]
        dish_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

        # Fetch IDs of recommended dishes
        recommended_dish_names = [data.iloc[i[0]]['name'] for i in dish_indices]
        recommended_recipes = Recipe.objects.filter(name__in=recommended_dish_names)
        print(recommend_recipes,'here')
        # if not recommended_recipes.exists():
        #     return Response({"message": "No matching recipes found in the database."}, status=404)

        # Serialize and return the recommended recipes
        serializer = RecipeSerializer(recommended_recipes, many=True)
        print(serializer)
        return Response(serializer.data)

    except Exception as e:
        return Response({"message": f"Error processing recommendation: {str(e)}"}, status=500)

# # Recommendation based on search
# @api_view(['GET'])
# def recommend_recipes(request):
#     query = request.GET.get('search', '')
#     print(query)
#     if not query:
#         return Response({"message": "No query provided."}, status=400)

#     try:
#         # Access loaded pickle files
#         ahaar_app = apps.get_app_config('ahaar')
#         data = ahaar_app.data
#         similarity = ahaar_app.similarity
#         print(ahaar_app,data,similarity)

#         # Check if the query exists in the data
#         if query not in data['name'].values:
#             return Response({"message": f"No recommendations found for '{query}'."}, status=404)

#         # Find recommendations
#         dish_index = data[data['name'] == query].index[0]
#         distances = similarity[dish_index]
#         dish_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

#         recommendations = [data.iloc[i[0]]['name'] for i in dish_list]

#         # Optionally filter recommendations from Recipe database
#         from ahaar.models import Recipe
#         from .serializers import RecipeSerializer
#         recommended_recipes = Recipe.objects.filter(name__in=recommendations)
#         serializer = RecipeSerializer(recommended_recipes, many=True)

#         return Response(serializer.data)

#     except Exception as e:
#         return Response({"message": f"Error processing recommendation: {str(e)}"}, status=500)


# Search
# @api_view(['GET'])
# def search_recipes(request):
#     query = request.GET.get('search', '')
#     if query:
#         results = Recipe.objects.filter(name__icontains=query) | Recipe.objects.filter(ingredients__icontains=query)
#         serialized_data = RecipeSerializer(results, many=True)
#         return Response(serialized_data.data)
#     return Response({"message": "No query provided or no results found."}, status=400)

