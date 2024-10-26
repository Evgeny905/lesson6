import sqlite3
connection = sqlite3.connect('Products.db')
cursor = connection.cursor()
connection_users = sqlite3.connect('Users.db')
cursor_users = connection_users.cursor()
def initiate_db():
    cursor_users.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    """)
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
    connection_users.commit()
    connection.commit()
def add_user(username, email, age):
    cursor_users.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",(username, email, age, 1000))
    connection_users.commit()
def is_included(username):
    Replay_user = False
    cursor_users.execute("SELECT * FROM Users")
    Users = cursor_users.fetchall()
    for User in Users:
        if User[1] == username:
            Replay_user = True
        else:
            continue
    return Replay_user
    connection_users.commit()
    connection_users.close()
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