import sqlite3

def init_db():
    with open ('create_tables.sql', 'r') as f:
        sql = f.read()

    with sqlite3.connect('task_manager.db') as con:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()

if __name__ == '__main__':
    init_db()