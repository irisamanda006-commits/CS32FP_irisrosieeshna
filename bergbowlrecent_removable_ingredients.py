# Build Your Berg Bowl — beginner/intermediate Python web app
#
# PSEUDOCODE OVERVIEW:
# 1. Store a menu of ingredients with nutrition facts, diet tags, allergens, and simple categories.
# 2. Start a small Python web server on port 8080 for cs50.dev.
# 3. Every time the user clicks a button, the browser sends form data back to Python.
# 4. Python reads the form, updates the bowl, checks constraints, chooses a sprite/message, and rebuilds the HTML page.
# 5. The “Suggest bowl” feature randomly tries many five-ingredient bowls that match the user's filters.

# Import only built-in Python modules so this runs directly in cs50.dev without installing packages.
import html
import http.server
import mimetypes
import os
import random
import socketserver
import urllib.parse
from datetime import datetime

# Use port 8080 because cs50.dev can preview that port easily from the Ports tab.
PORT = 8080

# Store ingredient data. Each ingredient has nutrition, diet tags, allergens, and a category.
INGREDIENTS = [
    {"name": "Black-Eyed Peas", "cal": 100, "prot": 6.7, "carb": 18.0, "fat": 0.5, "fiber": 6.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "protein"},
    {"name": "Broccoli Slaw", "cal": 90, "prot": 2.5, "carb": 10.0, "fat": 4.5, "fiber": 3.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Caesar Salad", "cal": 180, "prot": 4.0, "carb": 12.0, "fat": 13.0, "fiber": 2.0, "tags": ["vegetarian"], "allergens": ["dairy", "gluten"], "category": "vegetable"},
    {"name": "Chickpeas", "cal": 120, "prot": 6.5, "carb": 20.0, "fat": 2.0, "fiber": 5.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "protein"},
    {"name": "Corn", "cal": 66, "prot": 2.5, "carb": 15.0, "fat": 1.0, "fiber": 2.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Cottage Cheese", "cal": 110, "prot": 13.0, "carb": 5.0, "fat": 2.5, "fiber": 0.0, "tags": ["vegetarian"], "allergens": ["dairy"], "category": "protein"},
    {"name": "Cranberries", "cal": 46, "prot": 0.0, "carb": 12.0, "fat": 0.1, "fiber": 1.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "fruit"},
    {"name": "Onions", "cal": 8, "prot": 0.2, "carb": 1.9, "fat": 0.0, "fiber": 0.3, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Farro", "cal": 170, "prot": 6.0, "carb": 32.0, "fat": 1.5, "fiber": 5.0, "tags": ["vegan", "vegetarian"], "allergens": ["gluten"], "category": "grain"},
    {"name": "Feta Cheese", "cal": 75, "prot": 4.0, "carb": 1.2, "fat": 6.0, "fiber": 0.0, "tags": ["vegetarian"], "allergens": ["dairy"], "category": "protein"},
    {"name": "Tuna", "cal": 60, "prot": 13.0, "carb": 0.0, "fat": 0.5, "fiber": 0.0, "tags": [], "allergens": [], "category": "protein"},
    {"name": "Tomatoes", "cal": 27, "prot": 1.3, "carb": 5.8, "fat": 0.3, "fiber": 1.5, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Tofu", "cal": 80, "prot": 9.0, "carb": 2.0, "fat": 4.0, "fiber": 1.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "protein"},
    {"name": "Eggs", "cal": 78, "prot": 6.3, "carb": 0.6, "fat": 5.3, "fiber": 0.0, "tags": ["vegetarian"], "allergens": [], "category": "protein"},
    {"name": "Boom Sauce", "cal": 90, "prot": 0.0, "carb": 3.0, "fat": 9.0, "fiber": 0.0, "tags": [], "allergens": [], "category": "sauce"},
    {"name": "Hummus", "cal": 70, "prot": 2.0, "carb": 8.0, "fat": 3.0, "fiber": 2.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "protein"},
    {"name": "Olives", "cal": 35, "prot": 0.3, "carb": 1.8, "fat": 3.2, "fiber": 1.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Greens", "cal": 10, "prot": 0.8, "carb": 1.5, "fat": 0.1, "fiber": 1.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Millet", "cal": 150, "prot": 4.2, "carb": 30.0, "fat": 1.7, "fiber": 2.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "grain"},
    {"name": "Chicken", "cal": 120, "prot": 23.0, "carb": 1.0, "fat": 2.5, "fiber": 0.0, "tags": ["halal"], "allergens": [], "category": "protein"},
    {"name": "Carrots", "cal": 26, "prot": 0.6, "carb": 6.0, "fat": 0.1, "fiber": 2.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Avocado", "cal": 80, "prot": 1.0, "carb": 4.3, "fat": 7.3, "fiber": 5.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Cucumbers", "cal": 8, "prot": 0.3, "carb": 1.9, "fat": 0.1, "fiber": 0.5, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Spinach", "cal": 7, "prot": 0.9, "carb": 1.1, "fat": 0.1, "fiber": 0.7, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Broccoli", "cal": 27, "prot": 1.9, "carb": 5.5, "fat": 0.3, "fiber": 2.5, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Peppers", "cal": 20, "prot": 0.7, "carb": 4.6, "fat": 0.2, "fiber": 1.5, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Sweet Potatoes", "cal": 130, "prot": 2.0, "carb": 30.0, "fat": 0.5, "fiber": 4.0, "tags": ["vegan", "vegetarian"], "allergens": [], "category": "vegetable"},
    {"name": "Tabouleh", "cal": 100, "prot": 2.5, "carb": 16.0, "fat": 3.5, "fiber": 2.0, "tags": ["vegan", "vegetarian"], "allergens": ["gluten"], "category": "grain"},
]

# Create fast lookup tables so we can find ingredients by name.
BY_NAME = {item["name"]: item for item in INGREDIENTS}
SAVED_BOWLS = []

# Escape text before putting it into HTML so special characters do not break the page.
def esc(text):
    return html.escape(str(text), quote=True)

# Check if an ingredient matches the user's search text.
def search_matches(item, search_text):
    if not search_text:
        return True
    return search_text.lower() in item["name"].lower()

# Check if an ingredient satisfies every selected diet filter.
def diet_matches(item, diet_filters):
    for diet in diet_filters:
        if diet not in item["tags"]:
            return False
    return True

# Check whether an ingredient contains a selected allergen.
def has_selected_allergen(item, allergy_filters):
    return bool(set(item["allergens"]) & allergy_filters)

# Add up nutrition totals for the selected bowl.
def totals(selected):
    total = {"cal": 0.0, "prot": 0.0, "carb": 0.0, "fat": 0.0, "fiber": 0.0}
    for name, qty in selected.items():
        item = BY_NAME[name]
        total["cal"] += item["cal"] * qty
        total["prot"] += item["prot"] * qty
        total["carb"] += item["carb"] * qty
        total["fat"] += item["fat"] * qty
        total["fiber"] += item["fiber"] * qty
    return total

# Calculate percent of calories that come from carbs.
def carb_percent(total):
    if total["cal"] <= 0:
        return 0.0
    return 100 * (total["carb"] * 4) / total["cal"]

# Check if a bowl satisfies selected nutrition goals.
def meets_goals(total, goal_filters, min_cal=None, max_cal=None):
    if "high-protein" in goal_filters and total["prot"] < 50:
        return False
    if "low-carb" in goal_filters and carb_percent(total) >= 20:
        return False
    if min_cal is not None and total["cal"] < min_cal:
        return False
    if max_cal is not None and total["cal"] > max_cal:
        return False
    return True

# Give a score to bowls that do not perfectly meet the goals; lower is better.
def goal_penalty(total, goal_filters, min_cal=None, max_cal=None):
    penalty = 0.0
    if "high-protein" in goal_filters:
        penalty += max(0, 50 - total["prot"]) * 10
    if "low-carb" in goal_filters:
        penalty += max(0, carb_percent(total) - 19.9) * 8
    if min_cal is not None:
        penalty += max(0, min_cal - total["cal"]) * 2
    if max_cal is not None:
        penalty += max(0, total["cal"] - max_cal) * 2
    return penalty

# Parse ingredient quantities from the submitted form.
def parse_selected(form):
    selected = {}
    for item in INGREDIENTS:
        raw = form.get(f"qty_{item['name']}", ["0"])[0]
        try:
            qty = int(raw)
        except ValueError:
            qty = 0
        qty = max(0, min(5, qty))
        if qty > 0:
            selected[item["name"]] = qty
    return selected

# Parse diet filters, goal filters, and allergy warnings from the form.
def parse_filters(form):
    diet_filters = set(form.get("diet", []))
    goal_filters = set(form.get("goal", []))
    allergy_filters = set(form.get("allergy", []))
    return diet_filters, goal_filters, allergy_filters

# Read the user's desired calorie range and keep it reasonable.
def parse_calorie_range(form):
    try:
        min_cal = int(form.get("min_cal", ["450"])[0])
    except ValueError:
        min_cal = 450
    try:
        max_cal = int(form.get("max_cal", ["750"])[0])
    except ValueError:
        max_cal = 750

    min_cal = max(0, min_cal)
    max_cal = max(min_cal, max_cal)
    return min_cal, max_cal

# Convert comma-separated pinned text into ingredient names that match the menu.
def pinned_ingredients(pinned_text, pool):
    pins = [part.strip().lower() for part in pinned_text.split(",") if part.strip()]
    pinned = []
    for pin in pins:
        for item in pool:
            if pin in item["name"].lower() and item["name"] not in pinned:
                pinned.append(item["name"])
                break
    return pinned

# Check whether a proposed bowl has exactly five ingredients and includes protein + vegetable.
def valid_structure(names):
    if len(names) != 5:
        return False
    has_protein = any(BY_NAME[name]["category"] == "protein" for name in names)
    has_vegetable = any(BY_NAME[name]["category"] == "vegetable" for name in names)
    return has_protein and has_vegetable

# Randomly generate five-ingredient bowls that respect filters and choose a good one.
def suggest_bowl(diet_filters, goal_filters, allergy_filters, pinned_text, min_cal, max_cal):
    # Build a safe pool of ingredients that respects diet filters and avoids selected allergens.
    pool = [item for item in INGREDIENTS if diet_matches(item, diet_filters) and not has_selected_allergen(item, allergy_filters)]

    # Start with pinned ingredients that are allowed by the user's constraints.
    pinned = pinned_ingredients(pinned_text, pool)[:5]

    # If there are too few possible ingredients, return them with one serving each.
    if len(pool) < 5:
        return {item["name"]: 1 for item in pool}

    best_selected = None
    best_penalty = float("inf")
    best_random_tiebreaker = 0

    # Try many random bowls. Each bowl has five ingredient TYPES, but each type can have
    # 1 to 5 servings. This lets suggestions hit bigger calorie targets like 700-900 calories.
    for _ in range(7000):
        names = list(pinned)
        remaining = [item["name"] for item in pool if item["name"] not in names]
        needed = 5 - len(names)
        if needed < 0 or len(remaining) < needed:
            continue

        names.extend(random.sample(remaining, needed))

        # The bowl must include at least one protein source and one vegetable.
        if not valid_structure(names):
            continue

        # Give each of the five ingredient types a random serving count.
        # Protein ingredients are allowed to be doubled/tripled often because students may need
        # more than one serving to reach high-protein or high-calorie meal targets.
        selected = {}
        for name in names:
            item = BY_NAME[name]
            if item["category"] == "protein":
                selected[name] = random.choice([1, 1, 2, 2, 3, 4])
            elif item["category"] in ["sauce", "fruit"]:
                selected[name] = random.choice([1, 1, 1, 2])
            else:
                selected[name] = random.choice([1, 1, 2, 2, 3])

        # Score the bowl against the user's goals and calorie range.
        total = totals(selected)
        penalty = goal_penalty(total, goal_filters, min_cal, max_cal)

        # Small preference for bowls closer to the middle of the calorie range.
        if min_cal is not None and max_cal is not None:
            target_midpoint = (min_cal + max_cal) / 2
            penalty += abs(total["cal"] - target_midpoint) * 0.15

        # Small penalty for extremely huge serving counts so suggestions stay meal-like.
        penalty += max(0, sum(selected.values()) - 10) * 4

        # Random tie-breaker helps suggestions feel varied instead of always identical.
        tiebreaker = random.random()
        if penalty < best_penalty or (penalty == best_penalty and tiebreaker > best_random_tiebreaker):
            best_selected = selected
            best_penalty = penalty
            best_random_tiebreaker = tiebreaker

        if meets_goals(total, goal_filters, min_cal, max_cal):
            return selected

    # If random search failed, force one protein and one vegetable, then fill the rest.
    # Then add extra servings, prioritizing protein, until the bowl approaches the minimum calories.
    if best_selected is None:
        proteins = [item["name"] for item in pool if item["category"] == "protein"]
        vegetables = [item["name"] for item in pool if item["category"] == "vegetable"]
        names = list(pinned)
        if proteins and not any(BY_NAME[name]["category"] == "protein" for name in names):
            names.append(random.choice(proteins))
        if vegetables and not any(BY_NAME[name]["category"] == "vegetable" for name in names):
            names.append(random.choice(vegetables))
        remaining = [item["name"] for item in pool if item["name"] not in names]
        random.shuffle(remaining)
        names.extend(remaining[:max(0, 5 - len(names))])
        best_selected = {name: 1 for name in names[:5]}

    # Final adjustment pass. If the bowl is below the calorie minimum, add servings
    # to existing ingredients without adding a sixth ingredient type. Respect the max calorie range if set.
    if min_cal is not None:
        for _ in range(20):
            current = totals(best_selected)
            if current["cal"] >= min_cal:
                break

            # Prefer increasing protein servings first, then higher-calorie existing ingredients.
            candidates = sorted(
                best_selected.keys(),
                key=lambda name: (BY_NAME[name]["category"] == "protein", BY_NAME[name]["cal"]),
                reverse=True,
            )

            added = False
            for name in candidates:
                if best_selected[name] >= 5:
                    continue
                trial = dict(best_selected)
                trial[name] += 1
                trial_total = totals(trial)
                if max_cal is None or trial_total["cal"] <= max_cal:
                    best_selected = trial
                    added = True
                    break
            if not added:
                break

    return best_selected

# Save the current bowl in memory so the user can see past bowls during this session.
def save_current_bowl(selected):
    if not selected:
        return
    total = totals(selected)
    record = {"time": datetime.now().strftime("%I:%M %p").lstrip("0"), "items": dict(selected), "totals": total}
    SAVED_BOWLS.insert(0, record)
    del SAVED_BOWLS[10:]

# Choose the sprite mood and message based on the bowl's current nutrition.
def get_sprite_feedback(total, goal_filters, selected_count, min_cal=None, max_cal=None):
    cpercent = carb_percent(total)
    if selected_count == 0:
        return "idle", "Start building your Berg Bowl!"
    if min_cal is not None and total["cal"] < min_cal:
        return "thinking", "This bowl may be too light for a full meal."
    if max_cal is not None and total["cal"] > max_cal:
        return "warning", "This bowl is above your calorie range."
    if "low-carb" in goal_filters and cpercent >= 20:
        return "warning", "This bowl is high in carbs."
    if "high-protein" in goal_filters and total["prot"] >= 50:
        return "protein", "Nice! You hit your protein goal!"
    if "high-protein" in goal_filters and total["prot"] >= 40:
        return "thinking", "Almost there — add more protein!"
    if total["cal"] < 250 and total["prot"] < 15:
        return "thinking", "Try adding more protein!"
    return "happy", "Looking good!"

# Store small inline SVG drawings for each ingredient.
# Each entry has a border color and an SVG body. These graphics are embedded in the code,
# so they work without extra ingredient image files.
INGREDIENT_SVGS = {
    "Black-Eyed Peas": ("#7a5a24", "<ellipse cx='20' cy='20' rx='13' ry='10' fill='#d1a34b'/><circle cx='20' cy='20' r='4' fill='#222'/>"),
    "Broccoli Slaw": ("#4f8a3b", "<rect x='17' y='23' width='6' height='11' rx='2' fill='#8b6b35'/><circle cx='14' cy='20' r='7' fill='#4caf50'/><circle cx='26' cy='20' r='7' fill='#4caf50'/><circle cx='20' cy='14' r='8' fill='#75c46b'/>"),
    "Caesar Salad": ("#5f8f3f", "<ellipse cx='14' cy='23' rx='7' ry='11' fill='#9ccc65' transform='rotate(-18 14 23)'/><ellipse cx='25' cy='22' rx='7' ry='11' fill='#c5e1a5' transform='rotate(18 25 22)'/><ellipse cx='20' cy='15' rx='6' ry='10' fill='#dcedc8'/>"),
    "Chickpeas": ("#c8941a", "<circle cx='14' cy='22' r='8' fill='#f5d06b'/><circle cx='26' cy='22' r='8' fill='#f5d06b'/><circle cx='20' cy='15' r='8' fill='#eec843'/>"),
    "Corn": ("#d4a000", "<ellipse cx='20' cy='20' rx='9' ry='14' fill='#fdd835'/><g fill='#f9a825'><rect x='13' y='9' width='4' height='4' rx='2'/><rect x='18' y='8' width='4' height='4' rx='2'/><rect x='23' y='9' width='4' height='4' rx='2'/><rect x='13' y='15' width='4' height='4' rx='2'/><rect x='18' y='14' width='4' height='4' rx='2'/><rect x='23' y='15' width='4' height='4' rx='2'/><rect x='13' y='21' width='4' height='4' rx='2'/><rect x='18' y='20' width='4' height='4' rx='2'/><rect x='23' y='21' width='4' height='4' rx='2'/></g>"),
    "Cottage Cheese": ("#b0b0b0", "<rect x='8' y='10' width='24' height='20' rx='4' fill='#f8f8f8' stroke='#ddd'/><circle cx='14' cy='16' r='3' fill='white' stroke='#ddd'/><circle cx='22' cy='15' r='3' fill='white' stroke='#ddd'/><circle cx='27' cy='23' r='3' fill='white' stroke='#ddd'/><circle cx='16' cy='24' r='2.5' fill='white' stroke='#ddd'/>"),
    "Cranberries": ("#9b111e", "<circle cx='13' cy='23' r='6' fill='#c62828'/><circle cx='23' cy='24' r='5' fill='#b71c1c'/><circle cx='28' cy='17' r='6' fill='#d32f2f'/><circle cx='18' cy='14' r='5' fill='#e53935'/>"),
    "Onions": ("#9c6b9e", "<g fill='#ce93d8' stroke='#9c6b9e' stroke-width='.6'><rect x='9' y='9' width='8' height='8' rx='1'/><rect x='20' y='10' width='8' height='8' rx='1'/><rect x='11' y='21' width='8' height='8' rx='1'/><rect x='23' y='22' width='7' height='7' rx='1'/></g>"),
    "Farro": ("#8d6e3a", "<ellipse cx='14' cy='21' rx='5' ry='9' fill='#a1887f' transform='rotate(-15 14 21)'/><ellipse cx='21' cy='18' rx='5' ry='9' fill='#8d6e3a'/><ellipse cx='27' cy='22' rx='5' ry='9' fill='#a1887f' transform='rotate(15 27 22)'/><line x1='18' y1='8' x2='16' y2='4' stroke='#66bb6a' stroke-width='1.5'/>"),
    "Feta Cheese": ("#8a9bb0", "<rect x='7' y='12' width='26' height='16' rx='2' fill='#eceff1' stroke='#b0bec5'/><circle cx='13' cy='18' r='2' fill='#cfd8dc'/><circle cx='22' cy='16' r='1.8' fill='#cfd8dc'/><circle cx='28' cy='22' r='2' fill='#cfd8dc'/>"),
    "Tuna": ("#5b8fa8", "<ellipse cx='20' cy='20' rx='14' ry='10' fill='#b0bec5'/><path d='M9 17 Q15 13 21 17 Q27 21 31 17' fill='none' stroke='#78909c' stroke-width='1.3'/><path d='M9 22 Q15 18 21 22 Q27 26 31 22' fill='none' stroke='#78909c' stroke-width='1.3'/>"),
    "Tomatoes": ("#b71c1c", "<ellipse cx='14' cy='23' rx='7' ry='9' fill='#e53935'/><ellipse cx='26' cy='23' rx='7' ry='9' fill='#c62828'/><ellipse cx='20' cy='13' rx='7' ry='9' fill='#ef5350'/><line x1='20' y1='4' x2='20' y2='9' stroke='#388e3c' stroke-width='1.5'/>"),
    "Tofu": ("#c8960c", "<rect x='8' y='10' width='24' height='20' rx='2' fill='#fff9c4' stroke='#f9a825'/><line x1='8' y1='15' x2='32' y2='15' stroke='#f57f17' stroke-width='2'/><line x1='8' y1='21' x2='32' y2='21' stroke='#f57f17' stroke-width='2'/><line x1='8' y1='27' x2='32' y2='27' stroke='#f57f17' stroke-width='2'/>"),
    "Eggs": ("#c8a000", "<ellipse cx='20' cy='20' rx='12' ry='14' fill='#fffde7' stroke='#f9a825'/><circle cx='20' cy='20' r='7' fill='#fdd835'/>"),
    "Boom Sauce": ("#b85000", "<rect x='12' y='6' width='16' height='24' rx='3' fill='#ff8f00' stroke='#e65100'/><rect x='14' y='4' width='12' height='5' rx='1' fill='#e65100'/><rect x='15' y='14' width='10' height='3' rx='1' fill='#fff3e0'/><rect x='15' y='20' width='10' height='3' rx='1' fill='#fff3e0'/>"),
    "Hummus": ("#c8a050", "<ellipse cx='20' cy='22' rx='14' ry='9' fill='#f5deb3' stroke='#deb887'/><ellipse cx='20' cy='19' rx='10' ry='7' fill='#edd9a3'/><circle cx='20' cy='19' r='4' fill='#d2691e' opacity='.4'/>"),
    "Olives": ("#4a235a", "<ellipse cx='14' cy='22' rx='6' ry='9' fill='#6a1b9a'/><ellipse cx='26' cy='20' rx='6' ry='9' fill='#7b1fa2'/><ellipse cx='20' cy='14' rx='6' ry='9' fill='#6a1b9a'/>"),
    "Greens": ("#2e7d32", "<ellipse cx='14' cy='23' rx='6' ry='11' fill='#66bb6a' transform='rotate(-22 14 23)'/><ellipse cx='26' cy='23' rx='6' ry='11' fill='#4caf50' transform='rotate(22 26 23)'/><ellipse cx='20' cy='14' rx='5' ry='9' fill='#81c784'/>"),
    "Millet": ("#b8963e", "<g fill='#f5deb3'><circle cx='14' cy='20' r='4'/><circle cx='21' cy='17' r='4'/><circle cx='27' cy='22' r='4'/><circle cx='17' cy='26' r='3.5'/><circle cx='24' cy='27' r='3'/><circle cx='13' cy='27' r='3'/></g>"),
    "Chicken": ("#8b4513", "<ellipse cx='20' cy='20' rx='14' ry='10' fill='#d2691e'/><path d='M10 18 Q15 12 20 18 Q25 24 30 18' fill='none' stroke='#8b4513' stroke-width='1.5'/><path d='M10 23 Q15 17 20 23 Q25 29 30 23' fill='none' stroke='#8b4513' stroke-width='1.5'/>"),
    "Carrots": ("#d4500a", "<rect x='10' y='12' width='4' height='16' rx='2' fill='#ff8c00' transform='rotate(-10 12 20)'/><rect x='16' y='10' width='4' height='18' rx='2' fill='#ff7700'/><rect x='23' y='11' width='4' height='17' rx='2' fill='#ff8c00' transform='rotate(8 25 19)'/>"),
    "Avocado": ("#3d6b35", "<ellipse cx='20' cy='20' rx='11' ry='14' fill='#8bc34a'/><ellipse cx='20' cy='20' rx='8' ry='11' fill='#c5e1a5'/><ellipse cx='20' cy='21' rx='5' ry='7' fill='#5d4037'/>"),
    "Cucumbers": ("#2e7d32", "<circle cx='20' cy='20' r='12' fill='#c8e6c9' stroke='#4caf50' stroke-width='1.5'/><circle cx='20' cy='20' r='8' fill='#a5d6a7'/><line x1='20' y1='12' x2='20' y2='28' stroke='#388e3c'/><line x1='12' y1='20' x2='28' y2='20' stroke='#388e3c'/>"),
    "Spinach": ("#1b5e20", "<ellipse cx='16' cy='24' rx='8' ry='11' fill='#2e7d32' transform='rotate(-25 16 24)'/><ellipse cx='24' cy='24' rx='8' ry='11' fill='#388e3c' transform='rotate(25 24 24)'/><ellipse cx='20' cy='16' rx='7' ry='10' fill='#43a047'/>"),
    "Broccoli": ("#2e7d32", "<rect x='17' y='25' width='6' height='9' rx='2' fill='#795548'/><circle cx='13' cy='22' r='7' fill='#388e3c'/><circle cx='27' cy='22' r='7' fill='#388e3c'/><circle cx='20' cy='16' r='8' fill='#4caf50'/>"),
    "Peppers": ("#d4750a", "<rect x='9' y='10' width='6' height='20' rx='3' fill='#ffa000' transform='rotate(-10 12 20)'/><rect x='17' y='8' width='6' height='22' rx='3' fill='#ff8f00'/><rect x='25' y='10' width='6' height='20' rx='3' fill='#ffb300' transform='rotate(10 28 20)'/>"),
    "Sweet Potatoes": ("#b8560a", "<ellipse cx='14' cy='22' rx='8' ry='10' fill='#e8650a' transform='rotate(-10 14 22)'/><ellipse cx='26' cy='22' rx='8' ry='10' fill='#d4500a' transform='rotate(10 26 22)'/><ellipse cx='20' cy='15' rx='8' ry='10' fill='#f07020'/>"),
    "Tabouleh": ("#5d8a3c", "<g fill='#d4e157'><circle cx='14' cy='22' r='4'/><circle cx='21' cy='20' r='4'/><circle cx='27' cy='24' r='3.5'/><circle cx='17' cy='27' r='3'/><circle cx='24' cy='15' r='3'/><circle cx='13' cy='15' r='3'/></g><line x1='18' y1='10' x2='15' y2='6' stroke='#4caf50'/>"),
}
DEFAULT_SVG_COLOR = "#888888"
DEFAULT_SVG_BODY = "<circle cx='20' cy='20' r='14' fill='#ddd'/>"

# Build a URL that preserves the current page state but can remove one ingredient.
def make_state_url(selected, diet_filters, goal_filters, allergy_filters, search_text, pinned_text, min_cal, max_cal, remove_name=None):
    kept_selected = dict(selected)
    if remove_name in kept_selected:
        del kept_selected[remove_name]

    params = []
    params.append(("action", "update"))
    if search_text:
        params.append(("search", search_text))
    if pinned_text:
        params.append(("pinned", pinned_text))
    for diet in sorted(diet_filters):
        params.append(("diet", diet))
    for goal in sorted(goal_filters):
        params.append(("goal", goal))
    for allergy in sorted(allergy_filters):
        params.append(("allergy", allergy))
    params.append(("min_cal", str(min_cal)))
    params.append(("max_cal", str(max_cal)))
    for name, qty in kept_selected.items():
        params.append((f"qty_{name}", str(qty)))
    return "?" + urllib.parse.urlencode(params)

# Create an embedded SVG icon for an ingredient inside the bowl graphic.
def ingredient_svg(name, qty, remove_url=None):
    color, body = INGREDIENT_SVGS.get(name, (DEFAULT_SVG_COLOR, DEFAULT_SVG_BODY))
    label = name if len(name) <= 14 else name[:13] + "…"
    qty_badge = ""
    if qty > 1:
        qty_badge = (
            f"<circle cx='32' cy='8' r='7' fill='{esc(color)}'/>"
            f"<text x='32' y='11' font-size='8' text-anchor='middle' fill='white' "
            f"font-family='Arial,sans-serif' font-weight='bold'>{qty}</text>"
        )
    remove_button = ""
    if remove_url:
        remove_button = f"<a class='remove-ingredient' href='{esc(remove_url)}' title='Remove {esc(name)}'>×</a>"
    return (
        "<div class='ingredient-graphic'>"
        f"{remove_button}"
        "<svg width='46' height='46' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'>"
        f"{body}{qty_badge}"
        "</svg>"
        f"<span>{esc(label)}</span>"
        "</div>"
    )

# Draw the current bowl using embedded ingredient SVG graphics.
def bowl_visual(selected, diet_filters, goal_filters, allergy_filters, search_text, pinned_text, min_cal, max_cal):
    if not selected:
        return "<div class='empty-bowl'>Your bowl is empty.</div>"
    icons = []
    for name, qty in selected.items():
        remove_url = make_state_url(
            selected, diet_filters, goal_filters, allergy_filters,
            search_text, pinned_text, min_cal, max_cal, remove_name=name
        )
        icons.append(ingredient_svg(name, qty, remove_url))
    return f"<div class='bowl'>{''.join(icons)}</div>"

# Build the complete HTML page every time the browser requests it.
def render_page(selected, diet_filters, goal_filters, allergy_filters, search_text, pinned_text, min_cal, max_cal, message=""):
    total = totals(selected)
    cpercent = carb_percent(total)
    selected_count = sum(selected.values())
    sprite_mood, sprite_message = get_sprite_feedback(total, goal_filters, selected_count, min_cal, max_cal)

    # Build table rows only for ingredients that match search and diet filters.
    rows = []
    visible_names = set()
    for item in INGREDIENTS:
        if not search_matches(item, search_text):
            continue
        if not diet_matches(item, diet_filters):
            continue
        visible_names.add(item["name"])
        qty = selected.get(item["name"], 0)
        allergy_class = "allergy-warning" if has_selected_allergen(item, allergy_filters) else ""
        allergens = ", ".join(item["allergens"]) or "-"
        rows.append(f"""
        <tr class='{allergy_class}'>
          <td>{esc(item['name'])}</td>
          <td>{item['cal']}</td>
          <td>{item['prot']}</td>
          <td>{item['carb']}</td>
          <td>{item['fat']}</td>
          <td>{item['fiber']}</td>
          <td>{esc(item['category'])}</td>
          <td>{', '.join(item['tags']) or '-'}</td>
          <td>{esc(allergens)}</td>
          <td><input type='number' name='qty_{esc(item['name'])}' min='0' max='5' value='{qty}'></td>
        </tr>
        """)

    # Preserve hidden selected ingredients when search hides their rows.
    hidden_selected_inputs = ""
    for name, qty in selected.items():
        if name not in visible_names:
            hidden_selected_inputs += f"<input type='hidden' name='qty_{esc(name)}' value='{qty}'>\n"

    # Show saved bowls if the user has saved any during this run.
    if SAVED_BOWLS:
        saved_html = ""
        for record in SAVED_BOWLS:
            names = ", ".join(f"{name} x{qty}" for name, qty in record["items"].items())
            saved_html += f"<li><strong>{esc(record['time'])}</strong> — {esc(names)} ({round(record['totals']['cal'])} cal)</li>"
    else:
        saved_html = "<li>No saved bowls yet.</li>"

    # Show warnings if the current bowl breaks a selected nutrition goal or calorie range.
    warning = ""
    if total["cal"] > 0 and total["cal"] < min_cal:
        warning = "<div class='warn'>This bowl is under your calorie range, so it may not be substantial enough for a meal.</div>"
    elif total["cal"] > max_cal:
        warning = "<div class='warn'>This bowl is above your calorie range.</div>"
    elif "low-carb" in goal_filters and cpercent >= 20:
        warning = "<div class='warn'>Your bowl is over the low-carb target.</div>"

    # Tell the user whether the randomized suggestion met all selected nutrition goals.
    if message == "suggested":
        if meets_goals(total, goal_filters, min_cal, max_cal):
            message = "Suggested a random five-ingredient meal bowl within your calorie range."
        else:
            message = "Suggested the closest random five-ingredient bowl I could find for those constraints and calorie range."


    return f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>Build Your Berg Bowl</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f4ef; color: #2f2f2f; }}
header {{ background: linear-gradient(135deg, #8b1a1a, #c75b39); color: white; padding: 22px 24px; }}
header h1 {{ margin: 0; font-family: 'Trebuchet MS', 'Comic Sans MS', Arial, sans-serif; font-size: 44px; letter-spacing: 1px; text-shadow: 3px 3px 0 rgba(0,0,0,.18); }}
main {{ display: grid; grid-template-columns: 2fr 1fr; gap: 24px; padding: 24px; }}
section, aside {{ background: white; border-radius: 18px; padding: 18px; box-shadow: 0 1px 8px rgba(0,0,0,0.08); }}
h2, h3 {{ margin-top: 0; }}
.controls {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
label {{ display: block; margin: 6px 0; }}
input[type='text'], input[type='number'] {{ padding: 7px; border: 1px solid #ccc; border-radius: 6px; width: 100%; box-sizing: border-box; }}
button {{ background: #8b1a1a; color: white; border: none; padding: 10px 14px; border-radius: 8px; cursor: pointer; margin-right: 8px; }}
button.secondary {{ background: #555; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th, td {{ border-bottom: 1px solid #eee; padding: 8px; text-align: left; vertical-align: top; }}
.stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 16px; }}
.card {{ background: #faf6f1; border-radius: 12px; padding: 12px; }}
.bowl, .empty-bowl {{ min-height: 180px; border: 8px solid #8b5a2b; border-top-width: 14px; border-radius: 0 0 220px 220px; padding: 18px; background: #fffaf3; display: flex; flex-wrap: wrap; gap: 8px; align-content: flex-start; }}
.empty-bowl {{ align-items: center; justify-content: center; color: #777; }}
.ingredient-graphic {{ position: relative; display: inline-flex; flex-direction: column; align-items: center; gap: 4px; margin: 4px; width: 64px; }}
.ingredient-graphic svg {{ background: rgba(255,255,255,.58); border-radius: 14px; padding: 3px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
.remove-ingredient {{ position: absolute; top: -6px; right: 5px; width: 18px; height: 18px; line-height: 18px; border-radius: 50%; background: #8b1a1a; color: white; text-decoration: none; font-size: 14px; font-weight: bold; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,.2); }}
.remove-ingredient:hover {{ background: #c75b39; }}
.ingredient-graphic span {{ font-size: 10px; color: #555; text-align: center; max-width: 64px; line-height: 1.15; }}
.warn {{ background: #fff1f1; color: #a11; border: 1px solid #e5b2b2; padding: 10px; border-radius: 8px; margin: 12px 0; }}
.msg {{ background: #eef7ee; color: #245224; border: 1px solid #bfdcbf; padding: 10px; border-radius: 8px; margin-bottom: 14px; }}
.allergy-warning td {{ color: #b00020; font-weight: 700; }}
small {{ color: #666; }}
.sprite-box {{ position: fixed; top: 18px; right: 18px; background: #fff8ef; border: 1px solid #e2c8a0; border-radius: 14px; padding: 10px; width: 170px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.12); z-index: 999; }}
.sprite-img {{ width: 85px; height: 85px; object-fit: contain; }}
.sprite-message {{ font-size: 12px; font-weight: bold; color: #7a3e1d; margin-top: 6px; }}
</style>
</head>
<body>
<div class='sprite-box'>
  <img class='sprite-img' src='/sprites/{esc(sprite_mood)}.png'>
  <div class='sprite-message'>{esc(sprite_message)}</div>
</div>
<header>
  <h1>Build Your Berg Bowl</h1>
</header>
<main>
  <section>
    <h2>Choose your ingredients</h2>
    {f"<div class='msg'>{esc(message)}</div>" if message else ""}
    <form method='GET'>
      {hidden_selected_inputs}
      <div class='controls'>
        <div>
          <label><strong>Search ingredients</strong></label>
          <input type='text' name='search' value='{esc(search_text)}' placeholder='corn, tofu, avocado...'>
          <label><strong>Pin ingredients for suggestions</strong></label>
          <input type='text' name='pinned' value='{esc(pinned_text)}' placeholder='corn, avocado'>
          <small>Suggest mode tries to include these if they do not conflict with filters.</small>
        </div>
        <div>
          <label><strong>Diet filters</strong></label>
          <label><input type='checkbox' name='diet' value='vegetarian' {'checked' if 'vegetarian' in diet_filters else ''}> Vegetarian</label>
          <label><input type='checkbox' name='diet' value='vegan' {'checked' if 'vegan' in diet_filters else ''}> Vegan</label>
          <label><input type='checkbox' name='diet' value='halal' {'checked' if 'halal' in diet_filters else ''}> Halal</label>

          <label style='margin-top:10px;'><strong>Allergy warnings</strong></label>
          <label><input type='checkbox' name='allergy' value='nut' {'checked' if 'nut' in allergy_filters else ''}> Nut allergy</label>
          <label><input type='checkbox' name='allergy' value='dairy' {'checked' if 'dairy' in allergy_filters else ''}> Dairy allergy</label>
          <label><input type='checkbox' name='allergy' value='gluten' {'checked' if 'gluten' in allergy_filters else ''}> Gluten allergy</label>
          <small>Rows with selected allergens turn red. Suggestions avoid them.</small>

          <label style='margin-top:10px;'><strong>Goal filters</strong></label>
          <label><input type='checkbox' name='goal' value='high-protein' {'checked' if 'high-protein' in goal_filters else ''}> High protein (50g+)</label>
          <label><input type='checkbox' name='goal' value='low-carb' {'checked' if 'low-carb' in goal_filters else ''}> Low carb (&lt; 20% calories from carbs)</label>
          <label style='margin-top:10px;'><strong>Meal calorie range</strong></label>
          <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
            <label>Min cal <input type='number' name='min_cal' min='0' max='2000' value='{min_cal}'></label>
            <label>Max cal <input type='number' name='max_cal' min='0' max='2000' value='{max_cal}'></label>
          </div>
          <small>Suggest mode tries to make the five-ingredient bowl land inside this range.</small>
        </div>
      </div>

      <div style='margin-bottom:14px;'>
        <button type='submit' name='action' value='update'>Update bowl</button>
        <button type='submit' name='action' value='suggest'>Suggest bowl</button>
        <button type='submit' name='action' value='save'>Save bowl</button>
        <button type='submit' name='action' value='clear' class='secondary'>Clear bowl</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>Ingredient</th><th>Cal</th><th>Protein</th><th>Carbs</th><th>Fat</th><th>Fiber</th><th>Type</th><th>Tags</th><th>Allergens</th><th>Qty</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </form>
  </section>

  <aside>
    <h2>Your bowl</h2>
    <div class='stats'>
      <div class='card'><strong>Calories</strong><br>{round(total['cal'])}</div>
      <div class='card'><strong>Protein</strong><br>{round(total['prot'],1)} g</div>
      <div class='card'><strong>Carb Calories</strong><br>{round(cpercent,1)}%</div>
      <div class='card'><strong>Fiber</strong><br>{round(total['fiber'],1)} g</div>
      <div class='card'><strong>Carbs</strong><br>{round(total['carb'],1)} g</div>
      <div class='card'><strong>Fat</strong><br>{round(total['fat'],1)} g</div>
    </div>
    {warning}
    {bowl_visual(selected, diet_filters, goal_filters, allergy_filters, search_text, pinned_text, min_cal, max_cal)}

    <h3 style='margin-top:18px;'>Saved bowls</h3>
    <ul>{saved_html}</ul>
  </aside>
</main>
</body>
</html>"""

# Define the web request handler for pages and sprite images.
class Handler(http.server.BaseHTTPRequestHandler):
    # Handle every GET request from the browser.
    def do_GET(self):
        # If the browser asks for a sprite image, serve it from sprites/. Use a fallback if missing.
        if self.path.startswith("/sprites/"):
            requested_path = self.path.lstrip("/")
            fallback_path = "sprites/idle.png"
            if os.path.exists(requested_path):
                path = requested_path
                mime, _ = mimetypes.guess_type(path)
                with open(path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            if os.path.exists(fallback_path):
                path = fallback_path
                mime, _ = mimetypes.guess_type(path)
                with open(path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            data = b"""<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'><rect width='120' height='120' rx='24' fill='#fff8ef'/><circle cx='60' cy='55' r='28' fill='#f3c27a'/><circle cx='50' cy='50' r='4' fill='#552b12'/><circle cx='70' cy='50' r='4' fill='#552b12'/><path d='M48 65 Q60 76 72 65' fill='none' stroke='#552b12' stroke-width='5' stroke-linecap='round'/><text x='60' y='108' font-family='Arial' font-size='13' text-anchor='middle' fill='#7a3e1d'>Berg Pal</text></svg>"""
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # Parse the URL query string into form data.
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        search_text = params.get("search", [""])[0]
        pinned_text = params.get("pinned", [""])[0]
        diet_filters, goal_filters, allergy_filters = parse_filters(params)
        min_cal, max_cal = parse_calorie_range(params)
        action = params.get("action", ["update"])[0]
        selected = parse_selected(params)
        message = ""

        # Decide what to do based on which button the user clicked.
        if action == "clear":
            selected = {}
            message = "Bowl cleared."
        elif action == "suggest":
            selected = suggest_bowl(diet_filters, goal_filters, allergy_filters, pinned_text, min_cal, max_cal)
            message = "suggested"
        elif action == "save":
            save_current_bowl(selected)
            message = "Current bowl saved."

        # Build and send the HTML response.
        page = render_page(selected, diet_filters, goal_filters, allergy_filters, search_text, pinned_text, min_cal, max_cal, message)
        data = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # Silence default logs to keep the terminal clean.
    def log_message(self, format, *args):
        pass

# Allow restarting the server quickly without waiting for the port to reset.
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# Start the server until the user presses Ctrl+C.
def main():
    with ReusableTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Build Your Berg Bowl running on http://localhost:{PORT}")
        print("In cs50.dev: open the Ports tab and preview port 8080.")
        httpd.serve_forever()

# Run the app only when this file is executed directly.
if __name__ == "__main__":
    main()
