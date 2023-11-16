import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Загружаем данные из JSON файла
with open('orders_data.json', 'r', encoding='utf-8') as json_file:
    try:
        data_to_send = json.load(json_file)
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON файла.")
        data_to_send = None

    # Разбиваем данные на группы по 3 массива
    chunk_size = 3
    chunks = [
        data_to_send["data"][i:i + chunk_size] for i in range
        (0, len(data_to_send["data"]), chunk_size)
        ]

    server_url = os.getenv('server_url')
    headers = {'Content-Type': 'application/json'}

    for chunk in chunks:
        # Отправляем данные на сервер
        server_response = requests.post(
            server_url, json={"data": chunk}, headers=headers
            )

        # Выводим ответ сервера
        try:
            response_json = server_response.json()
            print(response_json)
        except json.JSONDecodeError:
            print(
                f"Ошибка при декодировании JSON ответа: {server_response.text}"
                )
            response_json = None

        # Проверяем статус ответа сервера
        if server_response.status_code == 200:
            # Проверяем, есть ли в ответе поле "status" и оно равно True
            if response_json and response_json.get("status") is True:
                print("Данные успешно отправлены на сервер.")
            else:
                print("Ошибка на сервере. Подробности:", response_json.get(
                    "message"
                    ))
        else:
            print(
                f"Ошибка при отправке данных на сервер:
                 {server_response.status_code}, {server_response.text}"
                 )

        # Добавляем задержку между отправками (3 секунды)
        time.sleep(3)
