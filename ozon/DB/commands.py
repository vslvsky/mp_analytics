from datetime import datetime

from wb_invest_stat.ozon.DB.models_commands import add_company, add_api_key, change_api_key


def add_companies_and_api_keys(companies_data: list):
    for company_info in companies_data:
        add_company(company_info['company_id'], company_info['client_id'], company_info['name'])
        add_api_key(company_info['api_key'], company_info['company_id'], company_info['client_id'])


def change_api_key_for_company(companies_data: list):
    for company_info in companies_data:
        change_api_key(company_id=company_info['company_id'], api_key=company_info['api_key'],
                       client_id=company_info['client_id'])


def get_execution_time(time_start: datetime, time_end: datetime) -> str:
    time_difference = time_end - time_start
    seconds = time_difference.seconds
    milliseconds = int(time_difference.microseconds / 1000)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} мин, {seconds} сек, {milliseconds} мс"
