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
        response = requests.get(f"{BACKEND_URL}/")
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

# --- Custom CSS (Beauty & Attraction) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    :root {
        --primary: #FF4B2B;
        --secondary: #FF416C;
        --accent: #6C63FF;
        --bg-color: #ffffff;
        --text-color: #1a1a1a;
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-border: rgba(255, 255, 255, 0.3);
    }

    /* Full Page - Aurora Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Outfit', sans-serif;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Overlay to adjust brightness for readability */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.4); /* Light overlay to keep text black and clear */
        z-index: -1;
    }

    /* Floating Background Circles for depth */
    .stApp::after {
        content: '';
        position: fixed;
        width: 100%; height: 100%;
        top: 0; left: 0;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(255,255,255,0.4) 0%, transparent 20%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.3) 0%, transparent 30%),
            radial-gradient(circle at 50% 50%, rgba(255,255,255,0.2) 0%, transparent 50%);
        z-index: -1;
        pointer-events: none;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 3rem;
        max-width: 1300px;
    }

    /* Header Styling with 3D Effect */
    h1 {
        font-weight: 880 !important;
        color: #1a1a1a !important;
        text-align: center;
        font-size: 5rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase;
        letter-spacing: -2px;
        line-height: 1 !important;
        text-shadow: 2px 2px 0px #fff, 4px 4px 0px rgba(0,0,0,0.1);
    }

    /* Force all text to DEEP BLACK for perfect visibility */
    p, span, label, div, h2, h3, h4, li, small {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Sidebar - Ultra Glass */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(255, 255, 255, 0.5);
    }

    /* Button Styling - The 'Popping' Look */
    .stButton > button {
        width: 100%;
        border-radius: 50px !important;
        border: none !important;
        background: linear-gradient(90deg, #1a1a1a 0%, #333333 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
        background: #000000 !important;
    }

    /* Input Fields - High Contrast */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #000000 !important;
        border-radius: 15px !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 1.2rem !important;
    }

    /* Chat Messages - Floating Glass */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 15px 45px rgba(0,0,0,0.1) !important;
        backdrop-filter: blur(10px);
    }

    /* Package/Bundle Card - Modern & Bold */
    .bundle-card {
        background: #ffffff !important;
        border-radius: 25px;
        padding: 3rem;
        border: 2px solid #000000;
        box-shadow: 15px 15px 0px #000000;
        margin-bottom: 3rem;
        transition: all 0.3s ease;
    }

    .bundle-card:hover {
        transform: translate(-5px, -5px);
        box-shadow: 20px 20px 0px #000000;
    }

    /* Images */
    img {
        border-radius: 20px;
        border: 3px solid #000000;
    }

</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = "GREETING"
if "order_details" not in st.session_state:
    st.session_state.order_details = {
        "people": 4,
        "appetite": None,
        "preference": None,
        "cart": {} # Changed to dict for quantity tracking
    }
# Migration check (if user reloads and has old list structure)
if isinstance(st.session_state.order_details["cart"], list):
    st.session_state.order_details["cart"] = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Helper Functions ---
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def update_cart(item_name, action):
    cart = st.session_state.order_details["cart"]
    if item_name in cart:
        if action == "increase":
            cart[item_name]["quantity"] += 1
        elif action == "decrease":
            if cart[item_name]["quantity"] > 1:
                cart[item_name]["quantity"] -= 1
        elif action == "delete":
            del cart[item_name]

def place_order_to_backend(payment_method, payment_details=None):
    if not backend_available:
        st.error("❌ Backend is offline. Cannot place order.")
        return
    
    cart = st.session_state.order_details["cart"]
    total = sum([item["price"] * item["quantity"] for item in cart.values()])
    
    order_payload = {
        "mobile": st.session_state.order_details.get("mobile"),
        "email": st.session_state.order_details.get("email"),
        "cart": cart,
        "total": float(total),
        "people": int(st.session_state.order_details["people"]),
        "appetite": st.session_state.order_details["appetite"],
        "preference": st.session_state.order_details["preference"],
        "payment_method": payment_method,
        "payment_details": payment_details
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/order/place", json=order_payload)
        if response.status_code == 200:
            st.toast("✅ Order saved to database!")
        else:
            st.error(f"❌ Backend Error: {response.text}")
    except Exception as e:
        st.error(f"❌ Connection Error: {str(e)}")

# --- Menu Data ---
MENU = {
    "Morning (Breakfast)": {
        "Veg": [
            {"name": "Masala Dosa", "price": 120, "image": "https://wallpaperaccess.com/full/6340448.jpg"},
            {"name": "Idli Vada", "price": 80, "image": "https://as1.ftcdn.net/v2/jpg/04/65/28/88/1000_F_465288827_zBiEkbK8VxEspw2DY2sKMN4U6hgCpIDN.jpg"},
            {"name": "Poha", "price": 60, "image": "https://thumbs.dreamstime.com/b/poha-23333662.jpg"},
            {"name": "Chole bhature", "price": 100, "image": "https://i0.wp.com/bakaasur.com/wp-content/uploads/2022/12/chole-bhature.jpg?w=1200&ssl=1"},
            {"name": "Bonda", "price": 70, "image": "https://www.masalakorb.com/wp-content/uploads/2023/02/EASY-MYSORE-BONDA-RECIPE-MAIDA-BONDA-MYSORE-BAJJI-V1.jpg"}
        ],
        "Non-Veg": [
            {"name": "Bread Omelette", "price": 80, "image": "https://tse2.mm.bing.net/th/id/OIP.0G9LjhrRb4VglpXOs54JigHaEK?pid=Api&P=0&h=180"},
            {"name": "Chicken Keema Paratha", "price": 180, "image": "https://1.bp.blogspot.com/-bFuZOx0Aoa4/XP8CVnIxGAI/AAAAAAAAZK4/DsSMVFOgv7gcHpZWDnqYz-a0VMKRgPD-QCLcBGAs/s1600/20190601_173704.jpg"},
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
            {"name": "South Indian Thali", "price": 320, "image": "https://wp.scoopwhoop.com/wp-content/uploads/2014/09/567731556e510a6f3a759a4d_south.jpg"},
            {"name": "Pallav", "price": 70, "image": "https://1.bp.blogspot.com/-Yf00fooZes8/WrMJKwxMVOI/AAAAAAAAgtg/32-H3Ym2iDk-enkac6zUIuRGneGk3vyoQCEwYBhgL/w1200-h630-p-k-no-nu/226.jpg"}
        ],
        "Non-Veg": [
           {"name": "Chicken Biryani", "price": 300, "image": "https://static.vecteezy.com/system/resources/previews/040/703/949/non_2x/ai-generated-royal-feast-master-the-art-of-chicken-biryani-at-home-generative-ai-photo.jpg"},
           {"name": "Mutton Curry", "price": 450, "image": "https://uploads-ssl.webflow.com/5c481361c604e53624138c2f/60f2eb0d5d007bd81723ebe2_Mutton%20curry_1500%20x%201200.jpg"},
           {"name": "Fish Curry", "price": 380, "image": "https://paattiskitchen.com/wp-content/uploads/2023/01/kmc_20230110_191241-1.jpg"},
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
            text = "👋 Welcome to Foodie Hub! I’ll help you place your order quickly 😊\n\nBefore we start, I need a few details.\n\n👉 **How many people are dining today?**"
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
        msg = f"Great! 👨👩👧👦 for {st.session_state.order_details['people']} people.\n\n👉 **What is your eating capacity?**"
        add_message("assistant", msg)
        st.rerun()

    st.write("Please choose your eating style:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🥗 **Low**\n(Light eaters 🧒)"):
        st.session_state.order_details["appetite"] = "Low"
        add_message("user", "Low - Light eaters 🧒")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col2.button("🍱 **Medium**\n(Standard Foodie 🧔)"):
        st.session_state.order_details["appetite"] = "Medium"
        add_message("user", "Medium - Standard Foodie 🧔")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col3.button("🍖 **Large**\n(Hungry Kings 🤴)"):
        st.session_state.order_details["appetite"] = "Large"
        add_message("user", "Large - Hungry Kings 🤴")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()



# 3. ASK PREFERENCE
elif st.session_state.step == "ASK_PREFERENCE":
    if len(st.session_state.chat_history) < 5:
        msg = "Perfect 🍽️\n\n👉 **Please choose your food preference:**"
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

# 4. CHECKOUT (Shows Bundle + Login Options Directly)
elif st.session_state.step == "CHECKOUT":
    pref = st.session_state.order_details.get("preference", "Veg")
    timing = st.session_state.order_details.get("timing", "Dinner")
    num_people = st.session_state.order_details.get("people", 1)
    
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    if last_msg in ["Veg", "Non-Veg"]:
        msg = f"🍽️ Perfect! I've prepared a **{timing}** package for {num_people} people. ✨\n\n🔐 Please login or sign up to complete your order."
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

    # --- UI: Bundle Display ---
    st.markdown(f"<div class='bundle-card'>### 🍱 Recommended Package for {num_people} People</div>", unsafe_allow_html=True)
    total_price = 0
    for rec in bundle:
        with st.container():
            c1, c2, c3 = st.columns([1, 4, 1])
            with c1: st.image(rec["item"]["image"], width=70)
            with c2: st.markdown(f"#### {rec['item']['name']}\nQuantity: **{rec['qty']}**")
            with c3:
                price = rec['item']['price'] * rec['qty']
                st.markdown(f"### ₹{price}")
                total_price += price
    
    st.markdown(f"<div style='text-align: right; font-size: 1.5rem; font-weight: bold; color: #FF416C;'>Total Amount: ₹{total_price}</div>", unsafe_allow_html=True)
    st.markdown("---")

    # --- UI: Directly show Login options ---
    st.markdown("<h3 style='text-align: center;'>🔐 Secure Checkout</h3>", unsafe_allow_html=True)
    st.info("Please select an option to complete your order:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Email Sign-up"):
            st.session_state.step = "AUTH_EMAIL"
            add_message("user", "Sign up with Email")
            st.rerun()
    with col2:
        if st.button("🔑 Login"):
            st.session_state.step = "LOGIN_HOME"
            add_message("user", "Login")
            st.rerun()

# Step 6 and 7 (Mobile) removed per user request

# 7. PAYMENT
elif st.session_state.step == "PAYMENT":
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    
    # If we just arrived from login/signup, show the select payment message
    if last_msg == st.session_state.get("generated_otp") or "successful" in last_msg.lower():
        if not any(m["content"] == "💳 **Select Payment Method**" for m in st.session_state.chat_history):
            add_message("assistant", "💳 **Select Payment Method**")
            st.rerun()

    st.write("### Choose a payment method:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 UPI (GPay/PhonePe)"):
            add_message("user", "UPI")
            st.session_state.step = "PAYMENT_DETAILS_UPI"
            st.rerun()
            
    with col2:
        if st.button("💳 Credit/Debit Card"):
            add_message("user", "Card")
            st.session_state.step = "PAYMENT_DETAILS_CARD"
            st.rerun()
            
    with col3:
        if st.button("💵 Cash on Delivery"):
            add_message("user", "Cash on Delivery")
            place_order_to_backend("Cash on Delivery")
            st.session_state.step = "SUCCESS"
            st.rerun()

# 8. PAYMENT DETAILS (UPI)
elif st.session_state.step == "PAYMENT_DETAILS_UPI":
    st.write("### 📱 UPI Payment Details")
    upi_name = st.text_input("Full Name", key="pay_upi_name")
    upi_id = st.text_input("UPI ID (e.g., name@okaxis)", key="pay_upi_id")
    
    if st.button("Proceed to Pay ₹", type="primary"):
        if upi_name and upi_id:
            add_message("assistant", f"Processing UPI payment for {upi_name}...")
            place_order_to_backend("UPI", {"name": upi_name, "upi_id": upi_id})
            time.sleep(1.5)
            st.session_state.step = "SUCCESS"
            st.rerun()
        else:
            st.error("Please fill in all details.")

# 9. PAYMENT DETAILS (CARD)
elif st.session_state.step == "PAYMENT_DETAILS_CARD":
    st.write("### 💳 Card Payment Details")
    card_name = st.text_input("Cardholder Name", key="pay_card_name")
    card_no = st.text_input("Card Number", max_chars=16, key="pay_card_no")
    card_expiry = st.text_input("Expiry (MM/YY)", key="pay_card_expiry")
        
    if st.button("Securely Pay ₹", type="primary"):
        if card_name and card_no and card_expiry:
            add_message("assistant", f"Verifying card details for {card_name}...")
            # Send all details explicitly
            details = {
                "cardholder_name": card_name,
                "card_number": card_no,
                "expiry": card_expiry
            }
            place_order_to_backend("Credit/Debit Card", details)
            time.sleep(2)
            st.session_state.step = "SUCCESS"
            st.rerun()
        else:
            st.error("Please fill in all details.")

# 10. SUCCESS
elif st.session_state.step == "SUCCESS":
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    
    # Identify payment method from history
    payment_method = "Unknown"
    if "Cash on Delivery" in last_msg:
        payment_method = "Cash on Delivery"
    elif "Processing UPI" in last_msg:
        payment_method = "UPI"
    elif "Verifying card" in last_msg:
        payment_method = "Credit/Debit Card"

    if payment_method != "Unknown":
        if not any("Order Placed Successfully" in m["content"] for m in st.session_state.chat_history):
            msg = f"🎉 **Order Placed Successfully!**\n\nPayment Method: **{payment_method}**\n\n⏱️ Estimated delivery: 35 minutes\n📍 Track your order anytime from My Orders\n\nThank you for ordering with Foodie Hub 🍴😊"
            add_message("assistant", msg)
            st.balloons()
            st.rerun()
    
    if st.button("Start New Order"):
        st.session_state.clear()
        st.rerun()
        
# --- New Auth Steps ---
elif st.session_state.step == "AUTH_EMAIL":
    st.write("### Sign up with Email")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if email and password:
            st.session_state.temp_email = email
            st.session_state.temp_password = password
            st.session_state.generated_otp = str(random.randint(100000, 999999))
            st.session_state.step = "VERIFY_OTP_SIGNUP"
            st.rerun()
        else:
            st.error("Please enter email and password")

elif st.session_state.step == "VERIFY_OTP_SIGNUP":
    target_otp = st.session_state.get("generated_otp", "123456")
    st.info(f"📧 Verification code sent to {st.session_state.temp_email}")
    st.info(f"Demo OTP: **{target_otp}**")
    otp = st.text_input("Enter Email OTP", key="signup_otp")
    if st.button("Verify & Create Account"):
        if otp == target_otp:
            # Create user in backend
            if backend_available and db_connected:
                try:
                    resp = requests.post(f"{BACKEND_URL}/signup/email", json={
                        "email": st.session_state.temp_email, 
                        "password": st.session_state.temp_password
                    })
                except Exception:
                    pass
            st.session_state.order_details["email"] = st.session_state.temp_email
            st.success("Account verified! Proceeding...")
            time.sleep(1)
            st.session_state.step = "PAYMENT"
            st.rerun()
        else:
            st.error(f"Invalid OTP. Use {target_otp}")
                
elif st.session_state.step == "LOGIN_HOME":
    st.write("### Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", key="login_pass", type="password")
    if st.button("Login", key="login_email_btn"):
        if backend_available and db_connected:
            try:
                resp = requests.post(f"{BACKEND_URL}/login/email", json={"email": email, "password": password})
                if resp.status_code == 200:
                    st.session_state.temp_email = email
                    st.session_state.generated_otp = str(random.randint(100000, 999999))
                    st.session_state.step = "VERIFY_OTP_LOGIN"
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            except Exception:
                st.error("Backend error")
        else:
            # Fallback for offline mode
            st.session_state.temp_email = email
            st.session_state.generated_otp = str(random.randint(100000, 999999))
            st.session_state.step = "VERIFY_OTP_LOGIN"
            st.rerun()

elif st.session_state.step == "VERIFY_OTP_LOGIN":
    target_otp = st.session_state.get("generated_otp", "123456")
    st.info(f"🔓 Security check: OTP sent to {st.session_state.temp_email}")
    st.info(f"Demo OTP: **{target_otp}**")
    otp = st.text_input("Enter Login OTP", key="login_otp")
    if st.button("Verify & Sign In"):
        if otp == target_otp:
             st.session_state.order_details["email"] = st.session_state.temp_email
             st.session_state.step = "PAYMENT"
             st.rerun()
        else:
            st.error(f"Invalid OTP. Use {target_otp}")

# Step LOGIN_OTP removed per user request
