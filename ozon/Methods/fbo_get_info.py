from datetime import datetime

from wb_invest_stat.ozon.DB import connect_db
from wb_invest_stat.ozon.DB.commands import get_execution_time
from wb_invest_stat.ozon.DB.methods_commands.fbo_get_info_commands import get_all_posting_numbers_for_client, set_info_variables, \
    try_to_find_fbo_info, add_fbo_info
from wb_invest_stat.ozon.DB.methods_commands.product_list_commands import get_client_id_and_api_keys
from wb_invest_stat.ozon.DB.models.fbo_get_info import FBOInfo
from wb_invest_stat.ozon.Parser.OzonRequest import Request
from wb_invest_stat.wb.connectors import VitalityBooster as vb

NAME_MODULE = 'OZON_fbo_get_info'

if __name__ == '__main__':
    try:
        start_work_time = datetime.now()
        print(f'Start work in {NAME_MODULE} at {start_work_time}')

        connect_db.Base.metadata.create_all(bind=connect_db.engine)
        req = Request(level='v2', target='posting', method='fbo/get')

        for client_id, api_key in get_client_id_and_api_keys():
            fbo_info_list_to_insert = []
            posting_numbers = get_all_posting_numbers_for_client(client_id=client_id)

            for number in posting_numbers:
                data = req.get_fbo_info(
                    headers={'Client-Id': str(client_id), 'Api-Key': api_key}, posting_number=number
                )
                if data is None:
                    print(f'Error with client id - {client_id} and posting number - {number}')
                    continue
                fbo_analytics_variables = set_info_variables(data.get('analytics_data'), type_res='analytics')
                fbo_clusters_variables = set_info_variables(data.get('financial_data'), type_res='clusters')

                products = data.get('financial_data').get('products')
                for product in products:
                    fbo_info = {'posting_number': data.get('posting_number')}
                    fbo_financial_variables = set_info_variables(product, type_res='financial')
                    fbo_item_services_variables = set_info_variables(product.get('item_services'),
                                                                     type_res='item_services')

                    fbo_info.update(fbo_analytics_variables)
                    fbo_info.update(fbo_clusters_variables)
                    fbo_info.update(fbo_financial_variables)
                    fbo_info.update(fbo_item_services_variables)

                    if not try_to_find_fbo_info(client_id=client_id, **fbo_info):
                        fbo_info_db = FBOInfo(client_id=client_id, **fbo_info)
                        fbo_info_list_to_insert.append(fbo_info_db)

            if fbo_info_list_to_insert:
                add_fbo_info(list_fbo_info=fbo_info_list_to_insert)

        end_work_time = datetime.now()
        print(f'Work done at {end_work_time}')
        vb.send_successfully(NAME_MODULE, time=get_execution_time(start_work_time, end_work_time))
    except Exception as e:
        print(e)
        vb.send_error(e, NAME_MODULE)
