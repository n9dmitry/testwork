import sqlite3
import json
import shlex
from typing import List, Optional


class CRUDMixin:
    """
    Базовый класс для реализации CRUD-операций.
    """

    def __init__(self, table_name: str, connection: sqlite3.Connection):
        self.table_name = table_name
        self.conn = connection

    def create(self, **kwargs) -> None:
        """
        Создает новую запись в таблице.
        """
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" for _ in kwargs)
        values = tuple(kwargs.values())

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()

    def read(self, join_query: Optional[str] = None) -> List[sqlite3.Row]:
        """
        Читает данные из таблицы. Можно указать `join_query` для сложных запросов.
        """
        query = join_query if join_query else f"SELECT * FROM {self.table_name}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def update(self, id: int, **kwargs) -> None:
        """
        Обновляет запись в таблице по ID.
        """
        columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = tuple(kwargs.values()) + (id,)

        query = f"UPDATE {self.table_name} SET {columns} WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()

    def delete(self, id: int) -> None:
        """
        Удаляет запись из таблицы по ID.
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (id,))
        self.conn.commit()


class TasksManager(CRUDMixin):
    """
    Управляет задачами, наследуясь от CRUDMixin.
    """

    def __init__(self, connection: sqlite3.Connection):
        super().__init__("tasks", connection)

    def list_tasks(self) -> None:
        """
        Отображает список задач с дополнительной информацией из связанных таблиц.
        Также сохраняет данные в JSON-файл.
        """
        join_query = '''
        SELECT 
            tasks.id, 
            tasks.title, 
            tasks.description, 
            tasks.due_date, 
            COALESCE(statuses.name, 'Неизвестно') AS status, 
            COALESCE(priorities.name, 'Неизвестно') AS priority, 
            COALESCE(categories.name, 'Неизвестно') AS category
        FROM tasks
        LEFT JOIN statuses ON tasks.status_id = statuses.id
        LEFT JOIN priorities ON tasks.priority_id = priorities.id
        LEFT JOIN categories ON tasks.category_id = categories.id
        '''
        tasks = self.read(join_query=join_query)

        # Сохранение в JSON-файл
        tasks_data = [
            {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "due_date": task[3],
                "status": task[4],
                "priority": task[5],
                "category": task[6],
            }
            for task in tasks
        ]
        with open("tasks_dump.json", "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=4)

        # Вывод задач
        if not tasks:
            print("В базе данных нет задач.")
        else:
            print(
                f"{'ID':<5} {'Название':<20} {'Описание':<30} {'Срок':<15} {'Статус':<15} {'Приоритет':<15} {'Категория':<15}")
            print("-" * 120)
            for task in tasks:
                print(
                    f"{task[0]:<5} {task[1]:<20} {task[2]:<30} {task[3]:<15} {task[4]:<15} {task[5]:<15} {task[6]:<15}")


def setup_database(connection: sqlite3.Connection) -> None:
    """
    Настраивает базу данных: создает таблицы и заполняет их базовыми данными.
    """
    cursor = connection.cursor()

    # Создание таблиц
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

    # Добавление базовых данных
    cursor.executemany('INSERT OR IGNORE INTO statuses (name) VALUES (?)', [
        ('Не выполнена',),
        ('Выполнена',),
    ])

    cursor.executemany('INSERT OR IGNORE INTO priorities (name) VALUES (?)', [
        ('Низкий',),
        ('Средний',),
        ('Высокий',),
    ])

    cursor.executemany('INSERT OR IGNORE INTO categories (name) VALUES (?)', [
        ('Работа',),
        ('Личное',),
        ('Обучение',),
    ])

    connection.commit()


def main() -> None:
    """
    Основной метод программы, реализующий интерфейс командной строки.
    """
    conn = sqlite3.connect('task_manager.db')
    setup_database(conn)
    tasks_manager = TasksManager(conn)

    print("Интерактивная консоль Task Manager. Введите 'help' для списка команд.")

    commands = {
        "add": lambda args: tasks_manager.create(
            title=args[0],
            description=args[1],
            due_date=args[2],
            status_id=int(args[3]),
            priority_id=int(args[4]),
            category_id=int(args[5]),
        ),
        "update": lambda args: tasks_manager.update(
            id=int(args[0]),
            title=args[1],
            description=args[2],
            due_date=args[3],
            status_id=int(args[4]),
            priority_id=int(args[5]),
            category_id=int(args[6]),
        ),
        "delete": lambda args: tasks_manager.delete(id=int(args[0])),
        "list": lambda args: tasks_manager.list_tasks(),
    }

    while True:
        command = input("\nВведите команду: ").strip()
        if command.lower() == "exit":
            print("Выход из Task Manager.")
            break
        elif command.lower() == "help":
            print("""
Доступные команды:
  add "<Название>" "<Описание>" "<Дата завершения>" <ID статуса> <ID приоритета> <ID категории>   Добавить новую задачу
  update <ID задачи> "<Название>" "<Описание>" "<Дата завершения>" <ID статуса> <ID приоритета> <ID категории>   Обновить задачу
  delete <ID задачи>   Удалить задачу
  list   Показать все задачи
  exit   Выйти из программы
  
  Статусы: 
    1	Не выполнена
    2	Dыполнена
  Приоритеты:
    1	Низкий
    2	Средний
    3	Большой
  Категории
    1	Работа
    2	Личное
    3	Обучение

Пример добавления задачи: 
Введите команду: add "Закончить тестовое" "Закончить тестовое задание" "2024-12-10" 0 1 2
            """)
        else:
            try:
                args = shlex.split(command)
                action = args.pop(0).lower()
                if action in commands:
                    commands[action](args)
                else:
                    print("Неизвестная команда. Введите 'help' для списка доступных команд.")
            except Exception as e:
                print(f"Ошибка: {e}")

    conn.close()

if __name__ == "__main__":
    main()
