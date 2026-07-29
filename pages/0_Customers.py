import streamlit as st
from utils.db_connection import run_query, execute_query

st.header("👤 Manage Customers")

st.subheader("All Customers")
customers = run_query("SELECT * FROM Customers")
st.dataframe(customers, use_container_width=True)

st.divider()
st.subheader("➕ Add New Customer")
with st.form("add_customer"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    address = st.text_area("Address")
    submitted = st.form_submit_button("Add Customer")
    if submitted:
        if name and phone:
            execute_query(
                "INSERT INTO Customers (name, phone, email, address) VALUES (%s, %s, %s, %s)",
                (name, phone, email, address)
            )
            st.success(f"✅ Customer '{name}' added!")
            st.rerun()
        else:
            st.warning("Name and phone are required.")

st.divider()
st.subheader("🗑️ Delete Customer")
if not customers.empty:
    del_id = st.selectbox(
        "Select Customer to Delete",
        customers["customer_id"],
        format_func=lambda x: customers.loc[customers["customer_id"] == x, "name"].values[0]
    )

    # Check if this customer has existing orders
    existing_orders = run_query(
        "SELECT COUNT(*) AS cnt FROM Orders WHERE customer_id = %s", (int(del_id),)
    )
    order_count = int(existing_orders.iloc[0]["cnt"])

    if order_count > 0:
        st.warning(
            f"⚠️ This customer has {order_count} existing order(s). "
            "You can't delete a customer with order history."
        )
    else:
        if st.button("Delete Customer", type="secondary"):
            execute_query("DELETE FROM Customers WHERE customer_id = %s", (int(del_id),))
            st.success("Deleted.")
            st.rerun()