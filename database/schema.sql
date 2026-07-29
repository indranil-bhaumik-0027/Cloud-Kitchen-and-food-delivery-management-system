CREATE DATABASE IF NOT EXISTS cloud_kitchen;
USE cloud_kitchen;

-- Customers
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    address TEXT
);

-- Restaurants
CREATE TABLE Restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    cuisine_type VARCHAR(50),
    rating DECIMAL(2,1) DEFAULT 0,
    location VARCHAR(150),
    total_orders INT DEFAULT 0
);

-- Menus
CREATE TABLE Menus (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    item_name VARCHAR(100),
    price DECIMAL(8,2),
    category VARCHAR(50),
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Drivers
CREATE TABLE Drivers (
    driver_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    phone VARCHAR(15),
    vehicle_no VARCHAR(20),
    is_available BOOLEAN DEFAULT TRUE
);

-- Coupons
CREATE TABLE Coupons (
    coupon_id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE,
    discount_percent DECIMAL(4,2),
    valid_till DATE
);

-- Offers
CREATE TABLE Offers (
    offer_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    description VARCHAR(200),
    discount_percent DECIMAL(4,2),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Orders
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    restaurant_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'Placed', -- Placed, Preparing, Out for Delivery, Delivered
    coupon_id INT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    FOREIGN KEY (coupon_id) REFERENCES Coupons(coupon_id)
);

-- Deliveries
CREATE TABLE Deliveries (
    delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    driver_id INT,
    pickup_time DATETIME,
    delivery_time DATETIME,
    delivery_status VARCHAR(20) DEFAULT 'Assigned',
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id)
);

-- Payments
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    amount DECIMAL(10,2),
    payment_mode VARCHAR(20), -- UPI, Card, COD
    payment_status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Ratings
CREATE TABLE Ratings (
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    restaurant_id INT,
    customer_id INT,
    rating_value DECIMAL(2,1),
    review TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);
-- ... all your CREATE TABLE statements above ...

DELIMITER //
CREATE TRIGGER after_order_delivered
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'Delivered' AND OLD.status <> 'Delivered' THEN
        UPDATE Restaurants
        SET total_orders = total_orders + 1
        WHERE restaurant_id = NEW.restaurant_id;
    END IF;
END //
DELIMITER ;
CREATE VIEW View_TodaysOrders AS ...
CREATE VIEW View_TopRestaurants AS ...
CREATE VIEW View_PendingDeliveries AS ...