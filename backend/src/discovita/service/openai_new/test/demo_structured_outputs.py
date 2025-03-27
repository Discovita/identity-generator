#!/usr/bin/env python3
"""
Demo Script for Structured Outputs with OpenAI

This script demonstrates how to use the structured outputs feature
of the OpenAI client to get typed, structured responses using Pydantic models.
"""

import json
import os
from typing import List, Optional

# Import the OpenAIClient from our package
from discovita.service.openai_new import AIModel, OpenAIClient
from pydantic import BaseModel, Field

# Get API key from environment (for security)
# In production, use environment variables or a secure vault
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("Please set the OPENAI_API_KEY environment variable")
    print("Example: export OPENAI_API_KEY=your-api-key")
    exit(1)


# Define Pydantic models for structured output
class RecipeIngredient(BaseModel):
    """
    Represents a single ingredient in a recipe.
    """

    name: str = Field(description="The name of the ingredient")
    quantity: str = Field(description="The quantity of the ingredient (e.g., '2 cups')")
    optional: bool = Field(
        description="Whether the ingredient is optional", default=False
    )


class Recipe(BaseModel):
    """
    Represents a recipe with title, ingredients, and preparation steps.
    """

    title: str = Field(description="The title of the recipe")
    description: str = Field(description="A brief description of the recipe")
    ingredients: List[RecipeIngredient] = Field(description="The list of ingredients")
    preparation_steps: List[str] = Field(
        description="The step-by-step preparation instructions"
    )
    prep_time_minutes: int = Field(description="Preparation time in minutes")
    cooking_time_minutes: int = Field(description="Cooking time in minutes")
    servings: int = Field(description="Number of servings the recipe yields")
    tips: List[str] = Field(description="Cooking tips (can be empty if none)")


def main():
    """
    Main function to demonstrate structured outputs.
    """
    # Print which models support structured outputs
    print("Models that support structured outputs:")
    for model in ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o1-mini"]:
        supports = AIModel.supports_structured_outputs(model)
        print(f"  {model}: {supports}")
    print()

    # Initialize the OpenAI client
    client = OpenAIClient(
        api_key=API_KEY, organization=os.environ.get("OPENAI_ORG_ID")  # Optional
    )

    # Create messages for the prompt
    # Using system message to improve the quality of the response
    system_message = (
        "You are a professional chef who creates delicious, easy-to-follow recipes. "
        "Provide detailed recipes with accurate ingredient measurements and clear steps."
    )

    # User's request for a recipe
    user_prompt = "Create a recipe for a quick vegetarian pasta dish using ingredients commonly found in most kitchens."

    print(f"Requesting recipe with prompt: '{user_prompt}'")
    print("This might take a few seconds...\n")

    try:
        # Call the create_structured_chat_completion method
        # This will return a parsed object of the Recipe type
        result = client.create_structured_chat_completion(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            model="gpt-4o",  # Using GPT-4o which supports structured outputs
            response_format=Recipe,
            # Parameters for generation quality
            temperature=0.7,
            max_completion_tokens=2000,
        )

        # Access the parsed model from the result
        recipe = result.choices[0].message.parsed

        # Display the recipe in a formatted way
        print("\n" + "=" * 50)
        print(f"## {recipe.title} ##")
        print("=" * 50)
        print(f"\nDescription: {recipe.description}")
        print(f"\nPrep Time: {recipe.prep_time_minutes} minutes")
        print(f"Cooking Time: {recipe.cooking_time_minutes} minutes")
        print(f"Servings: {recipe.servings}")

        print("\nIngredients:")
        for i, ingredient in enumerate(recipe.ingredients, 1):
            optional_text = " (optional)" if ingredient.optional else ""
            print(f"  {i}. {ingredient.quantity} {ingredient.name}{optional_text}")

        print("\nPreparation Steps:")
        for i, step in enumerate(recipe.preparation_steps, 1):
            print(f"  {i}. {step}")

        if recipe.tips:
            print("\nTips:")
            for i, tip in enumerate(recipe.tips, 1):
                print(f"  {i}. {tip}")

        # Also show the raw JSON
        print("\nRaw JSON output:")
        print(json.dumps(recipe.model_dump(), indent=2))

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if your OpenAI API key is valid")
        print("2. Ensure you're using a model that supports structured outputs")
        print("3. Check your internet connection")
        print("4. Make sure your OpenAI account has access to the specified model")

        # Additional guidance for schema-related errors
        error_msg = str(e).lower()
        if "schema" in error_msg or "response_format" in error_msg:
            print("\nSchema-specific troubleshooting:")
            print("- Pydantic models must follow OpenAI's JSON Schema restrictions:")
            print("  • Avoid using 'default' values in optional fields")
            print(
                "  • Use required fields with empty lists/values instead of Optional fields"
            )
            print("  • Keep model structure simple and avoid complex nested types")
            print("  • Ensure all field types are compatible with JSON Schema")


if __name__ == "__main__":
    main()
