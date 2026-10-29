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

def add_expense(user_id, date, category, amount):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('INSERT INTO expenses (user_id, date, category, amount) '
                    'VALUES (?,?,?,?);',
                    (user_id,date,category,amount))
    con_expenses.commit()
    con_expenses.close()


