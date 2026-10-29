import sqlite3

def init_db():
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'user_id INT,'
                'date TEXT,'
                'category TEXT,'
                'amount INT); ')
    con.commit()
    con.close()
