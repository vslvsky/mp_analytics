from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Float, Date
from sqlalchemy.orm import relationship

from wb_invest_stat.ozon.DB import connect_db

from wb_invest_stat.ozon.DB.models.companies import Company


class FinanceRealization(connect_db.Base):
    __tablename__ = 'finance_realization'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    client_id = Column(Integer, ForeignKey('companies.client_id'), nullable=False, index=True)

    num = Column(String, index=True)
    doc_date = Column(Date)
    contract_date = Column(String)
    contract_num = Column(String)
    currency_code = Column(String)
    doc_amount = Column(Float)
    vat_amount = Column(Float)
    payer_inn = Column(String)
    payer_kpp = Column(String)
    payer_name = Column(String)
    rcv_inn = Column(String)
    rcv_kpp = Column(String)
    rcv_name = Column(String)
    start_date = Column(Date)
    stop_date = Column(Date)

    row_number = Column(Integer, index=True)
    product_id = Column(BigInteger, index=True)
    product_name = Column(String, index=True)
    barcode = Column(String)
    offer_id = Column(String, index=True)
    commission_percent = Column(Float)
    price = Column(Float)
    price_sale = Column(Float)
    sale_amount = Column(Float)
    sale_commission = Column(Float)
    sale_discount = Column(Float)
    sale_price_seller = Column(Float)
    sale_qty = Column(Integer)
    return_sale = Column(Float)
    return_amount = Column(Float)
    return_commission = Column(Float)
    return_discount = Column(Float)
    return_price_seller = Column(Float)
    return_qty = Column(Integer)

    client = relationship("Company", foreign_keys=[client_id])
