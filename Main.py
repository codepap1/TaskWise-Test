from User import User
from Task import Task
from Database import Database

USERS_DB = "users.db"
TASKS_DB = "tasks.db"


def main():  #
    db_users = Database(USERS_DB)
    db_users.create_tables()

    db_tasks = Database(TASKS_DB)
    db_tasks.create_tables()

    while True:
        print('========================================================')
        print('\tSTUDENT TO-DO-LIST APPLICATION')
        print('========================================================')
        print('\t1. Login')
        print('\t2. Create an Account')
        print('\t3. Exit')
        print('========================================================')
        try:
            choice = int(input('Enter choice [1-3]: '))
            print('========================================================')

            if choice == 1:
                user = login(db_users)
                if user:
                    main_menu(user, db_tasks)
                    break
            elif choice == 2:
                create_account(db_users)
            elif choice == 3:
                db_users.close()
                db_tasks.close()
                print('========================================================')
                print('Thank you and come back again!')
                break
            else:
                print("Invalid choice [1-3] only!")
        except ValueError:
            print('========================================================')
            print("Invalid choice! Please enter a number [1-3] only.")


def login(db_users):
    try:
        username = input("Enter Registered Username: ")
        password = input("Enter Registered Password: ")
        users = db_users.load_users()
        for user in users:
            if user.username == username and user.password == password:
                print('========================================================')
                print("Login successful!")
                return user
        print('========================================================')
        print("Invalid username or password.")
        return None
    except Exception as e:
        print('An error occurred:', e)
        return None


def create_account(db_users):
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")
    studentNum = input("Student Number: ")
    username = input("Desired Username: ")
    password = input("Desired Password: ")

    users = db_users.load_users()
    for user in users:
        if user.username == username:
            print('========================================================')
            print("Username already exists.")
            return

    new_user = User(firstName, lastName, studentNum, username, password)
    db_users.save_user(new_user)
    print('========================================================')
    print("Account created successfully!")


def main_menu(user, db_tasks):
    while True:
        print('========================================================')
        print(f"Hi {user.first_name}, Welcome to TaskWise!")
        print('Your tasks today:')
        tasks = db_tasks.load_tasks(user.student_number)
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")
        print('========================================================')
        print('\t1. Create Task')
        print('\t2. Update Task')
        print('\t3. Delete Task')
        print('\t4. Search Task')
        print('\t5. Mark Task as Completed')
        print('\t6. Logout')
        print('========================================================')
        try:
            choice = int(input('Enter choice [1-6]: '))
            print('========================================================')
            if choice == 1:
                create_task(user, db_tasks)
            elif choice == 2:
                update_task(user, db_tasks)
            elif choice == 3:
                delete_task(user, db_tasks)
            elif choice == 4:
                search_task(user, db_tasks)
            elif choice == 5:
                mark_task_completed(user, db_tasks)
            elif choice == 6:
                print('Logging out...')
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print('========================================================')
            print("Invalid choice! Please enter a number.")


def create_task(user, db_tasks):
    task_name = input("Enter Task Name: ")
    task_desc = input("Enter Task Description: ")
    task_date = input("Enter Task Deadline (YYYY-MM-DD): ")
    task_time = input("Enter Task Time (00:00 AM/PM): ")
    task_sub = input("Enter Task Subject: ")
    task_cat = input("Enter Task Category: ")
    status = "Incomplete"
    new_task = Task(task_name, task_desc, task_date, task_time, task_sub, task_cat, status)
    db_tasks.save_task(new_task, user.student_number)
    print('========================================================')
    print('Task created successfully!')


def update_task(user, db_tasks):
    tasks = db_tasks.load_tasks(user.student_number)
    if not tasks:
        print("No tasks found.")
        return

    print("Select the task you want to update:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_index = int(input("Enter the task index: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            new_name = input("Enter new task name: ")
            new_description = input("Enter new task description: ")
            new_date = input("Enter new task deadline (YYYY-MM-DD): ")
            new_time = input("Enter new task time(HH:SS AM/PM): ")
            task.name = new_name if new_name else task.name
            task.task_desc = new_description if new_description else task.task_desc
            task.date = new_date if new_date else task.date
            task.time = new_time if new_time else task.time

            db_tasks.save_task(task, user.student_number)
            print('========================================================')
            print("Task updated successfully!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def delete_task(user, db_tasks):
    tasks = db_tasks.load_tasks(user.student_number)
    if not tasks:
        print("No tasks found.")
        return

    print("Select the task you want to delete:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_index = int(input("Enter the task index: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            db_tasks.delete_task(task, user.student_number)
            print('========================================================')
            print("Task deleted successfully!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def search_task(user, db_tasks):
    keyword = input("Enter a keyword to search: ")
    tasks = db_tasks.load_tasks(user.student_number)
    found_tasks = [task for task in tasks if keyword.lower() in task.task_name.lower()]
    if found_tasks:
        print("Matching tasks:")
        for i, task in enumerate(found_tasks, start=1):
            print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")
    else:
        print("No matching tasks found.")


def mark_task_completed(user, db_tasks):
    tasks = db_tasks.load_tasks(user.student_number)
    if not tasks:
        print("No tasks found.")
        return

    print("Select the task you want to mark as completed:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.task_name} - {task.task_desc} - Date: {task.date} - Time: {task.time} - Status: {task.status}")

    try:
        task_index = int(input("Enter the task index: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            task.status = "Completed"
            db_tasks.save_task(task, user.student_number)
            print('========================================================')
            print("Task marked as completed!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()
