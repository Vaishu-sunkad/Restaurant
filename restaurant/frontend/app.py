import streamlit as st

# Minimal working cart app
st.title("🍽️ Foodie Hub")

# Initialize cart with sample data
if "cart" not in st.session_state:
    st.session_state.cart = {
        "Veg Biryani": {"name": "Veg Biryani", "price": 280, "image": "https://img.freepik.com/premium-photo/traditional-indian-veg-biryani-banana-leaf_1179130-190160.jpg", "quantity": 2},
        "Palak Paneer": {"name": "Palak Paneer", "price": 220, "image": "https://img.freepik.com/premium-photo/indian-palak-paneer-with-spinach-cottage-cheese_1072167-2540.jpg", "quantity": 1}
    }

st.write("### 🛒 Your Cart")

# Process button clicks
if "action" not in st.session_state:
    st.session_state.action = None

# Check for button actions
for item_name in list(st.session_state.cart.keys()):
    # Check minus button
    if st.session_state.action == f"minus_{item_name}":
        if st.session_state.cart[item_name]["quantity"] > 1:
            st.session_state.cart[item_name]["quantity"] -= 1
        st.session_state.action = None
        st.rerun()
    
    # Check plus button
    if st.session_state.action == f"plus_{item_name}":
        st.session_state.cart[item_name]["quantity"] += 1
        st.session_state.action = None
        st.rerun()
    
    # Check delete button
    if st.session_state.action == f"delete_{item_name}":
        del st.session_state.cart[item_name]
        st.session_state.action = None
        st.rerun()

# Display cart items
total_price = 0
for item_name, item_data in list(st.session_state.cart.items()):
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
        
        with col1:
            st.image(item_data["image"], width=70)
        
        with col2:
            st.markdown(f"#### {item_data['name']}")
        
        with col3:
            if st.button("➖", key=f"minus_{item_name}"):
                st.session_state.action = f"minus_{item_name}"
        
        with col4:
            st.markdown(f"**{item_data['quantity']}**")
        
        with col5:
            if st.button("➕", key=f"plus_{item_name}"):
                st.session_state.action = f"plus_{item_name}"
        
        # Delete button in separate row
        if st.button("🗑️ Delete", key=f"delete_{item_name}"):
            st.session_state.action = f"delete_{item_name}"
        
        # Price display
        st.markdown(f"**₹{item_data['price'] * item_data['quantity']}**")
        
        total_price += item_data["price"] * item_data["quantity"]

# Display total
st.markdown("---")
st.markdown(f"### 💰 Total Amount: ₹{total_price}")

# Debug section
st.markdown("---")
st.write("### 🔍 Debug Info")
st.write(f"Cart items: {len(st.session_state.cart)}")
for name, data in st.session_state.cart.items():
    st.write(f"- {name}: {data['quantity']} x ₹{data['price']}")

# Reset button
if st.button("🔄 Reset Cart"):
    st.session_state.cart = {}
    st.rerun()
