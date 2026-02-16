import streamlit as st

# Simple Foodie Hub App
st.title("🍽️ Foodie Hub")

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = {
        "Veg Biryani": {"name": "Veg Biryani", "price": 280, "image": "https://img.freepik.com/premium-photo/traditional-indian-veg-biryani-banana-leaf_1179130-190160.jpg", "quantity": 2},
        "Palak Paneer": {"name": "Palak Paneer with chapathi", "price": 220, "image": "https://img.freepik.com/premium-photo/indian-palak-paneer-with-spinach-cottage-cheese_1072167-2540.jpg", "quantity": 1}
    }

st.write("### 🛒 Your Cart")

# Display cart items with working buttons
for item_name, item_data in list(st.session_state.cart.items()):
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
        
        with col1:
            st.image(item_data["image"], width=70)
        
        with col2:
            st.markdown(f"#### {item_data['name']}")
        
        with col3:
            if st.button("➖", key=f"minus_{item_name}"):
                if st.session_state.cart[item_name]["quantity"] > 1:
                    st.session_state.cart[item_name]["quantity"] -= 1
                    st.rerun()
        
        with col4:
            st.markdown(f"**{st.session_state.cart[item_name]['quantity']}**")
        
        with col5:
            if st.button("➕", key=f"plus_{item_name}"):
                st.session_state.cart[item_name]["quantity"] += 1
                st.rerun()
        
        # Delete button
        if st.button("🗑️ Delete", key=f"delete_{item_name}"):
            if item_name in st.session_state.cart:
                del st.session_state.cart[item_name]
                st.rerun()
        
        # Price display
        st.markdown(f"**₹{item_data['price'] * st.session_state.cart[item_name]['quantity']}**")

# Calculate and display total
total_price = sum(item_data["price"] * item_data["quantity"] for item_data in st.session_state.cart.values())
st.markdown("---")
st.markdown(f"### 💰 Total Amount: ₹{total_price}")

# Reset button
if st.button("🔄 Reset Cart"):
    st.session_state.cart = {}
    st.rerun()
