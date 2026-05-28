#docstring - Niyati Gupta - cooking database application
import sqlite3

# Connect to the database - creates recipes.db file if it doesn't already exist
connection = sqlite3.connect("recipes.db")

# Cursor acts as a messenger between Python and the database - used to run SQL commands
cursor = connection.cursor()

# Create categories table - IF NOT EXISTS prevents errors if table already exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
)
""")

# Create recipes table - AUTOINCREMENT automatically gives each recipe a unique ID
cursor.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    method TEXT NOT NULL,
    cooking_time INTEGER NOT NULL,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
    -- FOREIGN KEY links recipes to categories table ensuring every recipe has a valid category
)
""")

# Default categories stored as a list of tuples ready to insert into database
default_categories = [
    (1, "Breakfast"),
    (2, "Lunch"),
    (3, "Dinner"),
    (4, "Dessert"),
    (5, "Snacks"),
    (6, "Drinks")
]

# Default recipes stored as a list of tuples ready to insert into database
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

# OR IGNORE prevents duplicate categories being added if the program is run multiple times
cursor.executemany("INSERT OR IGNORE INTO categories VALUES (?, ?)", default_categories)

# OR IGNORE prevents duplicate recipes being added if the program is run multiple times
cursor.executemany("INSERT OR IGNORE INTO recipes VALUES (?, ?, ?, ?, ?, ?)", default_recipes)

# Save all changes permanently to the database
connection.commit()

# ---- CONSTANTS ----
# Using constants instead of magic numbers makes the program flexible and easy to update
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6"]
MIN_COOKING_TIME = 1  # Minimum valid cooking time in minutes
MAX_CATEGORY_ID = 6   # Number of categories available

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
    # JOIN combines recipes and categories tables so category name displays instead of just a number
    cursor.execute("""
        SELECT recipe_name, ingredients, method, cooking_time, category_name
        FROM recipes
        JOIN categories ON recipes.category_id = categories.category_id
    """)
    recipes = cursor.fetchall()
    
    # Check if any recipes exist before displaying
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

# ---- ADD RECIPE ----
def add_recipe():
    print("\n--- Add a Recipe ---")
    
    # Get recipe name - strip() removes whitespace so spaces only counts as empty
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
        print("Method cannot be empty.")
        return
    
    # isdigit() rejects decimals, negatives and letters - only accepts whole positive numbers
    cooking_time = input("Enter cooking time in minutes: ").strip()
    if cooking_time.isdigit() == False:
        print("Cooking time must be a number.")
        return
    cooking_time = int(cooking_time)
    
    # Check cooking time is at least the minimum value using constant MIN_COOKING_TIME
    if cooking_time < MIN_COOKING_TIME:
        print(f"Cooking time must be at least {MIN_COOKING_TIME} minute.")
        return
    
    # Show categories so user knows valid options before entering category number
    display_categories()
    category_id = input("Enter category number: ").strip()
    if category_id.isdigit() == False:
        print("Invalid category.")
        return
    category_id = int(category_id)
    
    # Check category is within valid range using MAX_CATEGORY_ID constant
    if category_id not in range(1, MAX_CATEGORY_ID + 1):
        print("Invalid category number.")
        return
    
    # Insert recipe into database using ? placeholders to prevent SQL injection
    cursor.execute("""
        INSERT INTO recipes (recipe_name, ingredients, method, cooking_time, category_id)
        VALUES (?, ?, ?, ?, ?)
    """, (recipe_name, ingredients, method, cooking_time, category_id))
    connection.commit()
    print("Recipe added successfully!")

# ---- SEARCH RECIPE ----
def search_recipe():
    print("\n--- Search Recipes ---")
    
    # Get search term - strip() removes whitespace so spaces only counts as empty
    search_term = input("Enter recipe name to search: ").strip()
    if len(search_term) == 0:
        print("Search term cannot be empty.")
        return
    
    # LIKE with % wildcards searches for the term anywhere in the recipe name
    cursor.execute("""
        SELECT recipe_name, ingredients, method, cooking_time, category_name
        FROM recipes
        JOIN categories ON recipes.category_id = categories.category_id
        WHERE recipe_name LIKE ?
    """, ("%" + search_term + "%",))
    
    results = cursor.fetchall()
    
    # Display results or inform user if nothing found
    if len(results) == 0:
        print("No recipes found.")
    else:
        print(f"\n--- Results for '{search_term}' ---")
        for recipe in results:
            print(f"\nName: {recipe[0]}")
            print(f"Ingredients: {recipe[1]}")
            print(f"Method: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Category: {recipe[4]}")
            print("-" * 30)

# ---- DELETE RECIPE ----
def delete_recipe():
    print("\n--- Delete a Recipe ---")
    
    # Show all recipes first so user can see exact recipe names before deleting
    view_recipes()
    
    recipe_name = input("\nEnter the name of the recipe to delete: ").strip()
    if len(recipe_name) == 0:
        print("Recipe name cannot be empty.")
        return
    
    # COLLATE NOCASE makes search case insensitive so 'pancakes' matches 'Pancakes'
    cursor.execute("SELECT * FROM recipes WHERE recipe_name = ? COLLATE NOCASE", (recipe_name,))
    recipe = cursor.fetchone()
    
    # Check recipe exists before attempting to delete
    if recipe is None:
        print("Recipe not found.")
        return
    
    # COLLATE NOCASE used again so delete matches regardless of capitalisation
    cursor.execute("DELETE FROM recipes WHERE recipe_name = ? COLLATE NOCASE", (recipe_name,))
    connection.commit()
    print(f"{recipe_name} deleted successfully!")

# ---- SORT RECIPES ----
def sort_recipes():
    print("\n--- Sort Recipes ---")
    print("1. Shortest cooking time first")
    print("2. Longest cooking time first")
    
    sort_choice = input("Enter choice: ").strip()
    
    # Validate sort choice is either 1 or 2
    if sort_choice not in ["1", "2"]:
        print("Invalid choice.")
        return
    
    # ORDER BY ASC sorts shortest to longest cooking time
    if sort_choice == "1":
        cursor.execute("""
            SELECT recipe_name, ingredients, method, cooking_time, category_name
            FROM recipes
            JOIN categories ON recipes.category_id = categories.category_id
            ORDER BY cooking_time ASC
        """)
        print("\n--- Recipes by Shortest Cooking Time ---")
    else:
        # ORDER BY DESC sorts longest to shortest cooking time
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
        print(f"Method: {recipe[2]}")
        print(f"Cooking Time: {recipe[3]} minutes")
        print(f"Category: {recipe[4]}")
        print("-" * 30)

# ---- MAIN MENU ----
def main_menu():
    # Display menu options to user
    print("\n=== Recipe Manager ===")
    print("1. View all recipes")
    print("2. Add a recipe")
    print("3. Search for a recipe")
    print("4. Delete a recipe")
    print("5. Sort recipes by cooking time")
    print("6. Exit")

# ---- MAIN LOOP ----
# while True keeps the program running until the user chooses to exit
while True:
    main_menu()
    choice = input("Enter your choice: ").strip()
    
    # Validate menu choice is in the list of valid options
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
        # Close database connection safely before exiting
        connection.close()
        break
