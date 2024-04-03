import sqlite3
from User import User
from Task import Task


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    full_name TEXT,
                                    student_number TEXT,
                                    birth_date TEXT,
                                    username TEXT PRIMARY KEY,
                                    password TEXT
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                    name TEXT,
                                    description TEXT,
                                    deadline TEXT,
                                    status TEXT,
                                    username TEXT,
                                    FOREIGN KEY (username) REFERENCES users(username)
                                )''')
        self.conn.commit()

    def save_user(self, user):
        self.cursor.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?)''',
                            (user.full_name, user.student_number, user.birth_date, user.username, user.password))
        self.conn.commit()

    def load_users(self):
        self.cursor.execute('''SELECT * FROM users''')
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4])
            users.append(user)
        return users

    def save_task(self, task, username):
        self.cursor.execute('''INSERT INTO tasks VALUES (?, ?, ?, ?, ?)''',
                            (task.name, task.description, task.deadline, task.status, username))
        self.conn.commit()

    def delete_task(self, task, username):
        self.cursor.execute('''DELETE FROM tasks WHERE name = ? AND username = ?''', (task.name, username))
        self.conn.commit()

    def load_tasks(self, username):
        self.cursor.execute('''SELECT * FROM tasks WHERE username = ?''', (username,))
        rows = self.cursor.fetchall()
        tasks = []
        for row in rows:
            task = Task(row[0], row[1], row[2], row[3])
            tasks.append(task)
        return tasks

    def close(self):
        self.conn.close()
