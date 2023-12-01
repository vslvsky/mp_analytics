from sqlalchemy.exc import IntegrityError

from wb_invest_stat.ozon.DB.connect_db import session
from wb_invest_stat.ozon.DB.models.api_keys import APIKey
from wb_invest_stat.ozon.DB.models.companies import Company


def try_to_commit(model):
    session.add(model)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def add_company(company_id: int, client_id: int, name: str):
    company = Company(company_id=company_id, client_id=client_id, name=name)
    try_to_commit(company)


def add_api_key(api_key: str, company_id: int, client_id: int):
    api_key = APIKey(api_key=api_key, company_id=company_id, client_id=client_id)
    try_to_commit(api_key)


def change_api_key(company_id: int, api_key: str, client_id: int):
    company = session.query(APIKey).filter_by(company_id=company_id, client_id=client_id).first()
    if company:
        company.api_key = api_key
        session.commit()
