from wb_invest_stat.ozon.DB.connect_db import session
from wb_invest_stat.ozon.DB.models.analytics_stocks import AnalyticsStocks


def try_to_find_analytics_stocks(client_id: int, **kwargs):
    sku = kwargs.pop('sku', None)
    warehouse_name = kwargs.pop('warehouse_name', None)
    item_code = kwargs.pop('item_code', None)

    analytics_stocks = session.query(AnalyticsStocks).filter_by(
        sku=sku, client_id=client_id, warehouse_name=warehouse_name, item_code=item_code
    ).first()

    if not analytics_stocks: return False
    analytics_stocks.client_id = client_id
    for key, value in kwargs.items():
        setattr(analytics_stocks, key, value)
    session.commit()
    return True


def add_analytics_stocks_data(list_analytics_stocks_data: list):
    session.bulk_save_objects(list_analytics_stocks_data)
    session.commit()


def set_analytics_stocks_variables(data):
    def extract_string_value(key):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value if value != '' else None

    def extract_int_value(key):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        try:
            return int(value) if value != '' else None
        except (ValueError, TypeError):
            return None

    return {
        'sku': extract_int_value('sku'),
        'warehouse_name': extract_string_value('warehouse_name'),
        'item_code': extract_string_value('item_code'),
        'item_name': extract_string_value('item_name'),
        'promised_amount': extract_int_value('promised_amount'),
        'free_to_sell_amount': extract_int_value('free_to_sell_amount'),
        'reserved_amount': extract_int_value('reserved_amount')
    }
