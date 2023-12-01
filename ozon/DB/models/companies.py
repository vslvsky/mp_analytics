import datetime

from sqlalchemy import Column, Integer, Date, Boolean, String

from wb_invest_stat.ozon.DB import connect_db


class Company(connect_db.Base):
    __tablename__ = 'companies'

    company_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=False)
    client_id = Column(Integer, nullable=False, unique=True)
    created_at = Column(Date, nullable=False, default=datetime.date.today())
    name = Column(String, nullable=False)
    deleted_at = Column(Date)
    is_deleted = Column(Boolean, default=False)
