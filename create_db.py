import sqlite3
def create_db():
    con=sqlite3.connect(database=r'fms.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,Category text,name text,price text,qty text,status text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS recruitment(rid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,address text,sex text,contact text,date text,cccd text,workplace text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS sales(sale_id INTEGER PRIMARY KEY AUTOINCREMENT,product_id INTEGER,product_name TEXT,quantity INTEGER,price_paid REAL,sale_date TEXT, FOREIGN KEY (product_id) REFERENCES product(pid))")
    con.commit()

create_db()