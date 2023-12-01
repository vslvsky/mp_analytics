import environs

from wb_invest_stat.ozon.DB import connect_db
from wb_invest_stat.ozon.DB.commands import add_companies_and_api_keys, change_api_key_for_company


def set_companies_data(companies_data: list):
    add_companies_and_api_keys(companies_data=companies_data)


def update_companies_api_keys(new_companies_data: list):
    change_api_key_for_company(companies_data=new_companies_data)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    connect_db.Base.metadata.create_all(bind=connect_db.engine)

    main_companies_data = [
        {
            'company_id': 1,
            'client_id': 1194703,
            'name': 'ООО УК ВЕРОЙ',
            'api_key': env('API_KEY_1')
        },
        {
            'company_id': 2,
            'client_id': 1201673,
            'name': 'ООО АЛЬТЕРНАТИВА',
            'api_key': env('API_KEY_2')
        },
        {
            'company_id': 3,
            'client_id': 1192280,
            'name': 'ООО ВБ ИНВЕСТ',
            'api_key': env('API_KEY_3')
        },
        {
            'company_id': 7,
            'client_id': 293313,
            'name': 'ИП Записоцкий Н.В.',
            'api_key': env('API_KEY_7')
        },
        {
            'company_id': 8,
            'client_id': 1201399,
            'name': 'ИП Фендель Р.В.',
            'api_key': env('API_KEY_8')
        },
        {
            'company_id': 9,
            'client_id': 1384633,
            'name': 'ИП Сердюк М.С.',
            'api_key': env('API_KEY_9')
        },
        {
            'company_id': 11,
            'client_id': 459385,
            'name': 'ИП Набока В.В.',
            'api_key': env('API_KEY_11')
        }
    ]

    set_companies_data(main_companies_data)
