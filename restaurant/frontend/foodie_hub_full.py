import streamlit as st
import pytz
from datetime import datetime

# Configuration
st.set_page_config(page_title="Foodie Hub | Premium Dining", page_icon="🍽️", layout="wide")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "GREETING"
if "order_details" not in st.session_state:
    st.session_state.order_details = {
        "people": 4,
        "appetite": None,
        "preference": None,
        "cart": {}
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Helper functions
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

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

# Menu data
MENU = {
    "Morning (Breakfast)": {
        "Veg": [
            {"name": "Masala Dosa", "price": 120, "image": "https://wallpaperaccess.com/full/6340448.jpg"},
            {"name": "Idli Vada", "price": 80, "image": "https://as1.ftcdn.net/v2/jpg/04/65/28/88/1000_F_465288827_zBiEkb_660x660.jpg"},
            {"name": "Poha", "price": 60, "image": "https://thumbs.dreamstime.com/b/poha-23333662.jpg"}
        ],
        "Non-Veg": [
            {"name": "Bread Omelette", "price": 80, "image": "https://tse2.mm.bing.net/th/id/OIP.0G9LjhrRb4VglpXOs54JjAHaKX?pid=Api&P=0&h=180"},
            {"name": "Egg Bhurji", "price": 90, "image": "http://eggcellent.recipes/wp-content/uploads/2024/08/Indian-Egg-Bhurji-Recipe-1024x1024.png"}
        ]
    },
    "Afternoon (Lunch)": {
        "Veg": [
            {"name": "Veg Biryani", "price": 280, "image": "https://img.freepik.com/premium-photo/traditional-indian-veg-biryani-banana-leaf_1179130-190160.jpg?w=2000"},
            {"name": "Palak Paneer with chapathi", "price": 220, "image": "https://img.freepik.com/premium-photo/indian-palak-paneer-with-spinach-cottage-cheese_1072167-2540.jpg?w=2000"}
        ],
        "Non-Veg": [
            {"name": "Chicken Biryani", "price": 300, "image": "https://static.vecteezy.com/system/resources/previews/040/703/949/non_2x/ai-generated-royal-feast-master-the-art-of-chicken-biryani-at-home-generative-ai-photo.jpg"},
            {"name": "Egg Curry", "price": 210, "image": "https://static.vecteezy.com/system/resources/previews/050/436/451/large_2x/spicy-indian-egg-curry-served-parathas-garnished-with-fresh-coriander-and-a-side-of-raita-photo.jpg"}
        ]
    },
    "Evening (Snacks)": {
        "Veg": [
            {"name": "Paneer Tikka", "price": 290, "image": "https://img.freepik.com/premium-photo/photography-tasty-indian-paneer-tikka_1288657-46631.jpg"},
            {"name": "Samosa (3 pcs)", "price": 50, "image": "https://thehimalayantreasure.pl/wp-content/uploads/2018/09/chicken-samosa.jpg"}
        ],
        "Non-Veg": [
            {"name": "Chicken Nuggets", "price": 200, "image": "http://www.proofdc.com/wp-content/uploads/media/02/58716144-crispy-baked-chicken-nuggets-recipe-proofdc.jpg"},
            {"name": "Egg Puff", "price": 50, "image": "https://nodashofgluten.com/wp-content/uploads/2025/02/Egg-Puff-Recipe-Kerala-Style-3.png.webp"}
        ]
    },
    "Night (Dinner)": {
        "Veg": [
            {"name": "Butter Naan & Paneer", "price": 350, "image": "https://media-cdn.tripadvisor.com/media/photo-m/1280/1a/54/fd/77/paneer-butter-masala.jpg"},
            {"name": "Veg Fried Rice", "price": 240, "image": "https://thedelishrecipe.com/wp-content/uploads/2024/05/vegetable-fried-rice.jpg"}
        ],
        "Non-Veg": [
            {"name": "Tandoori Chicken", "price": 280, "image": "https://img.freepik.com/premium-photo/indian-spices-barbecue-murgh-tandoori-tandoori-chicken-with-raita-lime-chapati-onion-rings-served-dish-isolated-dark-background-top-view-food_689047-1446.jpg?w=1380"},
            {"name": "Chicken Curry & Roti", "price": 320, "image": "https://themayakitchen.com/wp-content/uploads/2019/06/CURRY.jpg"}
        ]
    }
}

# Header
st.title("🍽️ Foodie Hub")
current_meal_time = get_current_meal_time()
st.markdown(f"### 🕐 {current_meal_time}")
st.markdown("---")

# Chat display
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# State machine logic

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

    # Auto-fill cart with sample items
    available_items = MENU[timing][pref]
    st.session_state.order_details["cart"] = {}
    
    # Add 2-3 items to cart
    for i, item in enumerate(available_items[:3]):
        item_data = item.copy()
        item_data["quantity"] = 1
        st.session_state.order_details["cart"][item_data["name"]] = item_data

    # Display cart
    st.markdown(f"### 🍱 Recommended Package for {num_people} People")
    st.markdown(f"#### 🕐 {timing}")
    
    total_price = 0
    cart = st.session_state.order_details["cart"]
    
    if not cart:
        st.write("Your cart is empty.")
    else:
        for item_name, item_data in list(cart.items()):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
                
                with col1:
                    st.image(item_data["image"], width=70)
                
                with col2:
                    st.markdown(f"#### {item_data['name']}")
                
                with col3:
                    if st.button("➖", key=f"minus_{item_name}"):
                        if st.session_state.order_details["cart"][item_name]["quantity"] > 1:
                            st.session_state.order_details["cart"][item_name]["quantity"] -= 1
                            st.rerun()
                
                with col4:
                    st.markdown(f"**{st.session_state.order_details['cart'][item_name]['quantity']}**")
                
                with col5:
                    if st.button("➕", key=f"plus_{item_name}"):
                        st.session_state.order_details["cart"][item_name]["quantity"] += 1
                        st.rerun()
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{item_name}"):
                    if item_name in st.session_state.order_details["cart"]:
                        del st.session_state.order_details["cart"][item_name]
                        st.rerun()
                
                # Price display
                st.markdown(f"**₹{item_data['price'] * st.session_state.order_details['cart'][item_name]['quantity']}**")
                
                total_price += item_data["price"] * st.session_state.order_details['cart'][item_name]['quantity']

    st.markdown(f"### Total Amount: ₹{total_price}")
    st.markdown("---")

    if st.button("Start New Order"):
        st.session_state.clear()
        st.rerun()
