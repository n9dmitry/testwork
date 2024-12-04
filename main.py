import json
import sqlite3

conn = sqlite3.connect('task_manager.db')

cursor = conn.cursor()
# ===
def create_json_dump():
    cursor.execute('''
    SELECT 
        tasks.id, 
        tasks.title, 
        tasks.description, 
        tasks.due_date, 
        COALESCE(statuses.name, (SELECT name FROM statuses WHERE id = 1)) AS status, 
        priorities.name AS priority, 
        categories.name AS category
    FROM tasks
    LEFT JOIN statuses ON tasks.status_id = statuses.id
    LEFT JOIN priorities ON tasks.priority_id = priorities.id
    LEFT JOIN categories ON tasks.category_id = categories.id
    ''')
    tasks = cursor.fetchall()
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "due_date": task[3],
            "status": task[4],
            "priority": task[5],
            "category": task[6],
        })
    with open('tasks_dump.json', 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)

# ===

cursor.execute('''
CREATE TABLE IF NOT EXISTS statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS priorities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status_id INTEGER,
    priority_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES statuses(id),
    FOREIGN KEY (priority_id) REFERENCES priorities(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
    )
''')

def add_status(name):
    cursor.execute('INSERT OR IGNORE INTO statuses (name) VALUES (?)', (name,))
    conn.commit()

def add_priority(name):
    cursor.execute('INSERT OR IGNORE INTO priorities (name) VALUES (?)', (name,))
    conn.commit()

def add_category(name):
    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (name,))
    conn.commit()

def add_task(title, description, due_date, status_id, priority_id, category_id):
    cursor.execute('''
    INSERT INTO tasks (title, description, due_date, status_id, priority_id, category_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, due_date, status_id, priority_id, category_id))
    conn.commit()


add_status('Не выполнена')
add_status('Dыполнена')

add_priority('Низкий')
add_priority('Средний')
add_priority('Большой')

add_category('Работа')
add_category('Личное')
add_category('Обучение')

add_task('Тестовая задача', 'Закончить конечный отчет по проекту', '2024-12-10', 0, 2, 1)
conn.commit()
create_json_dump()
# ======

conn.close()




# def main():
#     parser = argparse.ArgumentParser(description='Task Manager CLI')
#     subparsers = parser.add_subparsers(dest='command')