from datetime import datetime

from wb_invest_stat.ozon.DB import connect_db
from wb_invest_stat.ozon.DB.commands import get_execution_time
from wb_invest_stat.ozon.DB.methods_commands.finance_realization_commands import try_to_find_finance_realization_row, \
    add_finance_realization
from wb_invest_stat.ozon.DB.methods_commands.product_list_commands import get_client_id_and_api_keys
from wb_invest_stat.ozon.DB.models.finance_realization import FinanceRealization
from wb_invest_stat.ozon.Parser.OzonRequest import Request
from wb_invest_stat.wb.connectors import VitalityBooster as vb

NAME_MODULE = 'OZON_finance_realization'

if __name__ == '__main__':
    try:
        start_work_time = datetime.now()
        print(f'Start work in {NAME_MODULE} at {start_work_time}')

        connect_db.Base.metadata.create_all(bind=connect_db.engine)
        req = Request(level='v1', target='finance', method='realization')

        for client_id, api_key in get_client_id_and_api_keys():
            finance_realization_list = []
            data = req.get_finance_realization(headers={'Client-Id': str(client_id), 'Api-Key': api_key})

            if data is None:
                print(f'Problem with client id - {client_id}')
                continue

            header_info = data.get('header', None)
            rows_info = data.get('rows', None)

            for row_info in rows_info:
                finance_realization_variables = {}
                finance_realization_variables.update(header_info)
                finance_realization_variables.update(row_info)

                if not try_to_find_finance_realization_row(client_id=client_id, **finance_realization_variables):
                    finance_realization_item_db = FinanceRealization(
                        client_id=client_id, **finance_realization_variables
                    )
                    finance_realization_list.append(finance_realization_item_db)

            if finance_realization_list:
                add_finance_realization(finance_realization_list=finance_realization_list)

        end_work_time = datetime.now()
        print(f'Work done at {end_work_time}')
        vb.send_successfully(NAME_MODULE, time=get_execution_time(start_work_time, end_work_time))
    except Exception as e:
        print(e)
        vb.send_error(e, NAME_MODULE)
