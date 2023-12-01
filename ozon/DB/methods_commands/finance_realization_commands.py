from wb_invest_stat.ozon.DB.connect_db import session
from wb_invest_stat.ozon.DB.models.finance_realization import FinanceRealization


def try_to_find_finance_realization_row(client_id: int, **kwargs):
    num = kwargs.pop('num', None)
    row_number = kwargs.pop('row_number', None)
    doc_date = kwargs.pop('doc_date', None)

    finance_realization_row = session.query(FinanceRealization).filter_by(
        client_id=client_id, num=num, row_number=row_number, doc_date=doc_date
    ).first()

    if not finance_realization_row: return False
    finance_realization_row.client_id = client_id
    for key, value in kwargs.items():
        setattr(finance_realization_row, key, value)
    session.commit()
    return True


def add_finance_realization(finance_realization_list: list):
    session.bulk_save_objects(finance_realization_list)
    session.commit()
