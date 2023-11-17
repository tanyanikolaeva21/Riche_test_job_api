import requests
import json
import time
import os
from io import StringIO
from dotenv import load_dotenv

load_dotenv()
user = 'НиколаеваТ'

# Сначала собираем данные
url = os.getenv('url')
api_key = os.getenv('api_key')
server_url = os.getenv('server_url')
page_number = 1  # начинаем с первой страницы
total_pages = 1  # устанавливаем начальное значение

# Создаем строковый буфер для данных, который соответствует вашему ожиданию
data_to_send_buffer = StringIO()
data_to_send_buffer.write('{"data": []}')

while page_number <= total_pages and len(
    json.loads(data_to_send_buffer.getvalue())["data"]
    ) < 5:
    params = {
        'page': page_number,
        'user': user,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        orders = response.json()
        total_pages = orders['pagination']['totalPageCount']

        # Создаем список для хранения данных внутри цикла
        data_list = []

        # Проходим по каждому заказу
        for order in orders['orders']:
            # Проходим по каждому товару в заказе
            for item in order['items']:
                prices = item.get('prices', [])
                offer = item.get('offer', {})
                unit = offer.get('unit', {})
                purchase_price = item.get('purchasePrice')

                # Добавляем данные о товаре в data_list
                data_list.append({
                    'bonusesChargeTotal': item.get('bonusesChargeTotal'),
                    'bonusesCreditTotal': item.get('bonusesCreditTotal'),
                    'initialPrice': item.get('initialPrice'),
                    'discountTotal': int(float(item.get('discountTotal'))),
                    'vatRate': int(float(item.get('vatRate'))) if '.' in item.get('vatRate') else 'N/A',
                    'createdAt': order.get('createdAt'),
                    'quantity_1': prices[0].get('quantity'),
                    'status': str(item.get('status')),
                    'purchasePrice': str(purchase_price),
                    'ordering': item.get('ordering'),
                    'offer_displayName': str(offer.get('displayName')),
                    'offer_id': str(offer.get('id')),
                    'offer_externalId': int(float(offer.get('externalId'))),
                    'offer_xmlId': str(offer.get('xmlId')),
                    'offer_name': str(offer.get('name')),
                    'offer_article': str(offer.get('article')),
                    'offer_vatRate': str(offer.get('vatRate')),
                    'offer_properties_type': str(offer.get('properties', {}).get('type')),
                    'offer_unit_code': str(unit.get('code')),
                    'offer_unit_name': str(unit.get('name')),
                    'offer_unit_sym': str(unit.get('sym')),
                    'price': str(prices[0].get('price')) if prices else 'N/A',
                })

            if len(data_list) >= 100:
                break

        # Обновляем данные в буфере
        data_to_send_buffer.seek(0)
        existing_data = json.load(data_to_send_buffer)
        existing_data["data"].extend(data_list)
        data_to_send_buffer.seek(0)
        json.dump(existing_data, data_to_send_buffer, ensure_ascii=False, indent=2)
        data_to_send_buffer.truncate()

        print(f"Страница {page_number} обработана.")
        page_number += 1

        # Добавляем задержку между сбором данных
        time.sleep(5)
    else:
        print(f"Ошибка при запросе: {response.status_code}, {response.text}")
        break

# Затем отправляем данные
data_to_send = json.loads(data_to_send_buffer.getvalue())

# Загружаем данные из JSON файла
try:
    data_to_send = json.loads(data_to_send_buffer.getvalue())
except json.JSONDecodeError:
    print("Ошибка при декодировании JSON файла.")
    data_to_send = None

# Разбиваем данные на группы по 3 массива
chunk_size = 3
chunks = [data_to_send["data"][i:i + chunk_size] for i in range(0, len(data_to_send["data"]), chunk_size)]

headers = {'Content-Type': 'application/json'}

for chunk in chunks:
    # Отправляем данные на сервер
    server_response = requests.post(server_url, json={"data": chunk}, headers=headers)

    # Выводим ответ сервера
    try:
        response_json = server_response.json()
        print(response_json)
    except json.JSONDecodeError:
        print(f"Ошибка при декодировании JSON ответа: {server_response.text}")
        response_json = None

    # Проверяем статус ответа сервера
    if server_response.status_code == 200:
        # Проверяем, есть ли в ответе поле "status" и оно равно True
        if response_json and response_json.get("status") is True:
            print("Данные успешно отправлены на сервер.")
        else:
            print("Ошибка на сервере. Подробности:", response_json.get("message"))
    else:
        print(f"Ошибка при отправке данных на сервер: {server_response.status_code}, {server_response.text}")

    # Добавляем задержку между отправками (в сек)
    time.sleep(3)
