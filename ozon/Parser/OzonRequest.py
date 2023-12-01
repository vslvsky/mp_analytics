from datetime import datetime, timedelta
from time import sleep

import requests


class Request:
    def __init__(self, level: str = 'v2', target: str = 'product', method: str = 'list'):
        self.url = f'https://api-seller.ozon.ru/{level}/{target}/{method}'

    def get_json_data(self, **kwargs):
        json_data = {}

        for key, value in kwargs.items():
            json_data[key] = value

        return json_data

    def send_post_request(self, headers: dict, json: dict = {}):
        response = requests.post(self.url, headers=headers, json=json)
        response.raise_for_status()

        return response.json()


    def get_product_info(self, headers: dict, product_id: int, offer_id: str = "", sku: int = 0):
        try:
            data = self.send_post_request(headers=headers, json={
                "offer_id": offer_id,
                "product_id": product_id,
                "sku": sku
            })['result']
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None


    def get_fbo_info(self, headers: dict, posting_number: str, translit: bool = True, analytics_data: bool = True,
                     financial_data: bool = True):
        try:
            data = self.send_post_request(headers=headers, json={
                "posting_number": posting_number,
                "translit": translit,
                "with": {
                    "analytics_data": analytics_data,
                    "financial_data": financial_data
                }
            })['result']
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None


    def get_analytics_stock_on_warehouses(self,
                                          headers: dict,
                                          limit: int = 1000,
                                          offset: int = 0,
                                          warehouse_type: str = 'ALL'):
        try:
            data = self.send_post_request(
                headers=headers,
                json={
                    "limit": limit,
                    "offset": offset,
                    "warehouse_type": warehouse_type
                }
            )['result']['rows']
            return data
        except Exception as e:
            print(e)
            return None


    def get_finance_realization(self,
                                headers: dict,
                                date: str = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")
                                ):
        try:
            data = self.send_post_request(
                headers=headers,
                json={
                    "date": date
                }
            ).get('result', None)

            return data
        except Exception as e:
            print(e)
            return None
