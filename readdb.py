import sqlite3

database_path = 'markov_chain.db'

connection = sqlite3.connect(database_path)

# Создаем курсор для выполнения SQL-запросов
cursor = connection.cursor()

# Выполняем SQL-запрос
cursor.execute("SELECT * FROM markov_chain")

# Получаем результат запроса
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
