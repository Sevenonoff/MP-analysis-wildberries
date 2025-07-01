import sqlite3

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    discounted_price REAL,
    rating REAL,
    reviews_count INTEGER
)
''')

conn.close()
