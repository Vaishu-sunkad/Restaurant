import streamlit as st
import time
import random

# --- Configuration ---
st.set_page_config(page_title="Foodie Hub", page_icon="🍽️", layout="wide")

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
    st.rerun()

# --- Menu Data ---
MENU = {
    "Veg": [
        {"name": "Veg Biryani", "price": 280, "image": "https://genv.org/wp-content/uploads/2023/02/17-Vegetable-Biryani.jpg"},
        {"name": "Dal Tadka", "price": 220, "image": "https://manjulaskitchen.com/wp-content/uploads/dal_fry_dal_tadka-1024x576.jpg"},
        {"name": "Butter Naan (2 pcs)", "price": 90, "image": "https://allmomsrecipes.com/wp-content/uploads/2025/02/u9552142339_httpss.mj_.runhuTKdwV8Ako_Amateur_close-up_from_re_b3707721-3b44-4310-bf5f-b80db0785fc2_2.jpg"},
        {"name": "Paneer Tikka", "price": 290, "image": "https://img.freepik.com/premium-photo/paneer-tikka-is-indian-dish-made-from-chunks-cottage-cheese-marinated-spices-grilled-tandoor_466689-76784.jpg?w=2000"},
        {"name": "Mushroom Masala", "price": 310, "image": "https://vismaifood.com/storage/app/uploads/public/274/0cf/870/thumb__700_0_0_0_auto.jpg"},
        {"name": "Malai Kofta", "price": 330, "image": "https://recetinas.com/wp-content/uploads/2022/07/malai-kofta-1024x682.jpg"},
        {"name": "Veg Fried Rice", "price": 240, "image": "https://placehold.co/600x400?text=Veg+Fried+Rice"},
    ],
    "Non-Veg": [
        {"name": "Chicken Curry", "price": 350, "image": "https://placehold.co/600x400?text=Chicken+Curry"},
        {"name": "Chicken Biryani", "price": 300, "image": "https://placehold.co/600x400?text=Chicken+Biryani"},
        {"name": "Mutton Rogan Josh", "price": 450, "image": "https://placehold.co/600x400?text=Mutton+Rogan+Josh"},
        {"name": "Tandoori Chicken", "price": 280, "image": "https://placehold.co/600x400?text=Tandoori+Chicken"},
        {"name": "Fish Curry", "price": 380, "image": "https://placehold.co/600x400?text=Fish+Curry"},
        {"name": "Prawns Masala", "price": 420, "image": "https://placehold.co/600x400?text=Prawns+Masala"},
        {"name": "Grilled Chicken", "price": 320, "image": "https://placehold.co/600x400?text=Grilled+Chicken"},
        {"name": "Egg Curry", "price": 210, "image": "https://placehold.co/600x400?text=Egg+Curry"},
    ]
}

# --- Sidebar / Header ---
st.title("🍽️ Foodie Hub")
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

    st.write("Please choose one:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🟢 Low (Light eaters)"):
        st.session_state.order_details["appetite"] = "Low"
        add_message("user", "Low")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col2.button("🟡 Medium (Normal appetite)"):
        st.session_state.order_details["appetite"] = "Medium"
        add_message("user", "Medium")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()
    if col3.button("🔴 Large (Heavy eaters)"):
        st.session_state.order_details["appetite"] = "Large"
        add_message("user", "Large")
        st.session_state.step = "ASK_PREFERENCE"
        st.rerun()

# 3. ASK PREFERENCE
elif st.session_state.step == "ASK_PREFERENCE":
    if len(st.session_state.chat_history) < 5:
        msg = "Perfect 👍\n\n👉 **Please choose your food preference:**"
        add_message("assistant", msg)
        st.rerun()

    col1, col2 = st.columns(2)
    if col1.button("🥦 Veg"):
        st.session_state.order_details["preference"] = "Veg"
        add_message("user", "Veg")
        st.session_state.step = "SHOW_MENU"
        st.rerun()
    if col2.button("🍗 Non-Veg"):
        st.session_state.order_details["preference"] = "Non-Veg"
        add_message("user", "Non-Veg")
        st.session_state.step = "SHOW_MENU"
        st.rerun()

# 4. SHOW MENU
elif st.session_state.step == "SHOW_MENU":
    pref = st.session_state.order_details["preference"]
    
    last_msg = st.session_state.chat_history[-1]["content"] if st.session_state.chat_history else ""
    if last_msg in ["Veg", "Non-Veg"]:
        msg = f"🥦 **{pref} Menu** (Recommended for {st.session_state.order_details['people']} people – {st.session_state.order_details['appetite']} appetite)"
        add_message("assistant", msg)
        st.rerun()

    # --- Menu Grid ---
    st.markdown("### Menu")
    items = MENU[pref]
    
    # Use 2 columns grid for menu items
    for i in range(0, len(items), 2):
        col1, col2 = st.columns(2)
        
        # Item 1
        with col1:
            item = items[i]
            st.image(item["image"], use_container_width=True)
            st.subheader(item["name"])
            st.write(f"₹{item['price']}")
            if st.button(f"Add {item['name']}", key=item["name"]):
                cart = st.session_state.order_details["cart"]
                if item["name"] in cart:
                    cart[item["name"]]["quantity"] += 1
                else:
                    item_data = item.copy()
                    item_data["quantity"] = 1
                    cart[item["name"]] = item_data
                st.toast(f"✅ {item['name']} added/updated!")
                st.rerun()
        
        # Item 2
        with col2:
            if i + 1 < len(items):
                item = items[i+1]
                st.image(item["image"], use_container_width=True)
                st.subheader(item["name"])
                st.write(f"₹{item['price']}")
                if st.button(f"Add {item['name']}", key=item["name"]):
                    cart = st.session_state.order_details["cart"]
                    if item["name"] in cart:
                        cart[item["name"]]["quantity"] += 1
                    else:
                        item_data = item.copy()
                        item_data["quantity"] = 1
                        cart[item["name"]] = item_data
                    st.toast(f"✅ {item['name']} added/updated!")
                    st.rerun()

    st.markdown("---")
    
    # --- Cart Section ---
    cart = st.session_state.order_details["cart"]
    if cart:
        with st.expander("🛒 Your Cart", expanded=True):
            st.markdown("### Cart Items")
            for item_name, item_data in cart.items():
                c1, c2, c3, c4, c5 = st.columns([1, 2, 1.5, 1, 0.5])
                
                with c1:
                    st.image(item_data["image"])
                with c2:
                    st.write(f"**{item_data['name']}**")
                    st.write(f"₹{item_data['price']}")
                with c3:
                    # Quantity Controls
                    qc1, qc2, qc3 = st.columns([1, 1, 1])
                    if qc1.button("➖", key=f"dec_{item_name}"):
                        update_cart(item_name, "decrease")
                    with qc2:
                         st.write(f"{item_data['quantity']}")
                    if qc3.button("➕", key=f"inc_{item_name}"):
                        update_cart(item_name, "increase")
                with c4:
                    st.write(f"**₹{item_data['price'] * item_data['quantity']}**")
                with c5:
                    if st.button("🗑️", key=f"del_{item_name}"):
                        update_cart(item_name, "delete")
            
            total_price = sum(item['price'] * item['quantity'] for item in cart.values())
            st.markdown(f"### Total: ₹{total_price}")

    if st.button("🛒 Proceed to Checkout"):
        if not cart:
            st.toast("Please add items to your cart first!")
        else:
            st.session_state.step = "CHECKOUT"
            st.rerun()

# 5. CHECKOUT / AUTH
elif st.session_state.step == "CHECKOUT":
    if st.session_state.chat_history[-1]["content"].startswith("🥦"): # Check if coming from menu
         msg = "🔐 **To place your order, please sign up or log in.**"
         add_message("assistant", msg)
         st.rerun()
         
    st.write("Choose an option:")
    if st.button("📱 Sign up with Mobile Number"):
        st.session_state.step = "AUTH_MOBILE"
        add_message("user", "Sign up with Mobile Number")
        st.rerun()
    
    if st.button("📧 Sign up with Email"):
        st.info("Email signup not implemented in this demo.")
        
    if st.button("🔑 Login (Existing user)"):
        st.info("Login not implemented in this demo.")

# 6. ENTER MOBILE
elif st.session_state.step == "AUTH_MOBILE":
    if st.session_state.chat_history[-1]["content"] == "Sign up with Mobile Number":
         add_message("assistant", "📱 Please enter your mobile number:")
         st.rerun()

    mobile = st.chat_input("Enter Mobile Number")
    if mobile:
        add_message("user", mobile)
        st.session_state.order_details["mobile"] = mobile
        st.session_state.step = "AUTH_OTP"
        st.rerun()

# 7. ENTER OTP
elif st.session_state.step == "AUTH_OTP":
    mobile = st.session_state.order_details.get("mobile", "your number")
    last_user_msg = [m for m in st.session_state.chat_history if m["role"] == "user"][-1]["content"]
    if last_user_msg == mobile:
        add_message("assistant", f"🔐 OTP sent to {mobile}\n\nPlease enter the OTP (use 123456):")
        st.rerun()

    otp = st.chat_input("Enter OTP")
    if otp:
        add_message("user", otp)
        if otp == "123456":
            st.session_state.step = "CONFIRMATION"
            st.rerun()
        else:
            st.error("Invalid OTP. Try 123456.")

# 8. CONFIRMATION
elif st.session_state.step == "CONFIRMATION":
    if st.session_state.chat_history[-1]["content"] == "123456":
         msg = "✅ Signup successful! 🎉\n\n**🛒 Order Summary**"
         add_message("assistant", msg)
         
         cart = st.session_state.order_details['cart']
         total = sum([item['price'] * item['quantity'] for item in cart.values()])
         
         summary_items = ""
         for item in cart.values():
             summary_items += f"- {item['name']} x {item['quantity']} (₹{item['price'] * item['quantity']})\n"

         summary = f"""
         **Items:**
         {summary_items}
         
         **Total:** ₹{total}
         
         👥 People: {st.session_state.order_details['people']}
         🍽️ Appetite: {st.session_state.order_details['appetite']}
         🥦 Preference: {st.session_state.order_details['preference']}
         
         👉 **Confirm order?**
         """
         add_message("assistant", summary)
         st.rerun()

    c1, c2 = st.columns(2)
    if c1.button("✅ Yes, Place Order"):
        st.session_state.step = "SUCCESS"
        add_message("user", "Yes")
        st.rerun()
    if c2.button("❌ Modify Order"):
        st.session_state.step = "SHOW_MENU"
        add_message("user", "Modify")
        st.rerun()

# 9. SUCCESS
elif st.session_state.step == "SUCCESS":
    if st.session_state.chat_history[-1]["content"] == "Yes":
        msg = "🎉 **Order Placed Successfully!**\n\n⏱️ Estimated delivery: 35 minutes\n📍 Track your order anytime from My Orders\n\nThank you for ordering with Foodie Hub 🍴😊"
        add_message("assistant", msg)
        st.balloons()
        st.rerun() 
    
    if st.button("Start New Order"):
        st.session_state.clear()
        st.rerun()
