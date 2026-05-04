# CS32FP_irisrosieeshna
Harvard students often face challenges such as limited budgets, busy schedules, and easy access to unhealthy food options. This project aims to provide a simple and practical tool to help students make better dietary choices and stay on track with their health goals.

We created a nutrition tracker that helps college students in Cambridge eat healthier at Harvard dining halls by building custom meal bowls aligned with their nutrition goals. The project focuses on realistic, dining hall–style options (inspired by Annenberg) and provides an interactive, user-friendly experience.

Goals
- Help students set and track nutrition goals (calories, protein, etc.)
- Generate personalized meal plans
- Encourage healthier eating habits on a college budget
- Provide a simple, intuitive user experience
Features
- Custom bowl builder: Users select ingredients and adjust serving sizes; the bowl updates dynamically with visual ingredient graphics
- Nutrition tracking: Displays calories, protein, carbs, fat, fiber, and carb-calorie percentage in real time
- Smart suggestions: “Suggest Bowl” generates a randomized 5-ingredient meal that fits within a user-defined calorie range, respects dietary filters and allergies, includes at least one protein and one vegetable, and allows multiple servings to meet targets
- Search & filters: Users can search ingredients and filter by vegetarian, vegan, or halal
- Allergy support: Nut, dairy, and gluten allergies highlight restricted foods in red and influence suggestions
- Ingredient removal: Users can remove items directly from the bowl via an “×” button
- Berg Pal feedback: A sprite provides real-time feedback based on nutrition (e.g., hitting protein goals or exceeding calories)
Usage

Run the program:

python bergbowlrecent_multi_serving_suggest.py

Then open port 8080 in cs50.dev.

Users can search for ingredients, build a bowl, apply filters, set a calorie range, generate suggestions, and receive live feedback.

Challenges & Learning
- Managing dynamic UI updates without JavaScript required careful handling of form state
- Preserving selections across searches required hidden inputs
- Designing a suggestion algorithm that balances randomness with nutritional constraints
- Maintaining consistency between ingredient data and visual rendering

Use of Generative AI
We used generative AI to:
- help organize and structure our Python code
- assist with HTML/CSS interface design
- generate and iterate on sprite visuals

All final implementation, debugging, and design decisions were completed by our team.
