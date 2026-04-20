from sqlite3 import Error

def get_task_by_user(con, user_id):
    cur = con.cursor()
    all_tasks = None
    try:
        all_tasks = cur.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (user_id,)
        ).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return all_tasks

def get_task_by_status(con, status_name):
    cur = con.cursor()
    all_tasks = None
    try:
        all_tasks = cur.execute("""
            SELECT tasks.*
            FROM tasks
            JOIN status ON tasks.status_id = status.id
            WHERE status.name = ?
        """, (status_name,)).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return all_tasks

def new_status_for_task(con, task_id, status_name):
    cur = con.cursor()
    try:
        cur.execute("SELECT id FROM status WHERE name = ?", (status_name,))
        status = cur.fetchone()

        if status is None:
            print("Статус не знайдено")
            return

        status_id = status[0]
        cur.execute(
            "UPDATE tasks SET status_id = ? WHERE id = ?",
            (status_id, task_id)
        )
        con.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def get_user_with_no_tasks(con):
    cur = con.cursor()
    users_with_no_tasks = None
    try:
        users_with_no_tasks = cur.execute("""
            SELECT * 
            FROM users 
            WHERE id NOT IN (
                SELECT user_id FROM tasks
            )
        """).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return users_with_no_tasks

def add_new_task(con, task_title, task_description, task_status_id, task_user_id):
    cur = con.cursor()
    try:
        cur.execute('''INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)''', (task_title, task_description, task_status_id, task_user_id))
        con.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def get_unfinished_tasks(con):
    cur = con.cursor()
    unfinished_tasks = None
    try:
        cur.execute("""
            SELECT * 
            FROM tasks 
            JOIN status on tasks.status_id = status.id
            WHERE status.name != 'completed'
        """)
        unfinished_tasks = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return unfinished_tasks

def delete_task(con, task_id):
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        con.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def get_user_by_email(con, email_pattern):
    cur = con.cursor()
    user_by_email = None
    try:
        user_by_email = cur.execute('''
        SELECT * 
        FROM users 
        WHERE email 
        LIKE ?
        ORDER BY fullname''', (email_pattern,)).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return user_by_email

def update_user_name(con, user_id, new_name):
    cur = con.cursor()
    try:
        cur.execute("""
            UPDATE users
            SET fullname = ?
            WHERE id = ?
        """, (new_name, user_id))
        con.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def get_quant_status(con):
    cur = con.cursor()
    quant_status = None
    try:
        quant_status = cur.execute("""
            SELECT status.name, COUNT(tasks.id) AS total_tasks
            FROM status
            LEFT JOIN tasks ON status.id = tasks.status_id
            GROUP BY status.id, status.name
            ORDER BY status.id
        """).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return quant_status

def get_tasks_by_email(con, domain):
    cur = con.cursor()
    tasks_by_email = None
    try:
        domain_like = f"%@{domain}"
        tasks_by_email = cur.execute("""
            SELECT *
            FROM users
            JOIN tasks ON users.id = tasks.user_id
            WHERE email LIKE ?
            ORDER BY tasks.title
        """, (domain_like,)).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return tasks_by_email

def get_tasks_without_description(con):
    cur = con.cursor()
    tasks_without_description = None
    try:
        tasks_without_description = cur.execute('''
        SELECT *
        FROM tasks
        WHERE description IS NULL''').fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return tasks_without_description

def users_and_tasks_by_status(con, status_name='in progress'):
    cur = con.cursor()
    users_and_tasks = None
    try:
        users_and_tasks = cur.execute("""
            SELECT users.id, users.fullname, tasks.id, tasks.title
            FROM tasks
            INNER JOIN users ON users.id = tasks.user_id
            INNER JOIN status ON status.id = tasks.status_id
            WHERE status.name = ?
            ORDER BY users.fullname, tasks.title
        """, (status_name,)).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return users_and_tasks

def get_users_and_num_tasks(con):
    cur = con.cursor()
    users_and_num_tasks = None
    try:
        users_and_num_tasks = cur.execute("""
            SELECT users.id, users.fullname, COUNT(tasks.id) AS total_tasks
            FROM users
            LEFT JOIN tasks ON users.id = tasks.user_id
            GROUP BY users.id
            ORDER BY users.fullname
        """).fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return users_and_num_tasks