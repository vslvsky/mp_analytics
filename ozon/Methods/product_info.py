from datetime import datetime

from wb_invest_stat.ozon.DB import connect_db
from wb_invest_stat.ozon.DB.commands import get_execution_time
from wb_invest_stat.ozon.DB.methods_commands.product_info_commands import get_all_products_for_client, try_to_find_product_info, \
    add_products_info, set_variables
from wb_invest_stat.ozon.DB.methods_commands.product_list_commands import get_client_id_and_api_keys
from wb_invest_stat.ozon.DB.models.product_info import ProductInfo
from wb_invest_stat.ozon.Parser.OzonRequest import Request
from wb_invest_stat.wb.connectors import VitalityBooster as vb

NAME_MODULE = 'OZON_product_info'

if __name__ == '__main__':
    try:
        start_work_time = datetime.now()
        print(f'Start work in {NAME_MODULE} at {start_work_time}')

        connect_db.Base.metadata.create_all(bind=connect_db.engine)
        req = Request(level='v2', target='product', method='info')

        for client_id, api_key in get_client_id_and_api_keys():
            products_info_to_insert = []
            list_products_for_client = get_all_products_for_client(client_id=client_id)

            for product_id in list_products_for_client:
                data = req.get_product_info(headers={'Client-Id': str(client_id), 'Api-Key': api_key},
                                            product_id=product_id)

                if data is None:
                    print(f'Error with client id - {client_id} and product id - {product_id}')
                    continue

                variables = set_variables(data)
                if not try_to_find_product_info(data['id'], client_id, **variables):
                    product_info_db = ProductInfo(product_id=data['id'], client_id=client_id, **variables)
                    products_info_to_insert.append(product_info_db)

            if products_info_to_insert:
                add_products_info(list_info_products=products_info_to_insert)

        end_work_time = datetime.now()
        print(f'Work done at {end_work_time}')
        vb.send_successfully(NAME_MODULE, time=get_execution_time(start_work_time, end_work_time))
    except Exception as e:
        vb.send_error(e, NAME_MODULE)
