import sqlite3

def connection():
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY,title TEXT, author TEXT, year INTEGER , category TEXT,status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY,book_id INTEGER,book TEXT,borrowed_name TEXT,loan_date TEXT)")
    connect.commit()
    connect.close()


def insert(title, author, year, category, status):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO books VALUES (NULL,?,?,?,?,?)", (title, author, year, category, status))
    connect.commit()
    connect.close()


def viewAll():
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    connect.close()
    return rows


def delete(id):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    connect.commit()
    connect.close()


def update(id, title, author, year, category, status):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE books SET title=? , author=?,year=? , category=?, status=? WHERE id = ?",
                   (title, author, year, category, status, id))
    connect.commit()
    connect.close()


def search(column,value):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM books WHERE {column} LIKE ?",(f"%{value}%",))
    rows = cursor.fetchall()
    connect.close()
    return rows

def borrow_book(book_id,book,borrower_name,loan_date):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO loans VALUES (NULL,?,?,?,?)",(book_id,book,borrower_name,loan_date))
    cursor.execute("UPDATE books SET status=? WHERE id=?",("Borrowed",book_id))
    connect.commit()
    connect.close()

def view_all_loans():
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM loans")
    rows = cursor.fetchall()
    connect.close()
    return rows

def return_loan_book(book_id):
    connect = sqlite3.connect('./library.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM loans WHERE book_id=?", (book_id,))
    cursor.execute("UPDATE books SET status=? WHERE id=?", ("Available", book_id))
    connect.commit()
    connect.close()

connection()

