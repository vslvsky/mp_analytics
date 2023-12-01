from wb_invest_stat.ozon.DB.connect_db import session
from wb_invest_stat.ozon.DB.models.fbo_get_info import FBOInfo
from wb_invest_stat.ozon.DB.models.fbo_list import FBOList


def get_all_posting_numbers_for_client(client_id: int):
    posting_numbers = session.query(FBOList.posting_number).filter(FBOList.client_id == client_id).all()

    return [posting[0] for posting in posting_numbers]


def try_to_find_fbo_info(client_id: int, **kwargs):
    product_id = kwargs.pop('product_id', None)
    posting_number = kwargs.pop('posting_number', None)
    fbo_info = session.query(FBOInfo).filter_by(
        posting_number=posting_number, client_id=client_id, product_id=product_id
    ).first()

    if not fbo_info: return False
    fbo_info.client_id = client_id
    for key, value in kwargs.items():
        setattr(fbo_info, key, value)
    session.commit()
    return True


def add_fbo_info(list_fbo_info: list):
    session.bulk_save_objects(list_fbo_info)
    session.commit()


def set_info_variables(data, type_res: str):
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

    def extract_float_value(key):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        try:
            return float(value) if value != '' else None
        except (ValueError, TypeError):
            return None

    def extract_string_value(key):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k)
            if value is None:
                return None
        return value if value != '' else None

    def extract_bool_value(key):
        keys = key.split('.')
        value = data
        for k in keys:
            value = value.get(k)
            if value is None:
                return False
        return value if isinstance(value, bool) else False

    if type_res == 'analytics':
        return {
            'analytics_region': extract_string_value('region'),
            'analytics_city': extract_string_value('city'),
            'analytics_delivery_type': extract_string_value('delivery_type'),
            'analytics_is_premium': extract_bool_value('is_premium'),
            'analytics_payment_type_group_name': extract_string_value('payment_type_group_name'),
            'analytics_warehouse_id': extract_int_value('warehouse_id'),
            'analytics_warehouse_name': extract_string_value('warehouse_name'),
            'analytics_is_legal': extract_bool_value('is_legal')
        }
    if type_res == 'financial':
        return {
            'commission_amount': extract_float_value('commission_amount'),
            'commission_percent': extract_int_value('commission_percent'),
            'payout': extract_float_value('payout'),
            'product_id': extract_int_value('product_id'),
            'old_price': extract_float_value('old_price'),
            'price': extract_float_value('price'),
            'total_discount_value': extract_int_value('total_discount_value'),
            'total_discount_percent': extract_float_value('extract_float_value'),
            'actions': extract_string_value('actions'),
            'quantity': extract_float_value('quantity'),
            'client_price': extract_float_value('client_price'),
        }
    if type_res == 'item_services':
        return {
            'marketplace_service_item_fulfillment': extract_float_value('marketplace_service_item_fulfillment'),
            'marketplace_service_item_pickup': extract_float_value('marketplace_service_item_pickup'),
            'marketplace_service_item_dropoff_pvz': extract_float_value('marketplace_service_item_dropoff_pvz'),
            'marketplace_service_item_dropoff_sc': extract_float_value('marketplace_service_item_dropoff_sc'),
            'marketplace_service_item_dropoff_ff': extract_float_value('marketplace_service_item_dropoff_ff'),
            'marketplace_service_item_direct_flow_trans': extract_float_value(
                'marketplace_service_item_direct_flow_trans'),
            'marketplace_service_item_return_flow_trans': extract_float_value(
                'marketplace_service_item_return_flow_trans'),
            'marketplace_service_item_deliv_to_customer': extract_float_value(
                'marketplace_service_item_deliv_to_customer'),
            'marketplace_service_item_return_not_deliv_to_customer': extract_float_value(
                'marketplace_service_item_return_not_deliv_to_customer'),
            'marketplace_service_item_return_part_goods_customer': extract_float_value(
                'marketplace_service_item_return_part_goods_customer'),
            'marketplace_service_item_return_after_deliv_to_customer': extract_float_value(
                'marketplace_service_item_return_after_deliv_to_customer')
        }
    if type_res == 'clusters':
        return {
            'cluster_from': extract_string_value('cluster_from'),
            'cluster_to': extract_string_value('cluster_to')
        }
