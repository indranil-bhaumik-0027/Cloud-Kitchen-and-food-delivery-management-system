import streamlit as st
from utils.db_connection import run_query, execute_query

st.header("🛵 Manage Drivers")

st.subheader("All Drivers")
drivers = run_query("SELECT * FROM Drivers")
st.dataframe(drivers, use_container_width=True)

st.divider()
st.subheader("➕ Add New Driver")
with st.form("add_driver"):
    name = st.text_input("Driver Name")
    phone = st.text_input("Phone Number")
    vehicle_no = st.text_input("Vehicle Number")
    submitted = st.form_submit_button("Add Driver")
    if submitted:
        if name and phone and vehicle_no:
            success = execute_query(
                "INSERT INTO Drivers (name, phone, vehicle_no) VALUES (%s, %s, %s)",
                (name, phone, vehicle_no)
            )
            if success:
                st.success(f"✅ Driver '{name}' added!")
                st.rerun()
        else:
            st.warning("Please fill in all fields.")

st.divider()
st.subheader("🔄 Toggle Driver Availability")
if not drivers.empty:
    driver_id = st.selectbox(
        "Select Driver",
        drivers["driver_id"],
        format_func=lambda x: drivers.loc[drivers["driver_id"] == x, "name"].values[0]
    )
    new_status = st.radio("Set Availability", ["Available", "Unavailable"])
    if st.button("Update Availability"):
        is_available = 1 if new_status == "Available" else 0
        execute_query(
            "UPDATE Drivers SET is_available = %s WHERE driver_id = %s",
            (is_available, int(driver_id))
        )
        st.success("✅ Availability updated.")
        st.rerun()
else:
    st.info("No drivers found. Add one above.")