CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    mobile_number TEXT UNIQUE,
    tea_count INTEGER DEFAULT 0,
    coffee_count INTEGER DEFAULT 0,
    visit_count INTEGER DEFAULT 0,
    last_order TEXT,
    order_date TEXT,
    order_time TEXT
);
