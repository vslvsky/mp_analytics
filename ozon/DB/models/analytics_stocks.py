from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from wb_invest_stat.ozon.DB import connect_db

from wb_invest_stat.ozon.DB.models.companies import Company


class AnalyticsStocks(connect_db.Base):
    __tablename__ = 'analytics_stocks'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    sku = Column(Integer, index=True)
    client_id = Column(Integer, ForeignKey('companies.client_id'), nullable=False, index=True)
    warehouse_name = Column(String, index=True)
    item_code = Column(String, index=True)
    item_name = Column(String)
    promised_amount = Column(Integer)
    free_to_sell_amount = Column(Integer)
    reserved_amount = Column(Integer)

    client = relationship("Company", foreign_keys=[client_id])
