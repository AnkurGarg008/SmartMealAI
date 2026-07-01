import streamlit as st
from google import genai

# Initialize the Gemini API client
client = genai.Client()

st.set_page_config(page_title="Smart Meal Planner AI", page_icon="🥗", layout="centered")

st.title("🥗 Smart Meal Planner AI BY ANKUR")
st.write("---")
st.subheader("Turn your leftover fridge items into instant premium recipes!")

# Input fields
ingredients = st.text_input(
    "What ingredients do you have in your fridge right now?", 
    placeholder="e.g., Tomato, Onion, Paneer, Rice"
)

prep_time = st.slider("How much time do you have to cook? (Minutes)", 5, 60, 20)

# Action button
if st.button("Generate My Recipe 🚀", use_container_width=True):
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient first!")
    else:
        with st.spinner("Ankur's AI Chef is thinking..."):
            prompt = (
                f"Act as a professional chef. I have these ingredients: {ingredients}. "
                f"I only have {prep_time} minutes to cook. Provide a step-by-step recipe "
                f"using primarily these items. Keep it simple, healthy, appetizing, and easy to follow."
            )
            try:
                # Call the ultra-fast gemini-2.5-flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.success("Here is your custom recipe! 🔥")
                st.markdown(response.text)
            except Exception as e:
                st.error("API Key Verification Failed. Ensure your GEMINI_API_KEY environment variable is set.")
                st.write(e)