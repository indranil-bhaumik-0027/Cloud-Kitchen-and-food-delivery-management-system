import streamlit as st
from utils.db_connection import run_query, execute_query

st.header("🏬 Manage Restaurants")

st.subheader("All Restaurants")
restaurants = run_query("SELECT * FROM Restaurants")
st.dataframe(restaurants, use_container_width=True)

st.divider()
st.subheader("➕ Add New Restaurant")
with st.form("add_restaurant"):
    name = st.text_input("Restaurant Name")
    cuisine = st.text_input("Cuisine Type")
    location = st.text_input("Location")
    submitted = st.form_submit_button("Add Restaurant")
    if submitted:
        if name and cuisine and location:
            success = execute_query(
                "INSERT INTO Restaurants (name, cuisine_type, location) VALUES (%s, %s, %s)",
                (name, cuisine, location)
            )
            if success:
                st.success(f"✅ '{name}' added successfully!")
                st.rerun()
        else:
            st.warning("Please fill in all fields.")

st.divider()
st.subheader("📋 View Menu by Restaurant")
if not restaurants.empty:
    selected_id = st.selectbox(
        "Select Restaurant",
        restaurants["restaurant_id"],
        format_func=lambda x: restaurants.loc[restaurants["restaurant_id"] == x, "name"].values[0]
    )
    menu = run_query("SELECT * FROM Menus WHERE restaurant_id = %s", (int(selected_id),))
    st.dataframe(menu, use_container_width=True)
else:
    st.info("No restaurants found. Add one above.")
st.divider()
st.subheader("🍽️ Add Menu Item")
if not restaurants.empty:
    menu_restaurant_id = st.selectbox(
        "Restaurant",
        restaurants["restaurant_id"],
        format_func=lambda x: restaurants.loc[restaurants["restaurant_id"] == x, "name"].values[0],
        key="menu_restaurant_select"
    )
    with st.form("add_menu_item"):
        item_name = st.text_input("Item Name")
        price = st.number_input("Price (₹)", min_value=0.0, step=10.0)
        category = st.text_input("Category (e.g. Starter, Main Course, Dessert)")
        submitted = st.form_submit_button("Add Item")
        if submitted:
            if item_name and category:
                execute_query(
                    "INSERT INTO Menus (restaurant_id, item_name, price, category) VALUES (%s, %s, %s, %s)",
                    (int(menu_restaurant_id), item_name, price, category)
                )
                st.success(f"✅ '{item_name}' added to menu!")
                st.rerun()
            else:
                st.warning("Please fill in item name and category.")