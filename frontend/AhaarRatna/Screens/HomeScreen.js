import React, { useState, useEffect } from 'react';
import { View, Text, Image, TextInput, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { API_BASE_URL } from '../Context/config';
import { Ionicons } from '@expo/vector-icons';
import { MenuProvider } from 'react-native-popup-menu';

export default function HomeScreen() {
  const [recipes, setRecipes] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/api/recipes/`)
      .then((response) => response.json())
      .then((data) => setRecipes(data))
      .catch((error) => console.error('Error fetching recipes:', error))
      .finally(() => setLoading(false));
  };

  const handleSearch = () => {
    setLoading(true);
    fetch(`${API_BASE_URL}/api/recommend/?search=${searchQuery}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data,'data')
        setRecipes(data);
      })
      .catch((error) => console.error('Error fetching recipes:', error))
      .finally(() => setLoading(false));
  };
  

  const filteredRecipes = recipes.filter((recipe) => {
    const matchesFilter = filter ? recipe.diet === filter : true;
    const matchesSearch = searchQuery
      ? recipe.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        recipe.ingredients.toLowerCase().includes(searchQuery.toLowerCase())
      : true;
    return matchesFilter && matchesSearch;
  });

  const handleRecipePress = (recipe) => {
    navigation.navigate('Recipe', { recipe });
  };

  const renderRecipeItem = ({ item }) => (
    <TouchableOpacity onPress={() => handleRecipePress(item)} style={styles.recipeBox}>
      <Image source={{ uri: item.image_url }} style={styles.recipeImage} />
      <Text style={styles.recipeName}>{item.name}</Text>
      <Text style={styles.recipeType}>{item.cuisine}</Text>
    </TouchableOpacity>
  );

  return (
    <MenuProvider>
      <View style={styles.container}>
        <Image source={require('../assets/logo.png')} style={styles.logo} />
        <Text style={styles.subtitle}>An App that recommends traditional Indian recipes...</Text>

        <View style={styles.searchFilterRow}>
          <View style={styles.searchContainer}>
            <TextInput
              style={styles.searchBox}
              placeholder="Search item name or Ingredients"
              value={searchQuery}
              onChangeText={setSearchQuery}
            />
            <TouchableOpacity onPress={handleSearch} style={styles.searchIconContainer}>
              <Ionicons name="search" size={20} color="#333" />
            </TouchableOpacity>
          </View>
        </View>

        {loading ? (
          <ActivityIndicator size="large" color="#333" style={{ marginTop: 20 }} />
        ) : (
          <FlatList
            data={recipes.filter((recipe) => {
              const matchesFilter = filter ? recipe.diet === filter : true;
              const matchesSearch = searchQuery
                ? recipe.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                  recipe.ingredients.toLowerCase().includes(searchQuery.toLowerCase())
                : true;
              return matchesFilter && matchesSearch;
            })}
            renderItem={renderRecipeItem}
            keyExtractor={(item, index) => `${item.id || index}`}
            numColumns={2}
            contentContainerStyle={styles.recipeList}
          />
        )}
      </View>
    </MenuProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 16,
  },
  logo: {
    width: 200,
    height: 180,
    alignSelf: 'center',
    marginBottom: -90,
  },
  subtitle: {
    marginTop: 70,
    marginBottom: 20,
  },
  searchFilterRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  searchContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  searchBox: {
    flex: 1,
    padding: 10,
  },
  searchIconContainer: {
    padding: 10,
  },
  recipeList: {
    paddingBottom: 16,
  },
  recipeBox: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    margin: 8,
    borderRadius: 8,
    alignItems: 'center',
    padding: 12,
  },
  recipeImage: {
    width: '100%',
    height: 100,
    borderRadius: 8,
    marginBottom: 8,
  },
  recipeName: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  recipeType: {
    fontSize: 14,
    color: '#666',
  },
});
