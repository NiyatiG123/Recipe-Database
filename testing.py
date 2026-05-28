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
MAX_CATEGORY_ID = 6

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
            print(f"method: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Category: {recipe[4]}")
            print("-" * 30)

# ---- ADD RECIPE ----
def add_recipe():
    print("\n--- Add a Recipe ---")
    
    # Get recipe name and validate it is not empty
    recipe_name = input("Enter recipe name: ").strip()
    if len(recipe_name) == 0:
        print("Recipe name cannot be empty.")
        return
    
    # Get ingredients and validate not empty
    ingredients = input("Enter ingredients (comma separated): ").strip()
    if len(ingredients) == 0:
        print("Ingredients cannot be empty.")
        return
    
    # Get method and validate not empty
    method = input("Enter method: ").strip()
    if len(method) == 0:
        print("method cannot be empty.")
        return
    
    # Get cooking time and validate it is a number above minimum
    cooking_time = input("Enter cooking time in minutes: ").strip()
    if cooking_time.isdigit() == False:
        print("Cooking time must be a number.")
        return
    cooking_time = int(cooking_time)
    if cooking_time < MIN_COOKING_TIME:
        print(f"Cooking time must be at least {MIN_COOKING_TIME} minute.")
        return
    
    # Show categories and get valid category choice
    display_categories()
    category_id = input("Enter category number: ").strip()
    if category_id.isdigit() == False:
        print("Invalid category.")
        return
    category_id = int(category_id)
    if category_id not in range(1, MAX_CATEGORY_ID + 1):
        print("Invalid category number.")
        return
    
    # Insert recipe into database
    cursor.execute("""
        INSERT INTO recipes (recipe_name, ingredients, method, cooking_time, category_id)
        VALUES (?, ?, ?, ?, ?)
    """, (recipe_name, ingredients, method, cooking_time, category_id))
    connection.commit()
    print("Recipe added successfully!")

# ---- SEARCH RECIPE ----
def search_recipe():
    print("\n--- Search Recipes ---")
    
    # Get search term and validate not empty
    search_term = input("Enter recipe name to search: ").strip()
    if len(search_term) == 0:
        print("Search term cannot be empty.")
        return
    
    # Search database using LIKE to find partial matches
    cursor.execute("""
        SELECT recipe_name, ingredients, method, cooking_time, category_name
        FROM recipes
        JOIN categories ON recipes.category_id = categories.category_id
        WHERE recipe_name LIKE ?
    """, ("%" + search_term + "%",))
    
    results = cursor.fetchall()
    
    if len(results) == 0:
        print("No recipes found.")
    else:
        print(f"\n--- Results for '{search_term}' ---")
        for recipe in results:
            print(f"\nName: {recipe[0]}")
            print(f"Ingredients: {recipe[1]}")
            print(f"method: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Category: {recipe[4]}")
            print("-" * 30)


# ---- DELETE RECIPE ----
def delete_recipe():
    print("\n--- Delete a Recipe ---")
    
    # Show all recipes first so user knows what to delete
    view_recipes()
    
    # Get recipe name to delete
    recipe_name = input("\nEnter the name of the recipe to delete: ").strip()
    if len(recipe_name) == 0:
        print("Recipe name cannot be empty.")
        return
    
    # Check if recipe exists before deleting
    cursor.execute("SELECT * FROM recipes WHERE recipe_name = ? COLLATE NOCASE", (recipe_name,))
    recipe = cursor.fetchone()
    
    if recipe is None:
        print("Recipe not found.")
        return
    
    # Delete the recipe permanently
    cursor.execute("DELETE FROM recipes WHERE recipe_name = ? COLLATE NOCASE", (recipe_name,))
    connection.commit()
    print(f"{recipe_name} deleted successfully!")

# ---- SORT RECIPES ----
def sort_recipes():
    print("\n--- Sort Recipes ---")
    print("1. Shortest cooking time first")
    print("2. Longest cooking time first")
    
    sort_choice = input("Enter choice: ").strip()
    
    # Validate sort choice
    if sort_choice not in ["1", "2"]:
        print("Invalid choice.")
        return
    
    # Sort ascending or descending based on user choice
    if sort_choice == "1":
        cursor.execute("""
            SELECT recipe_name, ingredients, method, cooking_time, category_name
            FROM recipes
            JOIN categories ON recipes.category_id = categories.category_id
            ORDER BY cooking_time ASC
        """)
        print("\n--- Recipes by Shortest Cooking Time ---")
    else:
        cursor.execute("""
            SELECT recipe_name, ingredients, method, cooking_time, category_name
            FROM recipes
            JOIN categories ON recipes.category_id = categories.category_id
            ORDER BY cooking_time DESC
        """)
        print("\n--- Recipes by Longest Cooking Time ---")
    
    recipes = cursor.fetchall()
    for recipe in recipes:
        print(f"\nName: {recipe[0]}")
        print(f"Ingredients: {recipe[1]}")
        print(f"method: {recipe[2]}")
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
        add_recipe()
    elif choice == "3":
        search_recipe()
    elif choice == "4":
        delete_recipe()
    elif choice == "5":
        sort_recipes()
    elif choice == "6":
        print("Goodbye!")
        connection.close()
        break
