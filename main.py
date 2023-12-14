import requests
from bs4 import BeautifulSoup
import sqlite3

# Функция для получения текста сказок


def get_pushkin_fairytales(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fairytales = [p.get_text() for p in soup.find_all('p')]
    return ' '.join(fairytales)

# Функция для создания таблицы вероятностей следования букв


def create_markov_chain_table(text):
    chain_table = {}

    for i in range(len(text)-1):
        current_char = text[i]
        next_char = text[i+1]

        if current_char not in chain_table:
            chain_table[current_char] = {}

        if next_char not in chain_table[current_char]:
            chain_table[current_char][next_char] = 1
        else:
            chain_table[current_char][next_char] += 1

    # Нормализация вероятностей
    for char, transitions in chain_table.items():
        total_transitions = sum(transitions.values())
        for next_char, count in transitions.items():
            chain_table[char][next_char] = count / total_transitions

    return chain_table

# Функция для сохранения таблицы в базу данных SQL


def save_to_database(chain_table):
    conn = sqlite3.connect('markov_chain.db')
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute('''CREATE TABLE IF NOT EXISTS markov_chain (
                      current_char TEXT,
                      next_char TEXT,
                      probability REAL)''')

    # Заполнение таблицы
    for current_char, transitions in chain_table.items():
        for next_char, probability in transitions.items():
            cursor.execute('INSERT INTO markov_chain VALUES (?, ?, ?)',
                           (current_char, next_char, probability))

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения
    conn.close()


if __name__ == "__main__":
    pushkin_url = "https://all-the-books.ru/books/pushkin-aleksandr-sbornik-skazok-dlya-detey/"
    pushkin_text = get_pushkin_fairytales(pushkin_url)
    markov_chain_table = create_markov_chain_table(pushkin_text)
    save_to_database(markov_chain_table)
