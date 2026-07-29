import streamlit as st
from utils.db_connection import run_query, execute_query

st.header("💳 Manage Payments")

st.subheader("All Payments")
payments = run_query("""
    SELECT p.payment_id, p.order_id, c.name AS customer_name,
           p.amount, p.payment_mode, p.payment_status
    FROM Payments p
    JOIN Orders o ON p.order_id = o.order_id
    JOIN Customers c ON o.customer_id = c.customer_id
""")
st.dataframe(payments, use_container_width=True)

st.divider()
st.subheader("➕ Add Payment")
orders_list = run_query("SELECT order_id, total_amount FROM Orders")
if not orders_list.empty:
    with st.form("add_payment"):
        order_id = st.selectbox(
            "Order ID",
            orders_list["order_id"],
            format_func=lambda x: f"Order #{x} (₹{orders_list.loc[orders_list['order_id']==x, 'total_amount'].values[0]})"
        )
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        mode = st.selectbox("Payment Mode", ["UPI", "Card", "COD"])
        submitted = st.form_submit_button("Add Payment")
        if submitted:
            execute_query(
                "INSERT INTO Payments (order_id, amount, payment_mode) VALUES (%s, %s, %s)",
                (int(order_id), amount, mode)
            )
            st.success("✅ Payment record added!")
            st.rerun()
else:
    st.info("No orders found. Place an order first.")

st.divider()
st.subheader("🔄 Update Payment Status")
if not payments.empty:
    payment_id = st.selectbox("Select Payment ID", payments["payment_id"], key="update_payment_select")
    new_status = st.selectbox("New Status", ["Pending", "Completed", "Failed", "Refunded"])
    if st.button("Update Payment Status"):
        execute_query(
            "UPDATE Payments SET payment_status = %s WHERE payment_id = %s",
            (new_status, int(payment_id))
        )
        st.success(f"✅ Payment {payment_id} updated to '{new_status}'")
        st.rerun()
else:
    st.info("No payments found yet.")

st.divider()
st.subheader("📊 Payment Mode Breakdown")
if not payments.empty:
    breakdown = payments["payment_mode"].value_counts()
    st.bar_chart(breakdown)