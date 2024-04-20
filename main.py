import requests
import psycopg2

# Параметры для подключения к БД PostgreSQL
DB_NAME = "db_name"
DB_USER = "db_user"
DB_PASSWORD = "db_password"
DB_HOST = "db_host"

# Функция для проверки имени в БД и определения пола
def check_gender(name):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = conn.cursor()

    # Проверяем имя в таблице names_woman
    cursor.execute("SELECT count(*) FROM names_woman WHERE name = %s", (name,))
    count_woman = cursor.fetchone()[0]

    # Проверяем имя в таблице names_man
    cursor.execute("SELECT count(*) FROM names_man WHERE name = %s", (name,))
    count_man = cursor.fetchone()[0]

    if count_woman > 0:
        gender = "Женщина"
    elif count_man > 0:
        gender = "Мужчина"
    else:
        gender = "Неизвестно"

    conn.close()
    return gender

# Функция для отправки данных обратно в Битрикс24 по Webhook
def send_data(contact_id, gender):
    url = "https://bitrix24_domain/rest/contact.update.json"
    params = {
        "ID": contact_id,
        "FIELDS": {
            "UF_GENDER": gender
        }
    }
    response = requests.post(url, json=params)

    return response.json()

# Получение данных по Webhook
webhook_data = {
    "ID": "contact_id",
    "NAME": "Имя контакта"
}

contact_id = webhook_data["ID"]
contact_name = webhook_data["NAME"]

# Проверка пола по имени
gender = check_gender(contact_name)

# Отправка данных обратно в Битрикс24
result = send_data(contact_id, gender)

print(result)