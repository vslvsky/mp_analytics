from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from wb_invest_stat.ozon.DB import connect_db
from wb_invest_stat.ozon.DB.models.companies import Company


class APIKey(connect_db.Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    client_id = Column(Integer, ForeignKey('companies.client_id'), nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    company = relationship("Company", foreign_keys=[company_id])
    client = relationship("Company", foreign_keys=[client_id])
