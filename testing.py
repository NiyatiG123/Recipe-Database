#docstring - Niyati Gupta - cooking database application
import sqlite3

# Connect to the database (creates recipes.db if it doesn't exist)
connection = sqlite3.connect("recipes.db")
cursor = connection.cursor()

# Create categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
)
""")

# Create recipes table
cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    method TEXT NOT NULL,
    cooking_time INTEGER NOT NULL,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
)
""")

# Default categories
default_categories = [
    (1, "Breakfast"),
    (2, "Lunch"),
    (3, "Dinner"),
    (4, "Dessert"),
    (5, "Snacks"),
    (6, "Drinks")
]

# Default recipes
default_recipes = [
    (1, "Pancakes", "Flour, Milk, Eggs, Sugar", "Mix ingredients, cook in pan until golden.", 15, 1),
    (2, "Chicken Pasta", "Pasta, Chicken, Cream, Garlic", "Cook pasta, fry chicken, mix with sauce.", 30, 3),
    (3, "Chocolate Brownies", "Chocolate, Flour, Butter, Eggs", "Mix ingredients and bake in oven.", 40, 4),
    (4, "Fruit Smoothie", "Banana, Strawberries, Milk", "Blend all ingredients together.", 5, 6),
    (5, "Grilled Cheese Toastie", "Bread, Cheese, Butter", "Butter bread, add cheese, toast until golden.", 10, 2),
    (6, "Nachos", "Corn Chips, Cheese, Salsa", "Layer ingredients and bake.", 20, 5),
    (7, "Caesar Salad", "Lettuce, Chicken, Croutons, Dressing", "Mix all ingredients in bowl.", 15, 2),
    (8, "Omelette", "Eggs, Cheese, Ham", "Cook eggs in pan and add fillings.", 10, 1),
    (9, "Beef Stir Fry", "Beef, Vegetables, Soy Sauce", "Stir fry ingredients in pan.", 25, 3),
    (10, "Cookies", "Flour, Sugar, Chocolate Chips", "Mix ingredients and bake.", 25, 4)
]

# Insert categories - OR IGNORE prevents duplicates if program is run again
cursor.executemany("INSERT OR IGNORE INTO categories VALUES (?, ?)", default_categories)

# Insert recipes - OR IGNORE prevents duplicates if program is run again
cursor.executemany("INSERT OR IGNORE INTO recipes VALUES (?, ?, ?, ?, ?, ?)", default_recipes)

# Save all changes to the database
connection.commit()

# ---- CONSTANTS ----
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6"]
MIN_COOKING_TIME = 1

# ---- DISPLAY CATEGORIES ----
def display_categories():
    # Fetch and display all categories from the database
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    print("\n--- Categories ---")
    for category in categories:
        print(f"{category[0]}. {category[1]}")

# ---- VIEW RECIPES ----
def view_recipes():
    # Join recipes and categories tables so category name shows instead of just a number
    cursor.execute("""
        SELECT recipe_name, ingredients, method, cooking_time, category_name
        FROM recipes
        JOIN categories ON recipes.category_id = categories.category_id
    """)
    recipes = cursor.fetchall()
    
    if len(recipes) == 0:
        print("\nNo recipes found.")
    else:
        print("\n--- All Recipes ---")
        for recipe in recipes:
            print(f"\nName: {recipe[0]}")
            print(f"Ingredients: {recipe[1]}")
            print(f"Method: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Category: {recipe[4]}")
            print("-" * 30)

# ---- MAIN MENU ----
def main_menu():
    print("\n=== Recipe Manager ===")
    print("1. View all recipes")
    print("2. Add a recipe")
    print("3. Search for a recipe")
    print("4. Delete a recipe")
    print("5. Sort recipes by cooking time")
    print("6. Exit")

# ---- MAIN LOOP ----
while True:
    main_menu()
    choice = input("Enter your choice: ").strip()
    
    # Validate menu choice
    if choice not in MENU_OPTIONS:
        print("Invalid choice. Please enter a number between 1 and 6.")
    elif choice == "1":
        view_recipes()
    elif choice == "2":
        print("Coming soon.")
    elif choice == "3":
        print("Coming soon.")
    elif choice == "4":
        print("Coming soon.")
    elif choice == "5":
        print("Coming soon.")
    elif choice == "6":
        print("Goodbye!")
        connection.close()
        break