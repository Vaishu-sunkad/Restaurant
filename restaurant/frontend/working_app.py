import streamlit as st
import time
import random
import pytz
import os
from datetime import datetime
import requests

# Backend URL
BACKEND_URL = "http://localhost:8000"

def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            is_db_connected = "connected to Atlas" in data.get("database", "")
            return True, is_db_connected
        return True, False
    except Exception:
        return False, False

backend_available, db_connected = check_backend()

# Helper to get current meal time
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

# --- Configuration ---
st.set_page_config(page_title="Foodie Hub | Premium Dining", page_icon="🍽️", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = "GREETING"
if "order_details" not in st.session_state:
    st.session_state.order_details = {
        "people": 4,
        "appetite": None,
        "preference": None,
        "cart": {}
    }
# Migration check (if user reloads and has old list structure)
if isinstance(st.session_state.order_details["cart"], list):
    st.session_state.order_details["cart"] = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Helper Functions ---
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

# --- Menu Data ---
MENU = {
    "Morning (Breakfast)": {
        "Veg": [
            {"name": "Masala Dosa", "price": 120, "image": "https://wallpaperaccess.com/full/6340448.jpg"},
            {"name": "Idli Vada", "price": 80, "image": "https://as1.ftcdn.net/v2/jpg/04/65/28/88/1000_F_465288827_zBiEkb_660x660.jpg"},
            {"name": "Poha", "price": 60, "image": "https://thumbs.dreamstime.com/b/poha-23333662.jpg"},
            {"name": "Chole bhature", "price": 100, "image": "https://i0.wp.com/bakaasur.com/wp-content/uploads/2022/12/chole-bhature.jpg?w=1200&ssl=1"},
            {"name": "Bonda", "price": 70, "image": "https://www.masalakorb.com/wp-content/uploads/2023/02/EASY-MYSORE-BONDA-RECIPE-MAIDA-BONDA-MYSORE-BAJJI-V1.jpg"}
        ],
        "Non-Veg": [
            {"name": "Bread Omelette", "price": 80, "image": "https://tse2.mm.bing.net/th/id/OIP.0G9LjhrRb4VglpXOs54JjAHaKX?pid=Api&P=0&h=180"},
            {"name": "Chicken Keema Paratha", "price": 180, "image": "https://1.bp.blogspot.com/-bFuZOx0Aoa4/XP8CVnIxGAI/AAAAAAAAZK4/DsSMVFOlv7gcHpZ4Yw-1200.jpg"},
            {"name": "Egg Bhurji", "price": 90, "image": "http://eggcellent.recipes/wp-content/uploads/2024/08/Indian-Egg-Bhurji-Recipe-1024x1024.png"},
            {"name": "Chicken sausages", "price": 70, "image": "https://insanelygoodrecipes.com/wp-content/uploads/2021/12/Homemade-Fried-Chicken-Sausage-with-Garlic-Butter-Sauce-and-Lemons.jpg"},
            {"name": "Chicken cutlet", "price": 90, "image": "https://therecipemaster.com/wp-content/uploads/2024/09/Chicken-Cutlet-Recipe-Card.webp"}
        ]
    },
    "Afternoon (Lunch)": {
        "Veg": [
            {"name": "Veg Biryani", "price": 280, "image": "https://img.freepik.com/premium-photo/traditional-indian-veg-biryani-banana-leaf_1179130-190160.jpg?w=2000"},
            {"name": "Palak Paneer", "price": 220, "image": "https://img.freepik.com/premium-photo/indian-palak-paneer-with-spinach-cottage-cheese_1072167-2540.jpg?w=2000"},
            {"name": "North Indian Thali", "price": 350, "image": "https://i.pinimg.com/originals/e1/da/d5/e1dad5315972c8a9db86fb01d69c7ecb.jpg"},
            {"name": "South Indian Thali", "price": 320, "image": "https://wp.scoopwhoop.com/wp-content/uploads/2014/09/south.jpg"},
            {"name": "Pallav", "price": 70, "image": "https://1.bp.blogspot.com/-Yf00fooZes8/WrMJKwxMVOI/AAAAAAAAgtg/32-H3Ym2iD4k-y0x640.jpg"}
        ],
        "Non-Veg": [
           {"name": "Chicken Biryani", "price": 300, "image": "https://static.vecteezy.com/system/resources/previews/050/436/451/large_2x/spicy-indian-chicken-biryani-with-basmati-rice-garnished-with-fresh-coriander-and-a-side-of-raita-photo.jpg"},
           {"name": "Mutton Curry", "price": 450, "image": "https://uploads-ssl.webflow.com/5c481361c604e53624138c2f/60f2eb0d5d007bd81723ebe2_Mutton%20curry_1500%20x%201200.jpg"},
           {"name": "Fish Curry", "price": 380, "image": "https://paattiskitchen.com/wp-content/uploads/2023/01/kmc_20230110_191241.jpg"},
           {"name": "Egg Curry", "price": 210, "image": "https://static.vecteezy.com/system/resources/previews/050/436/451/large_2x/spicy-indian-egg-curry-served-parathas-garnished-with-fresh-coriander-and-a-side-of-raita-photo.jpg"},
           {"name": "Chicken Fried Rice", "price": 100, "image": "https://houseofnasheats.com/wp-content/uploads/2023/01/Chicken-Fried-Rice-Recipe-10-680x1018.jpg"}
        ]
    },
    "Evening (Snacks)": {
        "Veg": [
            {"name": "Paneer Tikka", "price": 290, "image": "https://img.freepik.com/premium-photo/photography-tasty-indian-paneer-tikka_1288657-46631.jpg"},
            {"name": "Samosa (3 pcs)", "price": 50, "image": "https://thehimalayantreasure.pl/wp-content/uploads/2018/09/chicken-samosa.jpg"},
            {"name": "Veg Puff", "price": 40, "image": "https://i.pinimg.com/736x/df/31/74/df3174666a44cd060e1eb6d59938d76c--puffs-spicy.jpg"},
            {"name": "French Fries", "price": 120, "image": "https://wallpapers.com/images/hd/french-fries-960-x-960-picture-317878ocb9hyulx0.jpg"}
        ],
        "Non-Veg": [
            {"name": "Chicken Nuggets", "price": 200, "image": "http://www.proofdc.com/wp-content/uploads/media/02/58716144-crispy-baked-chicken-nuggets-recipe-proofdc.jpg"},
            {"name": "Chicken Popcorn", "price": 220, "image": "https://wallpaperaccess.com/full/12256759.jpg"},
            {"name": "Egg Puff", "price": 50, "image": "https://nodashofgluten.com/wp-content/uploads/2025/02/Egg-Puff-Recipe-Kerala-Style-3.png.webp"},
            {"name": "Grilled Chicken Wings", "price": 280, "image": "https://recipeslily.com/wp-content/uploads/2024/07/grilled-wings-recipe.jpg"}
        ]
    },
    "Night (Dinner)": {
        "Veg": [
            {"name": "Butter Naan & Paneer", "price": 350, "image": "https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/54/fd/77/paneer-butter-masala.jpg"},
            {"name": "Veg Fried Rice", "price": 240, "image": "https://thedelishrecipe.com/wp-content/uploads/2024/05/vegetable-fried-rice.jpg"},
            {"name": "Malai Kofta", "price": 330, "image": "https://www.mrishtanna.com/wp-content/uploads/2023/11/malai-kofta-curry-recipe.jpg"},
            {"name": "Mushroom Masala", "price": 310, "image": "https://www.cookingcarnival.com/wp-content/uploads/2018/09/Mushroom-masala.webp"}
        ],
        "Non-Veg": [
            {"name": "Tandoori Chicken", "price": 280, "image": "https://img.freepik.com/premium-photo/indian-spices-barbecue-murgh-tandoori-tandoori-chicken-with-raita-lime-chapati-onion-rings-served-dish-isolated-dark-background-top-view-food_689047-1446.jpg?w=1380"},
            {"name": "Chicken Curry & Roti", "price": 320, "image": "https://themayakitchen.com/wp-content/uploads/2019/06/CURRY.jpg"},
            {"name": "Prawns Masala", "price": 420, "image": "https://rumkisgoldenspoon.com/wp-content/uploads/2022/08/Prawn-masala-recipe-2.jpg"},
            {"name": "Chicken Soup", "price": 180, "image": "https://thefoodxp.com/wp-content/uploads/2022/11/Jamie-Oliver-Chicken-Soup-Recipe-1.jpg"}
        ]
    },
    "Sweets": [
        {"name": "Gulab Jamun (2 pcs)", "price": 60, "image": "https://media.chefdehome.com/740/0/0/gulab-jamun/indian-gulab-jamun-chefdehome-1.jpg"},
        {"name": "Rasgulla (2 pcs)", "price": 70, "image": "https://www.aonesamosa.com/wp-content/uploads/2023/12/Rasgulla.webp"},
        {"name": "Ice Cream (Vanilla)", "price": 50, "image": "https://wallpapers.com/images/hd/ice-cream-pictures-93ucnuf5kr7ghmhg.jpg"},
        {"name": "Chocolate Brownie", "price": 120, "image": "https://tse4.mm.bing.net/th/id/OIP.2eWvcwOeJpY7YgwNfRsJjAHaKX?rs=1&pid=ImgDetMain&o=7&rm=3"}
    ]
}

# --- Sidebar / Header ---
st.title("🍽️ Foodie Hub")
current_meal_time = get_current_meal_time()
st.markdown(f"### 🕐 {current_meal_time}")
if db_connected:
    st.success("🟢 Connected to Database")
else:
    st.warning("🟡 Using Offline Mode (DB Disconnected)")
st.markdown("---")

# --- Chat Display ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- State Machine Logic ---

# 1. GREETING
if st.session_state.step == "GREETING":
    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            text = "👋 Welcome to Foodie Hub! I'll help you place your order quickly 😊 Before we start, I need a few details. 👉 **How many people are dining today?**"
            add_message("assistant", text)
            st.markdown(text)
    
    people = st.chat_input("Enter number of people...")
    if people:
        add_message("user", people)
        with st.chat_message("user"):
            st.markdown(people)
        
        try:
            st.session_state.order_details["people"] = int(people)
            st.session_state.step = "ASK_APPETITE"
            st.rerun()
        except ValueError:
            st.error("Please enter a valid number.")

# 2. ASK APPETITE
elif st.session_state.step == "ASK_APPETITE":
    if len(st.session_state.chat_history) < 3:
        msg = f"Great! 👨👩👧👦 for {st.session_state.order_details['people']} people. 👉 **What is your eating capacity?**"
        add_message("assistant", msg)
        st.rerun()

    st.write("Please choose your eating style:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🥗 **Low** (Light eaters 🧒)"):
        st.session_state.order_details["appetite"] = "Low"
        add_message("user", "Low - Light eaters 🧒")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col2.button("🍱 **Medium** (Standard Foodie 🧔)"):
        st.session_state.order_details["appetite"] = "Medium"
        add_message("user", "Medium - Standard Foodie 🧔")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col3.button("🍖 **Large** (Hungry Kings 🤴)"):
        st.session_state.order_details["appetite"] = "Large"
        add_message("user", "Large - Hungry Kings 🤴")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()

# 3. ASK PREFERENCE
elif st.session_state.step == "ASK_PREFERENCE":
    if len(st.session_state.chat_history) < 5:
        msg = "Perfect 🍽️ 👉 **Please choose your food preference:**"
        add_message("assistant", msg)
        st.rerun()

    col1, col2 = st.columns(2)
    if col1.button("🥦 Veg"):
        st.session_state.order_details["preference"] = "Veg"
        st.session_state.order_details["timing"] = get_current_meal_time()
        add_message("user", "Veg")
        st.session_state.step = "CHECKOUT"
        st.rerun()
    if col2.button("🍗 Non-Veg"):
        st.session_state.order_details["preference"] = "Non-Veg"
        st.session_state.order_details["timing"] = get_current_meal_time()
        add_message("user", "Non-Veg")
        st.session_state.step = "CHECKOUT"
        st.rerun()

# 4. CHECKOUT
elif st.session_state.step == "CHECKOUT":
    pref = st.session_state.order_details.get("preference", "Veg")
    timing = st.session_state.order_details.get("timing", "Dinner")
    num_people = st.session_state.order_details.get("people", 1)
    
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    if last_msg in ["Veg", "Non-Veg"]:
        msg = f"🍽️ Perfect! I've prepared a **{timing}** package for {num_people} people. ✨"
        add_message("assistant", msg)
        st.rerun()

    # --- Bundle Calculation ---
    available_items = MENU[timing][pref]
    used_items = []
    
    appetite = st.session_state.order_details.get("appetite", "Medium")
    if "Low" in appetite:
        portion_factor = 0.7
    elif "Large" in appetite:
        portion_factor = 1.3
    else:
        portion_factor = 1.0

    def get_unique_items(keywords, count):
        selected = []
        for item in available_items:
            if any(k.lower() in item["name"].lower() for k in keywords) and item["name"] not in [i["name"] for i in used_items]:
                selected.append(item); used_items.append(item)
                if len(selected) == count: return selected
        for item in available_items:
            if item["name"] not in [i["name"] for i in used_items]:
                selected.append(item); used_items.append(item)
                if len(selected) == count: return selected
        return selected

    # Get categorized items
    roti_list = get_unique_items(["Roti", "Naan", "Dosa", "Paratha", "Bhature"], 1)
    # Give fewer varieties of curries/rice to avoid overwhelming the order
    curry_list = get_unique_items(["Curry", "Paneer", "Kofta", "Masala", "Tikka"], 2 if num_people >= 6 else 1)
    rice_list = get_unique_items(["Rice", "Biryani", "Pallav", "Poha"], 1)
    sweet_list = [next((item for item in MENU["Sweets"] if "Jamun" in item["name"]), MENU["Sweets"][0])]

    # Build the final bundle for the cart with improved portion logic
    bundle = []
    
    # Roti/Bread: 1 per person adjusted by appetite
    if roti_list:
        bundle.append({"item": roti_list[0], "qty": max(1, round(num_people * portion_factor))})
    
    # Curries: 1 bowl per 2-3 people
    if curry_list:
        total_curry_qty = max(1, round((num_people * portion_factor) / 2.5))
        qty_per_curry = max(1, total_curry_qty // len(curry_list))
        for c in curry_list:
            bundle.append({"item": c, "qty": qty_per_curry})

    # Rice: 1 plate per 3 people if roti is present, else 1 per person
    if rice_list:
        rice_div = 3.0 if roti_list else 1.2
        bundle.append({"item": rice_list[0], "qty": max(1, round((num_people * portion_factor) / rice_div))})

    # Sweets: 1 per person
    if sweet_list:
        bundle.append({"item": sweet_list[0], "qty": max(1, round(num_people * portion_factor))})

    # Auto-fill the cart
    st.session_state.order_details["cart"] = {}
    for rec in bundle:
        item_data = rec["item"].copy()
        item_data["quantity"] = rec["qty"]
        st.session_state.order_details["cart"][item_data["name"]] = item_data

    # --- UI: Cart Display with WORKING buttons ---
    current_meal = get_current_meal_time()
    st.markdown(f"### 🍱 Recommended Package for {num_people} People")
    st.markdown(f"#### 🕐 {current_meal}")
    
    total_price = 0
    cart = st.session_state.order_details["cart"]
    
    if not cart:
        st.write("Your cart is empty.")
    else:
        for item_name, item_data in cart.items():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
                
                with col1:
                    st.image(item_data["image"], width=70)
                
                with col2:
                    st.markdown(f"#### {item_data['name']}")
                
                with col3:
                    # Working minus button
                    if st.button("➖", key=f"minus_{item_name}"):
                        if item_data["quantity"] > 1:
                            item_data["quantity"] -= 1
                            st.session_state.order_details["cart"][item_name] = item_data
                            st.rerun()
                
                with col4:
                    st.markdown(f"**{item_data['quantity']}**")
                
                with col5:
                    # Working plus button
                    if st.button("➕", key=f"plus_{item_name}"):
                        item_data["quantity"] += 1
                        st.session_state.order_details["cart"][item_name] = item_data
                        st.rerun()
                
                # Delete button in separate container
                if st.button("🗑️ Delete", key=f"delete_{item_name}"):
                    del st.session_state.order_details["cart"][item_name]
                    st.rerun()
                
                # Price display
                st.markdown(f"**₹{item_data['price'] * item_data['quantity']}**")
                
                total_price += item_data["price"] * item_data["quantity"]
    
    st.markdown(f"### Total Amount: ₹{total_price}")
    st.markdown("---")

    if st.button("Start New Order"):
        st.session_state.clear()
        st.rerun()
