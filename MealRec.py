import json
import random
import os
from typing import Dict, List

"""
Mealrec.py - meal recommendation CLI app

Usage:
    python Mealrec.py
"""


DATA_FILE = "meals.json"

DEFAULT_MEALS: Dict[str, List[str]] = {
    "breakfast": ["Oatmeal with fruit", "Scrambled eggs on toast", "Yogurt parfait"],
    "lunch": ["Chicken salad", "Veggie wrap", "Grilled cheese and tomato soup"],
    "dinner": ["Spaghetti Bolognese", "Stir-fry tofu and veggies", "Salmon with rice"],
    "snack": ["Apple and peanut butter", "Hummus and carrots", "Mixed nuts"]
}


def load_meals(path: str = DATA_FILE) -> Dict[str, List[str]]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    return DEFAULT_MEALS.copy()


def save_meals(meals: Dict[str, List[str]], path: str = DATA_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meals, f, indent=2, ensure_ascii=False)


def recommend(meals: Dict[str, List[str]], category: str | None = None) -> str:
    if category:
        items = meals.get(category.lower(), [])
        if not items:
            return f"No meals found for category '{category}'."
        return random.choice(items)
    # pick random category then a meal
    cat = random.choice(list(meals.keys()))
    return f"{cat.title()}: {random.choice(meals[cat])}"


def list_meals(meals: Dict[str, List[str]]) -> str:
    lines = []
    for cat, items in meals.items():
        lines.append(f"{cat.title()}:")
        for i, it in enumerate(items, 1):
            lines.append(f"  {i}. {it}")
    return "\n".join(lines)


def add_meal(meals: Dict[str, List[str]], category: str, meal: str) -> str:
    cat = category.lower()
    meals.setdefault(cat, [])
    if meal in meals[cat]:
        return f"'{meal}' already exists in '{cat}'."
    meals[cat].append(meal)
    save_meals(meals)
    return f"Added '{meal}' to '{cat}'."


def remove_meal(meals: Dict[str, List[str]], category: str, meal_index: int) -> str:
    cat = category.lower()
    items = meals.get(cat)
    if not items:
        return f"No such category: '{cat}'."
    if meal_index < 1 or meal_index > len(items):
        return f"Index out of range for '{cat}'."
    removed = items.pop(meal_index - 1)
    save_meals(meals)
    return f"Removed '{removed}' from '{cat}'."


def prompt() -> None:
    print("Meal Recommendation App")
    print("Commands: recommend [category], random, list, add, remove, quit, help")
    meals = load_meals()
    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not cmd:
            continue
        parts = cmd.split()
        action = parts[0].lower()
        if action in ("quit", "exit"):
            print("Bye.")
            break
        elif action in ("help", "?"):
            print("Commands:")
            print("  recommend [category]  - recommend a meal (optional category)")
            print("  random                - completely random meal")
            print("  list                  - list all meals")
            print("  add                   - add a meal (interactive)")
            print("  remove                - remove a meal (interactive)")
            print("  quit                  - exit")
        elif action in ("recommend",):
            if len(parts) > 1:
                print(recommend(meals, parts[1]))
            else:
                print(recommend(meals))
        elif action == "random":
            print(recommend(meals))
        elif action == "list":
            print(list_meals(meals))
        elif action == "add":
            category = input("Category: ").strip()
            meal = input("Meal name: ").strip()
            if category and meal:
                print(add_meal(meals, category, meal))
            else:
                print("Category and meal name required.")
        elif action == "remove":
            category = input("Category: ").strip()
            if not category:
                print("Category required.")
                continue
            cat = category.lower()
            items = meals.get(cat)
            if not items:
                print(f"No such category '{cat}'.")
                continue
            print(f"Meals in '{cat}':")
            for i, it in enumerate(items, 1):
                print(f"  {i}. {it}")
            try:
                idx = int(input("Index to remove: ").strip())
            except ValueError:
                print("Invalid index.")
                continue
            print(remove_meal(meals, cat, idx))
        else:
            print("Unknown command. Type 'help' for commands.")


if __name__ == "__main__":
    prompt()
