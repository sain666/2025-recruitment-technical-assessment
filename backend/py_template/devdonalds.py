from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:

	recipeName = recipeName.replace('-', ' ').replace('_', ' ')
	recipeName = re.sub(r'[^a-zA-Z\s]', '', recipeName)
	recipeName = re.sub(r'\s+', ' ', recipeName).strip()
	recipeName = recipeName.title()
	if not recipeName:
		return None
	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	try:
		entry = request.get_json()
		if entry.get("type") not in ["recipe", "ingredient"]:
			return jsonify({"error": 'Type must be "recipe" or "ingredient"'}), 400
		name = entry.get("name")
		if name in cookbook:
			return jsonify({"error": "Entry name must be unique"}), 400
		if entry["type"] == "ingredient":
			cook_time = entry.get("cookTime")
			if cook_time is None or cook_time < 0:
				return jsonify({"error": "cookTime must be greater than or equal to 0"}), 400
		if entry["type"] == "recipe":
			required_items = entry.get("requiredItems")
			if not isinstance(required_items, list):
				return jsonify({"error": "requiredItems must be a list"}), 400
			required_item_names = set()
			for item in required_items:
				if "name" not in item or "quantity" not in item:
					return jsonify({"error": "Each requiredItem must have 'name' and 'quantity' fields"}), 400
				item_name = item["name"]
				if item_name in required_item_names:
					return jsonify({"error": f"Duplicate required item name: {item_name}"}), 400
				required_item_names.add(item_name)
		
		cookbook[name] = entry
		return '', 200

	except Exception as e:
		return jsonify({"error": str(e)}), 400


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name

def get_recipe_summary(recipe_name):
    if recipe_name not in cookbook:
        return None
    entry = cookbook[recipe_name]
    if entry["type"] == "recipe":
        base_ingredients = []
        total_cook_time = 0
        for item in entry["requiredItems"]:
            ingredient_name = item["name"]
            ingredient = cookbook.get(ingredient_name)
            if ingredient:
                if ingredient["type"] == "recipe":
                    ingredient_summary = get_recipe_summary(ingredient_name)
                    if ingredient_summary:
                        base_ingredients.extend(ingredient_summary["ingredients"])
                        total_cook_time += ingredient_summary["cookTime"]
                else:
                    base_ingredients.append({
                        "name": ingredient_name,
                        "quantity": item["quantity"]
                    })
                    total_cook_time += ingredient["cookTime"]

        return {
            "name": entry["name"],
            "cookTime": total_cook_time,
            "ingredients": base_ingredients
        }
    return None


@app.route('/summary', methods=['GET'])
def summary():
	recipe_name = request.args.get("name")
	summary = get_recipe_summary(recipe_name)
	if summary:
		return jsonify(summary)
	else:
		return jsonify({"error": "Recipe not found"}), 404


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
