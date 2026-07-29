# 🍽️ Cloud Kitchen & Food Delivery Management System

A relational database backend with an interactive Streamlit dashboard — modeled on real-world platforms like **Swiggy**, **Zomato**, and **EatClub**.

This project manages the full order lifecycle for a cloud kitchen / food delivery business: customers, restaurants, menus, orders, drivers, deliveries, payments, ratings, coupons, and offers — with business logic automated at the database level using MySQL triggers and views.

---

## 📌 Features

- **Full CRUD interface** for Customers, Restaurants, Menus, Drivers, Orders, and Payments
- **Automated business logic** via MySQL Triggers:
  - Auto-increments a restaurant's `total_orders` when an order is marked `Delivered`
  - Auto-recalculates a restaurant's average `rating` whenever a new rating is added
- **Live dashboard** powered by SQL Views:
  - Today's Orders
  - Top Restaurants
  - Pending Deliveries
- **Referential integrity** enforced via foreign keys (e.g. a customer with existing orders cannot be deleted)
- Clean, page-based navigation using Streamlit's multipage app structure

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) (Python) |
| Backend / Database | MySQL |
| DB Connector | `mysql-connector-python` |
| Data handling | `pandas` |
| Language | Python 3.10+ |

---

## 🗂️ Project Structure

```
cloud_kitchen_app/
│
├── venv/                        # Virtual environment (not committed to git)
│
├── database/
│   ├── schema.sql                # Reference copy of all CREATE TABLE / TRIGGER / VIEW statements
│   ├── db_setup.py                # Creates database, tables, triggers, and views
│   ├── seed_data.py                # Inserts sample data for testing/demo
│   └── reset_data.py                # Wipes all table data (keeps structure intact)
│
├── utils/
│   └── db_connection.py            # Reusable run_query() / execute_query() helper functions
│
├── pages/
│   ├── 0_Customers.py               # Add / view customers
│   ├── 1_Restaurants.py             # Add restaurants & menu items
│   ├── 2_Orders.py                  # Place orders, update order status
│   ├── 3_Drivers.py                 # Add drivers, toggle availability
│   ├── 4_Payments.py                # Record & update payment status
│   └── 5_Dashboard.py               # Live metrics from SQL Views
│
├── app.py                          # Main entry point / landing page
├── requirements.txt                # Python dependencies
└── README.md                       # You are here
```

---

## 🗄️ Database Design

### Entities (10 tables)

`Customers` · `Restaurants` · `Menus` · `Drivers` · `Orders` · `Deliveries` · `Payments` · `Ratings` · `Coupons` · `Offers`

### Key relationships

- Every **Order** links a **Customer** to a **Restaurant**
- Every **Delivery** links an **Order** to a **Driver**
- **Payments** and **Ratings** both reference back to an **Order**
- Foreign keys enforce referential integrity — e.g. MySQL blocks deleting a Customer who has existing Orders

### Automation — Triggers

| Trigger | Fires when | Action |
|---|---|---|
| `after_order_delivered` | An order's `status` changes to `'Delivered'` | Increments that restaurant's `total_orders` |
| `after_rating_insert` | A new row is inserted into `Ratings` | Recalculates that restaurant's average `rating` |

### Automation — Views

| View | Purpose |
|---|---|
| `View_TodaysOrders` | Joins Orders + Customers + Restaurants, filtered to today's date |
| `View_TopRestaurants` | Ranks restaurants by rating and order volume |
| `View_PendingDeliveries` | Joins Deliveries + Orders + Drivers where status ≠ `'Delivered'` |

---

## 🚀 Getting Started

### 1. Clone / download the project

```bash
cd cloud_kitchen_app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

> ⚠️ You must activate the venv **every time** you open a new terminal for this project — it's what tells Python which installed packages to use.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:
```
streamlit
pandas
mysql-connector-python
plotly
```

### 4. Configure your database credentials

Open the following files and update the connection details to match your local MySQL setup:
- `database/db_setup.py`
- `database/seed_data.py`
- `database/reset_data.py`
- `utils/db_connection.py`

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "cloud_kitchen"
```

### 5. Set up the database

Make sure MySQL is running, then:

```bash
python database/db_setup.py
```

This creates the database, all 10 tables, both triggers, and all 3 views.

### 6. (Optional) Load sample data

```bash
python database/seed_data.py
```

### 7. Run the app

```bash
streamlit run app.py
```

Streamlit will open automatically in your browser (usually at `http://localhost:8501`).

---

## 🔄 Resetting Data

To wipe all data and start fresh (structure, triggers, and views remain untouched):

```bash
python database/reset_data.py
python database/seed_data.py   # optional, reload sample data
```

---

## 🧭 Demo Walkthrough

A suggested order to demonstrate the full system end-to-end:

1. **Add a Customer**
2. **Add a Restaurant** + a **Menu Item**
3. **Add a Driver**
4. **Place an Order**
5. **Mark the order as `Delivered`** → watch the restaurant's `total_orders` update automatically
6. **Add a Payment** for that order
7. Open the **Dashboard** → see live totals, top restaurants, and pending deliveries

---

## 🐛 Troubleshooting

| Issue | Likely Cause |
|---|---|
| `ModuleNotFoundError` | Virtual environment isn't activated in this terminal session |
| Restaurant's `total_orders` not increasing | The order didn't actually exist, or status was already `Delivered` (trigger only fires on a genuine change) |
| `IntegrityError: foreign key constraint fails` | You tried to delete a row (e.g. a Customer) that still has related rows (e.g. Orders) — this is expected, correct behavior |
| A page loads blank | Check the terminal for a Python traceback — Streamlit sometimes renders nothing when an error occurs before the first `st.` call |
| Streamlit shows stale data | Clear cache via the app menu (top-right) → **Clear cache**, or press `C` |

---

## 📈 Possible Future Enhancements

- Ratings page (UI for inserting into the `Ratings` table)
- Coupon/Offer application logic during order placement
- Authentication for customers vs. restaurant admins
- Deployment to Streamlit Community Cloud with managed MySQL (e.g. PlanetScale, AWS RDS)

---

## 📄 License

This project was built for educational purposes as a database systems / DBMS coursework project.
