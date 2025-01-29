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

# New Recommendation
@api_view(['GET'])
def recommend_recipes(request):
    query = request.GET.get('search', '').strip()
    print('got query', query)
    
    if not query:
        return Response({"message": "No query provided."}, status=400)

    try:
        # Access pickle files and data from the app configuration
        ahaar_app = apps.get_app_config('ahaar')
        data = ahaar_app.data
        similarity = ahaar_app.similarity

        # Convert query to lowercase to match similar behavior as .lower() in pandas
        query_lower = query.lower()

        # Use regex for case-insensitive search with contains behavior
        matching_recipes = Recipe.objects.filter(name__regex=r'(?i)' + query_lower)  # Case-insensitive regex match
        print("Matching Recipes:", matching_recipes)
        
        if not matching_recipes.exists():
            return Response({"message": f"No recipes found for '{query}'."}, status=404)

        # Search for exact match (case-insensitive)
        exact_match_recipes = Recipe.objects.filter(name__iexact=query)  # Case-insensitive exact match
        print("Exact Match Recipes:", exact_match_recipes)

        # If there's an exact match, we will add it to the top of the recommendations
        recommended_recipes = matching_recipes

        if exact_match_recipes.exists():
            # If exact match exists, return exact match first followed by similar recipes
            recommended_recipes = exact_match_recipes | matching_recipes

        # Use the first matching recipe as the base for recommendations if no exact match
        reference_recipe = matching_recipes.first() if not exact_match_recipes.exists() else exact_match_recipes.first()
        recipe_index = data[data['name'] == reference_recipe.name].index[0]

        # Calculate similarity scores and sort
        distances = similarity[recipe_index]
        dish_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

        # Fetch recommended dish names based on similarity
        recommended_dish_names = [data.iloc[i[0]]['name'] for i in dish_indices]
        recommended_recipes |= Recipe.objects.filter(name__in=recommended_dish_names)
        
        # Serialize and return the recommended recipes
        serializer = RecipeSerializer(recommended_recipes, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({"message": f"Error processing recommendation: {str(e)}"}, status=500)

"""def recommend(dish_name):
    dish_name = dish_name.lower()  # Convert input to lowercase

    # Find dishes that contain the search term
    matching_dishes = df[df['name'].str.lower().str.contains(dish_name, regex=True, na=False)]

    if matching_dishes.empty:
        print("❌ No matching dishes found. Try different keywords.")
        return

    recommended_dishes = set()  # To store unique recommendations

    print("\n🔍 *Matching Dishes:*")
    for idx in matching_dishes.index:
        print(f"✅ {df.loc[idx, 'name']}")  # Show matched dishes

        # Get top 5 similar dishes for each matched dish
        distances = similarity[idx]
        dish_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Top 5 excluding itself

        for i in dish_list:
          # Check if the index is within the valid range of the DataFrame index
          if i[0] in df.index:
            recommended_dishes.add(df.loc[i[0], 'name'])  # Add to recommendations

    if recommended_dishes:
        print("\n✨ *Recommended Similar Dishes:*")
        for dish in recommended_dishes:
            print(f"🔹 {dish}")"""