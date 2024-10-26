import sqlite3
connection = sqlite3.connect('Products.db')
cursor = connection.cursor()
def initiate_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Super Enzymes", "Бад для пищеварения", 100))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("Zinc Picolinate", "Дополнительный источник цинка", 200))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("С-1000", "Витамин С", 300))
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?, ?, ?)", ("СoQ10", "Кофермент Q10", 400))
    connection.commit()
    connection.close()
def get_all_products():
    cursor.execute("SELECT title, description, price FROM Products")
    Products = cursor.fetchall()
    Bad = []
    for Product in Products:
        Bad.append(f"Название продукта: {Product[0]} | Описание: {Product[1]} | Цена: {Product[2]}")
    return Bad
    connection.commit()
    connection.close()
def get_name_products():
    cursor.execute("SELECT title, description, price FROM Products")
    Products = cursor.fetchall()
    Bad_name = []
    for Product in Products:
        Bad_name.append(Product[0])
    return Bad_name
    connection.commit()
    connection.close()