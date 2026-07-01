import streamlit as st
import google.generativeai as genai
import os
import random

# Configure Gemini API Key securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    st.error("API Key not found. Please configure GEMINI_API_KEY in your settings.")

# Set page config
st.set_page_config(page_title="Smart Meal Planner AI", page_icon="🥗", layout="centered")

st.title("🥗 Smart Meal Planner AI BY ANKUR")
st.markdown("### Turn your leftover fridge items into instant premium recipes!")

# --- FEATURE 3: Surprise Me Logic ---
surprise_combinations = [
    "Paneer, Capsicum, Onion, Malai",
    "Maggi, Cheese, Oregano, Chilli Flakes",
    "Aloo, Bread, Green Chutney, Cheese",
    "Rice, Tomato, Garlic, Leftover Dal",
    "Bread, Egg, Onion, Pepper"
]

# Initialize session state for ingredients text if it doesn't exist
if "ingredients_input" not in st.session_state:
    st.session_state.ingredients_input = ""

# Layout for Text Input and Surprise Button side-by-side
col1, col2 = st.columns([4, 1])

with col2:
    st.write("") # Padding to align with text input label
    st.write("") 
    if st.button("✨ Surprise Me!"):
        st.session_state.ingredients_input = random.choice(surprise_combinations)

with col1:
    ingredients = st.text_input(
        "What ingredients do you have in your fridge right now?",
        value=st.session_state.ingredients_input,
        placeholder="e.g., Tomato, Onion, Paneer, Rice"
    )

# --- FEATURE 1 & 2: Dietary Preferences & Cuisine Choices ---
st.markdown("#### 🛠️ Customize Your Recipe")
c1, c2, c3 = st.columns(3)

with c1:
    diet_pref = st.selectbox(
        "Dietary Type:",
        ["No Restrictions", "Vegetarian (Veg)", "Non-Vegetarian", "Vegan", "Jain (No Onion/Garlic)"]
    )

with c2:
    cuisine_style = st.selectbox(
        "Cuisine/Vibe Style:",
        ["Standard Home Style", "Indian Street Food Style", "Healthy / Diet Friendly", "Restaurant Luxury Style", "Quick Evening Snack"]
    )

with c3:
    cooking_time = st.slider("Max Cooking Time (Minutes):", min_value=5, max_value=120, value=20, step=5)

# --- Generate Recipe Button ---
if st.button("Generate My Recipe 🚀", use_container_width=True):
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient first!")
    else:
        with st.spinner("🧑‍🍳 AI Chef Ankur is crafting your recipe..."):
            try:
                # Custom engineering the prompt using ALL chosen features
                prompt = f"""
                You are an elite expert chef. Create a premium recipe based on these parameters:
                - Available Ingredients: {ingredients}
                - Dietary Restriction: {diet_pref}
                - Style/Vibe of Recipe: {cuisine_style}
                - Max Time Allowed: {cooking_time} minutes
                
                Provide a creative and catchy name for the dish, yields, prep time, cook time, a clear ingredients list (incorporating staples like salt, oil, water as needed), and step-by-step instructions. Present it beautifully.
                """
                
                model = genai.GenerativeModel("models/gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.success("Here is your custom recipe! 🔥")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")