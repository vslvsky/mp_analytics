from wb_invest_stat.ozon.DB.connect_db import session
from wb_invest_stat.ozon.DB.models.product_info import ProductInfo
from wb_invest_stat.ozon.DB.models.product_list import Product


def get_all_products_for_client(client_id: int):
    products = session.query(Product.product_id).filter(Product.client_id == client_id).all()
    return [product[0] for product in products]


def try_to_find_product_info(product_id, client_id, **kwargs):
    product = session.query(ProductInfo).filter_by(product_id=product_id).first()

    if not product: return False
    product.client_id = client_id
    for key, value in kwargs.items():
        setattr(product, key, value)
    session.commit()
    return True


def add_products_info(list_info_products: list):
    session.bulk_save_objects(list_info_products)
    session.commit()


def set_variables(data):
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

    def extract_nested_value(keys):
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, list):
                try:
                    index = int(key)
                    value = value[index] if index < len(value) else None
                except (ValueError, IndexError, TypeError):
                    return None
            else:
                return None
        return value

    name = extract_string_value('name')
    offer_id = extract_string_value('offer_id')
    barcode = extract_string_value('barcode')
    created_at = extract_string_value('created_at')
    images = extract_string_value('images')
    marketing_price = extract_float_value('marketing_price')
    old_price = extract_float_value('old_price')
    premium_price = extract_float_value('premium_price')
    price = extract_float_value('price')
    recommended_price = extract_float_value('recommended_price')
    min_price = extract_float_value('min_price')

    sources_fbo_sku = extract_nested_value(['sources', 1, 'sku'])
    sources_fbs_sku = extract_nested_value(['sources', 0, 'sku'])

    stocks_coming = extract_int_value('stocks.coming')
    stocks_present = extract_int_value('stocks.present')
    stocks_reserved = extract_int_value('stocks.reserved')
    errors = extract_string_value('errors')
    vat = extract_float_value('vat')
    visible = extract_bool_value('visible')
    visibility_details_has_price = extract_bool_value('visibility_details.has_price')
    visibility_details_has_stock = extract_bool_value('visibility_details.has_stock')
    visibility_details_active_product = extract_bool_value('visibility_details.active_product')

    volume_weight = extract_float_value('volume_weight')
    is_prepayment = extract_bool_value('is_prepayment')
    is_prepayment_allowed = extract_bool_value('is_prepayment_allowed')
    images360 = extract_string_value('images360')
    color_image = extract_string_value('color_image')
    primary_image = extract_string_value('primary_image')

    status = extract_nested_value(['status', 'state'])
    status_state_name = extract_nested_value(['status', 'state_name'])
    status_state_description = extract_nested_value(['status', 'state_description'])
    status_state_tooltip = extract_nested_value(['status', 'state_tooltip'])

    item_errors_description = extract_nested_value(['status', 'item_errors', 0, 'description'])
    item_errors_matched_offer_id = extract_nested_value(
        ['status', 'item_errors', 0, 'optional_description_elements', 'matched_offer_id'])

    moderate_status = extract_nested_value(['status', 'moderate_status'])
    state = extract_string_value('state')
    currency_code = extract_string_value('currency_code')
    is_kgt = extract_bool_value('is_kgt')

    discounted_stocks_coming = extract_int_value('discounted_stocks.coming')
    discounted_stocks_present = extract_int_value('discounted_stocks.present')
    discounted_stocks_reserved = extract_int_value('discounted_stocks.reserved')
    is_discounted = extract_bool_value('is_discounted')
    has_discounted_item = extract_bool_value('has_discounted_item')
    barcodes = extract_string_value('barcodes')
    updated_at = extract_string_value('updated_at')

    price_index = extract_string_value('price_indexes.price_index')

    external_price_min_price = extract_string_value('price_indexes.external_index_data.minimal_price')
    external_price_index_value = extract_float_value('price_indexes.external_index_data.price_index_value')

    ozon_price_min_price = extract_string_value('price_indexes.ozon_index_data.minimal_price')
    ozon_price_index_value = extract_float_value('price_indexes.ozon_index_data.price_index_value')

    marketplaces_price_min_price = extract_string_value('price_indexes.self_marketplaces_index_data.minimal_price')
    marketplaces_price_index_value = extract_float_value('price_indexes.self_marketplaces_index_data.price_index_value')

    sku = extract_int_value('sku')
    description_category_id = extract_int_value('description_category_id')

    return {
        'name': name,
        'offer_id': offer_id,
        'barcode': barcode,
        'created_at': created_at,
        'images': images,
        'marketing_price': marketing_price,
        'old_price': old_price,
        'premium_price': premium_price,
        'price': price,
        'recommended_price': recommended_price,
        'min_price': min_price,
        'sources_fbo_sku': sources_fbo_sku,
        'sources_fbs_sku': sources_fbs_sku,
        'stocks_coming': stocks_coming,
        'stocks_present': stocks_present,
        'stocks_reserved': stocks_reserved,
        'errors': errors,
        'vat': vat,
        'visible': visible,
        'visibility_details_has_price': visibility_details_has_price,
        'visibility_details_has_stock': visibility_details_has_stock,
        'visibility_details_active_product': visibility_details_active_product,
        'volume_weight': volume_weight,
        'is_prepayment': is_prepayment,
        'is_prepayment_allowed': is_prepayment_allowed,
        'images360': images360,
        'color_image': color_image,
        'primary_image': primary_image,
        'status': status,
        'status_state_name': status_state_name,
        'status_state_description': status_state_description,
        'status_state_tooltip': status_state_tooltip,
        'item_errors_description': item_errors_description,
        'item_errors_matched_offer_id': item_errors_matched_offer_id,
        'moderate_status': moderate_status,
        'state': state,
        'currency_code': currency_code,
        'is_kgt': is_kgt,
        'discounted_stocks_coming': discounted_stocks_coming,
        'discounted_stocks_present': discounted_stocks_present,
        'discounted_stocks_reserved': discounted_stocks_reserved,
        'is_discounted': is_discounted,
        'has_discounted_item': has_discounted_item,
        'barcodes': barcodes,
        'updated_at': updated_at,
        'price_index': price_index,
        'external_price_min_price': external_price_min_price,
        'external_price_index_value': external_price_index_value,
        'ozon_price_min_price': ozon_price_min_price,
        'ozon_price_index_value': ozon_price_index_value,
        'marketplaces_price_min_price': marketplaces_price_min_price,
        'marketplaces_price_index_value': marketplaces_price_index_value,
        'sku': sku,
        'description_category_id': description_category_id
    }

