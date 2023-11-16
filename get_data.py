import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('url')
api_key = os.getenv('api_key')
page_number = 1 #Номер страницы
total_pages = 1 #Начальное значение страницы


# Создаем словарь данных
data_to_send = {"data": []}

while page_number <= total_pages and len(data_to_send["data"]) < 5:
    params = {
        'page': page_number,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        orders = response.json()
        total_pages = orders['pagination']['totalPageCount']

        # Проходим по каждому заказу
        for order in orders['orders']:
            # Проходим по каждому товару в заказе
            for item in order['items']:
                prices = item.get('prices', [])
                offer = item.get('offer', {})
                unit = offer.get('unit', {})
                purchase_price = item.get('purchasePrice')

                # Добавляем данные о товаре в data_to_send
                data_to_send["data"].append({
                    'bonusesChargeTotal': item.get('bonusesChargeTotal'),
                    'bonusesCreditTotal': item.get('bonusesCreditTotal'),
                    'initialPrice': item.get('initialPrice'),
                    'discountTotal': int(float(item.get('discountTotal'))),
                    'vatRate': int(
                        float(item.get('vatRate'))
                        ) if '.' in item.get('vatRate') else 'N/A',
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
                    'offer_properties_type': str(
                        offer.get('properties', {}).get('type')
                        ),
                    'offer_unit_code': str(unit.get('code')),
                    'offer_unit_name': str(unit.get('name')),
                    'offer_unit_sym': str(unit.get('sym')),
                    'price': str(prices[0].get('price')) if prices else 'N/A',
                })

            # Если мы собрали данные для 5 товаров, выходим из цикла
            if len(data_to_send["data"]) >= 100:
                break

        # Сохраняем данные в JSON файл
        with open('orders_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_to_send, json_file, ensure_ascii=False, indent=2)

        print(f"Страница {page_number} обработана "
              f"данные сохранены в orders_data.json.")
        page_number += 1

        # Добавляем задержку между сбором данных
        time.sleep(5)
    else:
        print(f"Ошибка при запросе: {response.status_code}, {response.text}")
        break
