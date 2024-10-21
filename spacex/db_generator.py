import sqlite3
from faker import Faker
import random

fake = Faker('ru_RU')

conn = sqlite3.connect('spacex_employees.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    level INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    position TEXT,
    hire_date TEXT,
    salary REAL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
)
''')

# Реальные названия департаментов SpaceX на русском
department_names = [
    "Инженерия",
    "Управление Миссией",
    "Производство",
    "Контроль Качества",
    "Человеческие Ресурсы",
    "Финансы",
    "Юридические Вопросы",
    "Информационные Технологии",
    "Связи с Общественностью",
    "Продажи и Маркетинг",
    "Операции Запуска",
    "Управление Программами",
    "Управление Цепочкой Поставок",
    "Разработка Ракет",
    "Разработка Космических Аппаратов",
    "Операции Тестирования",
    "Научные Исследования и Разработка",
    "Разработка Программного Обеспечения",
    "Анализ Данных",
    "Поддержка Клиентов",
    "Безопасность и Соответствие",
    "Современное Производство",
    "Управление Проектами",
    "Наземные Операции",
    "Операции Экипажа"
]

departments = []
for level in range(1, 6):
    for name in department_names:
        departments.append((name, level))

cursor.executemany('''
INSERT INTO departments (name, level) VALUES (?, ?)
''', departments)
conn.commit()

print("Подразделения успешно добавлены! 🌌")


def generate_employee(department_id):
    full_name = fake.name()
    position = fake.job()
    hire_date = fake.date_between(start_date='-10y', end_date='today')
    salary = round(random.uniform(50000, 150000), 2)

    return (full_name, position, hire_date, salary, department_id)


employees = []
num_employees = 51000
department_ids = [d[0] for d in cursor.execute('SELECT id FROM departments').fetchall()]

for i in range(num_employees):
    dept_id = random.choice(department_ids)
    employees.append(generate_employee(dept_id))

    # Принт прогресса каждые 1000 сотрудников
    if (i + 1) % 1000 == 0:
        print(f"Сгенерировано {i + 1} сотрудников...")

cursor.executemany('''
INSERT INTO employees (full_name, position, hire_date, salary, department_id)
VALUES (?, ?, ?, ?, ?)
''', employees)
conn.commit()

conn.close()

print("Генерация сотрудников завершена! 🎉")
