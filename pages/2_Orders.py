import streamlit as st
from utils.db_connection import run_query, execute_query

st.header("📦 Manage Orders")

st.subheader("All Orders")
orders = run_query("SELECT * FROM Orders")
st.dataframe(orders, use_container_width=True)

st.divider()
st.subheader("➕ Place New Order")

customers = run_query("SELECT customer_id, name FROM Customers")
restaurants = run_query("SELECT restaurant_id, name FROM Restaurants")

if customers.empty or restaurants.empty:
    st.warning("Add at least one Customer and one Restaurant first.")
else:
    with st.form("add_order"):
        customer_id = st.selectbox(
            "Customer", customers["customer_id"],
            format_func=lambda x: customers.loc[customers["customer_id"] == x, "name"].values[0]
        )
        restaurant_id = st.selectbox(
            "Restaurant", restaurants["restaurant_id"],
            format_func=lambda x: restaurants.loc[restaurants["restaurant_id"] == x, "name"].values[0]
        )
        total_amount = st.number_input("Total Amount (₹)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("Place Order")
        if submitted:
            execute_query(
                "INSERT INTO Orders (customer_id, restaurant_id, total_amount, status) VALUES (%s, %s, %s, 'Placed')",
                (int(customer_id), int(restaurant_id), total_amount)
            )
            st.success("✅ Order placed!")
            st.rerun()

st.divider()
st.subheader("🔄 Update Order Status")
if not orders.empty:
    order_id = st.selectbox("Order ID", orders["order_id"])
    new_status = st.selectbox("New Status", ["Placed", "Preparing", "Out for Delivery", "Delivered"])
    if st.button("Update Status"):
        execute_query("UPDATE Orders SET status=%s WHERE order_id=%s", (new_status, int(order_id)))
        st.success(f"Order {order_id} updated to {new_status}")
        if new_status == "Delivered":
            st.info("Trigger fired: restaurant's total_orders count updated ✅")
        st.rerun()
else:
    st.info("No orders yet. Place one above.")