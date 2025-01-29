import React from 'react';
import { View, Text, Image, StyleSheet, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';

export default function RecipeScreen({ route }) {
  const { recipe } = route.params;
  // console.log(recipe)
  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView style={styles.container}>
        <Image source={{ uri: recipe.image_url }} style={styles.recipeImage} />

        <View style={styles.headerSection}>
          <Text style={styles.recipeName}>{recipe.name}</Text>
          <View style={styles.infoRow}>
            <View style={[styles.tagBox, { backgroundColor: recipe.diet === 'Vegetarian' ? '#d4edda' : '#f8d7da' }]}>
              <Text style={[styles.tagText, { color: recipe.diet === 'Vegetarian' ? '#155724' : '#721c24' }]}> {recipe.diet} </Text>
            </View>
            <View style={styles.tagBox}>
              <Text style={styles.tagText}>#{recipe.cuisine}</Text>
            </View>
          </View>
        </View>

        <Text style={styles.sectionTitle}>Description</Text>
        <Text style={styles.recipeDescription}>{recipe.description}</Text>

        <Text style={styles.sectionTitle}>Ingredients</Text>
        {recipe.ingredients.split('\n').filter(line => line.trim()).map((ingredient, index) => (
          <View key={index} style={styles.bulletPointContainer}>
            <Text style={styles.bulletPoint}>{'\u2022'}</Text>
            <Text style={styles.ingredientText}>{ingredient.trim()}</Text>
          </View>
        ))}

        <Text style={styles.sectionTitle}>Instructions</Text>
        {recipe.instructions.split('\n').filter(line => line.trim()).map((instruction, index) => (
          <View key={index} style={styles.bulletPointContainer}>
            <Text style={styles.bulletPoint}>{'\u2022'}</Text>
            <Text style={styles.instructionText}>{instruction.trim()}</Text>
          </View>
        ))}

        <Text style={styles.sectionTitle}>Time required {recipe.prep_time}</Text>
        <Text></Text>
        <Text></Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 16,
  },
  recipeImage: {
    width: '100%',
    height: 250,
    borderRadius: 8,
    marginBottom: 16,
  },
  headerSection: {
    marginBottom: 16,
  },
  recipeName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  tagBox: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  tagText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 16,
    marginBottom: 8,
  },
  recipeDescription: {
    fontSize: 16,
    marginBottom: 16,
  },
  bulletPointContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 0,
  },
  bulletPoint: {
    fontSize: 16,
    lineHeight: 24,
    marginRight: 8,
  },
  ingredientText: {
    fontSize: 16,
    flex: 1,
  },
  instructionText: {
    fontSize: 16,
    flex: 1,
  },
});
