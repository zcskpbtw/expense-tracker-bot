import sqlite3
# переход выполнен
def init_db():
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL
       );''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS categories 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
       );''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    date TEXT,
    amount INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
       );''')

    con.commit()
    con.close()
# переход выполнен
def add_expense(telegram_id, date, category_name, amount):
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
                SELECT id 
                FROM users 
                WHERE telegram_id = ?
    ''',(telegram_id,))

    user_row = cur.fetchone()
    if user_row is None:
        cur.execute('''
                    INSERT INTO users (telegram_id) 
                    VALUES (?)
        ''', (telegram_id,))
        user_id_db = cur.lastrowid
    else:
        user_id_db = user_row[0]

    cur.execute('''
                SELECT id 
                FROM categories 
                WHERE user_id = ? 
                AND name = ?
    ''', (user_id_db, category_name))

    cat_row = cur.fetchone()
    if cat_row is None:
        cur.execute('''
                    INSERT INTO categories (user_id, name) 
                    VALUES (?,?)
        ''', (user_id_db,category_name))
        category_id_db = cur.lastrowid
    else:
        category_id_db = cat_row[0]

    cur.execute('''
                INSERT INTO expenses (user_id, category_id, date, amount) 
                VALUES (?,?,?,?)
    ''', (user_id_db, category_id_db, date, amount))


    con.commit()
    con.close()
# переход выполнен
def get_list_expenses(telegram_id):
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
                SELECT * FROM (
                    SELECT e.id, 
                    c.name,            
                    e.amount, 
                    e.date 
                    FROM users u 
                    JOIN categories c ON c.user_id = u.id 
                    JOIN expenses e ON e.user_id = u.id 
                    AND e.category_id = c.id
                    WHERE u.telegram_id = ?
                    ORDER BY e.id DESC 
                    LIMIT 10
                )
                ORDER BY date ASC;
    ''',(telegram_id,))
    result = cur.fetchall()
    con.close()
    return result

def get_all_expenses(user_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('SELECT SUM(amount), '
                    'COUNT(DISTINCT date) '
                    'FROM expenses '
                    'WHERE user_id = ? ', (user_id,))
    get_all = cur_exp.fetchall()
    con_expenses.close()
    return get_all

def get_max_expense(user_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('SELECT date, '
                    'category, '
                    'amount '
                    'FROM expenses '
                    'WHERE user_id = ? '
                    'ORDER BY amount DESC '
                    'LIMIT 1', (user_id,))
    result = cur_exp.fetchall()
    con_expenses.close()
    return result

def avg_expenses(user_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('SELECT SUM(amount), '
                    'COUNT(DISTINCT date) '
                    'FROM expenses '
                    'WHERE user_id = ? ', (user_id,))
    get_avg = cur_exp.fetchall()
    con_expenses.close()
    return get_avg

def delete_by_id(exp_id,user_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('DELETE '
                    'FROM expenses '
                    'WHERE id = ? '
                    'AND user_id = ?',(exp_id,user_id))
    con_expenses.commit()
    result = cur_exp.rowcount
    con_expenses.close()
    return result

def delete_all_exp(user_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('DELETE '
                    'FROM expenses '
                    'WHERE user_id = ?',(user_id,))
    con_expenses.commit()
    result = cur_exp.rowcount
    con_expenses.close()
    return result
