from random import randint
from faker import Faker
import sqlite3

NUMBER_OF_USERS = 15
NUMBER_OF_TASKS = 10
STATUS = [('new',), ('in progress',), ('completed',)]

def data_generator(number_of_users, status, number_of_tasks) -> tuple:
    fake_users = []
    fake_tasks = []

    fake_data = Faker()

    for _ in range(number_of_users):
        fake_users.append({
            'fullname': fake_data.name(),
            'email': fake_data.unique.email(),
        })

    for _ in range(number_of_tasks):
        fake_tasks.append({
            'title': fake_data.text(max_nb_chars=100),
            'description': None if randint(1, 3) == 1 else fake_data.paragraph(),
            'status_id': randint(1, len(status)),
            'user_id': randint(1, number_of_users),
        })

    return fake_users, status, fake_tasks

def prepare_data(fake_users, status, fake_tasks) -> tuple:
    ready_users = []
    ready_statuses = []
    ready_tasks = []

    for user in fake_users:
        prep_user = (user['fullname'], user['email'])
        ready_users.append(prep_user)

    for status_name in status:
        ready_statuses.append(status_name)

    for task in fake_tasks:
        prep_task = (task['title'], task['description'], task['status_id'], task['user_id'])
        ready_tasks.append(prep_task)

    return ready_users, ready_statuses, ready_tasks

def insert_data(ready_users, ready_statuses, ready_tasks):
    with sqlite3.connect('task_manager.db') as con:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()

        user_sql = '''
        INSERT OR IGNORE INTO users (fullname, email)
        VALUES (?, ?)
        '''
        cur.executemany(user_sql, ready_users)

        status_sql = '''
        INSERT OR IGNORE INTO status(name)
        VALUES (?)
        '''
        cur.executemany(status_sql, ready_statuses)

        task_sql = '''
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, ?, ?)
        '''
        cur.executemany(task_sql, ready_tasks)

        con.commit()

if __name__ == "__main__":
    users, statuses, tasks = prepare_data(*data_generator(NUMBER_OF_USERS, STATUS, NUMBER_OF_TASKS))
    insert_data(users, statuses, tasks)