import streamlit as st
from utils.db_connection import run_query
import plotly.express as px

st.header("📊 Live Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    todays_orders = run_query("SELECT * FROM View_TodaysOrders")
    st.metric("Today's Orders", len(todays_orders))
with col2:
    pending = run_query("SELECT * FROM View_PendingDeliveries")
    st.metric("Pending Deliveries", len(pending))
with col3:
    top = run_query("SELECT * FROM View_TopRestaurants")
    st.metric("Top Restaurant", top.iloc[0]['name'] if not top.empty else "N/A")

st.subheader("Today's Orders")
st.dataframe(todays_orders)

st.subheader("Top Restaurants")
fig = px.bar(top, x='name', y='rating', color='total_orders')
st.plotly_chart(fig, use_container_width=True)

st.subheader("Pending Deliveries")
st.dataframe(pending)