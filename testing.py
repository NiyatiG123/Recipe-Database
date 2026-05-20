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

print("Database set up successfully!")