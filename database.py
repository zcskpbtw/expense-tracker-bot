import sqlite3


## add .bd
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

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users_limits 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    limit_global INT
           );''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users_limits_categories 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    limit_category INT
               );''')

    con.commit()
    con.close()

## add
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

## stats
def get_all_expenses(telegram_id):
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
                SELECT SUM (e.amount), 
                    COUNT (DISTINCT e.date) 
                FROM expenses e 
                JOIN users u ON u.id = e.user_id 
                AND u.telegram_id = ?;
    ''', (telegram_id,))
    res = cur.fetchall()
    con.close()
    return res

def get_max_expense(telegram_id):
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
                SELECT e.date, 
                    c.name, 
                    e.amount 
                FROM expenses e 
                JOIN categories c ON c.id = e.category_id 
                JOIN users u ON u.id = e.user_id 
                AND u.telegram_id = ? 
                ORDER BY amount DESC 
                LIMIT 1;
                
        ''', (telegram_id,))
    res = cur.fetchall()
    con.close()
    return res

def get_avg_expenses(telegram_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('''
                    SELECT SUM(e.amount), 
                        COUNT(DISTINCT e.date)
                    FROM expenses e
                    JOIN users u ON u.id = e.user_id
                    WHERE u.telegram_id = ?             
    ''', (telegram_id,))
    res = cur_exp.fetchall()
    con_expenses.close()
    return res

## chart
def get_expenses_for_chart(telegram_id):
    con = sqlite3.connect('expenses.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute('''
                    SELECT c.name, 
                        SUM(e.amount) sum_amounts
                    FROM expenses e 
                    JOIN categories c ON c.id = e.category_id 
                    JOIN users u ON u.id = e.user_id 
                    WHERE u.telegram_id =  ? 
                    GROUP BY c.name 
                    ORDER BY sum_amounts DESC ;
            ''', (telegram_id,))
    res = cur.fetchall()
    con.close()
    return res

## list
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
    res = cur.fetchall()
    con.close()
    return res

## limit
# def set_global_limit(telegram_id):
#     con = sqlite3.connect('expenses.db')
#     cur = con.cursor()
#     cur.execute("PRAGMA foreign_keys = ON;")
#
#     cur.execute('''
#                     SELECT id
#                     FROM users
#                     WHERE telegram_id = ?
#         ''', (telegram_id,))
#
#     user_row = cur.fetchone()
#     if user_row is None:
#         cur.execute('''
#                         INSERT INTO users (telegram_id)
#                         VALUES (?)
#             ''', (telegram_id,))
#         user_id_db = cur.lastrowid
#     else:
#         user_id_db = user_row[0]
#
#     cur.execute('''
#                     SELECT id
#                     FROM categories
#                     WHERE user_id = ?
#                     AND name = ?
#         ''', (user_id_db, category_name))
#
#     cat_row = cur.fetchone()
#     if cat_row is None:
#         cur.execute('''
#                         INSERT INTO categories (user_id, name)
#                         VALUES (?,?)
#             ''', (user_id_db, category_name))
#         category_id_db = cur.lastrowid
#     else:
#         category_id_db = cat_row[0]
#
#     cur.execute('''
#                     INSERT INTO expenses (user_id, category_id, date, amount)
#                     VALUES (?,?,?,?)
#         ''', (user_id_db, category_id_db, date, amount))
#
#     con.commit()
#     con.close()
#
# def set_category_limit(telegram_id, category, limit):


## delete

def delete_id_expense(exp_id,telegram_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('''
                    DELETE FROM expenses 
                    WHERE id = ? 
                    AND user_id = (SELECT id FROM users WHERE telegram_id = ?) 
                    ''',(exp_id,telegram_id))
    con_expenses.commit()
    res = cur_exp.rowcount
    con_expenses.close()
    return res

def delete_all_expenses(telegram_id):
    con_expenses = sqlite3.connect('expenses.db')
    cur_exp = con_expenses.cursor()
    cur_exp.execute('''
                    DELETE FROM expenses 
                    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    ''',(telegram_id,))
    con_expenses.commit()
    res = cur_exp.rowcount
    con_expenses.close()
    return res
