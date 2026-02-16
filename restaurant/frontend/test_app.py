import streamlit as st
import pytz
from datetime import datetime

# Simple test app
st.set_page_config(page_title="Test", layout="wide")

# Simple CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    color: white;
}
h1 {
    color: #10b981;
}
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Foodie Hub - Test")

def get_current_meal_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hour = now.hour

    if 6 <= hour < 12:
        return "Morning (Breakfast)"
    elif 12 <= hour < 16:
        return "Afternoon (Lunch)"
    elif 16 <= hour < 19:
        return "Evening (Snacks)"
    else:
        return "Night (Dinner)"

current_meal_time = get_current_meal_time()
st.markdown(f"### 🕐 {current_meal_time}")

st.write("This is a test to see if CSS and basic functionality work.")

if st.button("Test Button"):
    st.success("Button works!")
