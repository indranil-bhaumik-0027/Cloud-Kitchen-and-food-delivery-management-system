"""
reset_data.py
Wipes all data from every table (but keeps table structure, triggers, views).
Usage: python database/reset_data.py
"""

import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "cloud_kitchen"

TABLES_IN_ORDER = [
    "Ratings", "Payments", "Deliveries", "Orders",
    "Offers", "Coupons", "Menus", "Drivers", "Restaurants", "Customers"
]

def main():
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in TABLES_IN_ORDER:
        cursor.execute(f"TRUNCATE TABLE {table}")
        print(f"🗑️  Cleared: {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n✅ All data cleared. Tables, triggers, and views are untouched.")

if __name__ == "__main__":
    main()