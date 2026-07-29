"""
db_setup.py
Run this once to create the database, tables, triggers, and views.
Usage: python database/db_setup.py
"""

import mysql.connector
from mysql.connector import Error

# ---- CONFIG: update these to match your MySQL setup ----
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "cloud_kitchen"


def create_database():
    """Create the database if it doesn't exist."""
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' ready.")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"❌ Error creating database: {e}")
        raise


def get_db_connection():
    """Connect directly to the cloud_kitchen database."""
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )


def create_tables(cursor):
    tables = {
        "Customers": """
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                phone VARCHAR(15),
                email VARCHAR(100),
                address TEXT
            )""",
        "Restaurants": """
            CREATE TABLE IF NOT EXISTS Restaurants (
                restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                cuisine_type VARCHAR(50),
                rating DECIMAL(2,1) DEFAULT 0,
                location VARCHAR(150),
                total_orders INT DEFAULT 0
            )""",
        "Menus": """
            CREATE TABLE IF NOT EXISTS Menus (
                menu_id INT PRIMARY KEY AUTO_INCREMENT,
                restaurant_id INT,
                item_name VARCHAR(100),
                price DECIMAL(8,2),
                category VARCHAR(50),
                is_available BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
            )""",
        "Drivers": """
            CREATE TABLE IF NOT EXISTS Drivers (
                driver_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                phone VARCHAR(15),
                vehicle_no VARCHAR(20),
                is_available BOOLEAN DEFAULT TRUE
            )""",
        "Coupons": """
            CREATE TABLE IF NOT EXISTS Coupons (
                coupon_id INT PRIMARY KEY AUTO_INCREMENT,
                code VARCHAR(20) UNIQUE,
                discount_percent DECIMAL(4,2),
                valid_till DATE
            )""",
        "Offers": """
            CREATE TABLE IF NOT EXISTS Offers (
                offer_id INT PRIMARY KEY AUTO_INCREMENT,
                restaurant_id INT,
                description VARCHAR(200),
                discount_percent DECIMAL(4,2),
                FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
            )""",
        "Orders": """
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT,
                restaurant_id INT,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'Placed',
                coupon_id INT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
                FOREIGN KEY (coupon_id) REFERENCES Coupons(coupon_id)
            )""",
        "Deliveries": """
            CREATE TABLE IF NOT EXISTS Deliveries (
                delivery_id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT,
                driver_id INT,
                pickup_time DATETIME,
                delivery_time DATETIME,
                delivery_status VARCHAR(20) DEFAULT 'Assigned',
                FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
            )""",
        "Payments": """
            CREATE TABLE IF NOT EXISTS Payments (
                payment_id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT,
                amount DECIMAL(10,2),
                payment_mode VARCHAR(20),
                payment_status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (order_id) REFERENCES Orders(order_id)
            )""",
        "Ratings": """
            CREATE TABLE IF NOT EXISTS Ratings (
                rating_id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT,
                restaurant_id INT,
                customer_id INT,
                rating_value DECIMAL(2,1),
                review TEXT,
                FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
            )""",
    }

    for name, ddl in tables.items():
        cursor.execute(ddl)
        print(f"  ✅ Table '{name}' ready.")


def create_triggers(cursor):
    # Drop first so re-running this script doesn't error out
    cursor.execute("DROP TRIGGER IF EXISTS after_order_delivered")
    cursor.execute("""
        CREATE TRIGGER after_order_delivered
        AFTER UPDATE ON Orders
        FOR EACH ROW
        BEGIN
            IF NEW.status = 'Delivered' AND OLD.status <> 'Delivered' THEN
                UPDATE Restaurants
                SET total_orders = total_orders + 1
                WHERE restaurant_id = NEW.restaurant_id;
            END IF;
        END
    """)
    print("  ✅ Trigger 'after_order_delivered' created.")

    cursor.execute("DROP TRIGGER IF EXISTS after_rating_insert")
    cursor.execute("""
        CREATE TRIGGER after_rating_insert
        AFTER INSERT ON Ratings
        FOR EACH ROW
        BEGIN
            UPDATE Restaurants
            SET rating = (
                SELECT AVG(rating_value) FROM Ratings
                WHERE restaurant_id = NEW.restaurant_id
            )
            WHERE restaurant_id = NEW.restaurant_id;
        END
    """)
    print("  ✅ Trigger 'after_rating_insert' created.")


def create_views(cursor):
    cursor.execute("""
        CREATE OR REPLACE VIEW View_TodaysOrders AS
        SELECT o.order_id, c.name AS customer_name, r.name AS restaurant_name,
               o.total_amount, o.status, o.order_date
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE DATE(o.order_date) = CURDATE()
    """)
    print("  ✅ View 'View_TodaysOrders' created.")

    cursor.execute("""
        CREATE OR REPLACE VIEW View_TopRestaurants AS
        SELECT restaurant_id, name, rating, total_orders
        FROM Restaurants
        ORDER BY rating DESC, total_orders DESC
        LIMIT 10
    """)
    print("  ✅ View 'View_TopRestaurants' created.")

    cursor.execute("""
        CREATE OR REPLACE VIEW View_PendingDeliveries AS
        SELECT d.delivery_id, o.order_id, dr.name AS driver_name, d.delivery_status
        FROM Deliveries d
        JOIN Orders o ON d.order_id = o.order_id
        JOIN Drivers dr ON d.driver_id = dr.driver_id
        WHERE d.delivery_status <> 'Delivered'
    """)
    print("  ✅ View 'View_PendingDeliveries' created.")


def main():
    print("🚀 Setting up Cloud Kitchen database...\n")
    create_database()

    conn = get_db_connection()
    cursor = conn.cursor()

    print("\n📋 Creating tables...")
    create_tables(cursor)

    print("\n⚡ Creating triggers...")
    create_triggers(cursor)

    print("\n👁️ Creating views...")
    create_views(cursor)

    conn.commit()
    cursor.close()
    conn.close()
    print("\n🎉 Database setup complete!")


if __name__ == "__main__":
    main()