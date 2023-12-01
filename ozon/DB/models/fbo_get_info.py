from sqlalchemy import Column, Integer, Date, String, ForeignKey, JSON, Boolean, BigInteger, Float
from sqlalchemy.orm import relationship

from wb_invest_stat.ozon.DB import connect_db

from wb_invest_stat.ozon.DB.models.companies import Company


class FBOInfo(connect_db.Base):
    __tablename__ = 'fbo_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('companies.client_id'), nullable=False, index=True)
    posting_number = Column(String, index=True)

    analytics_region = Column(String)
    analytics_city = Column(String)
    analytics_delivery_type = Column(String)
    analytics_is_premium = Column(Boolean)
    analytics_payment_type_group_name = Column(String)
    analytics_warehouse_id = Column(BigInteger)
    analytics_warehouse_name = Column(String)
    analytics_is_legal = Column(Boolean)

    commission_amount = Column(Float)
    commission_percent = Column(Integer)
    payout = Column(Float)
    product_id = Column(BigInteger)
    old_price = Column(Float)
    price = Column(Float)
    total_discount_value = Column(Integer)
    total_discount_percent = Column(Float)
    actions = Column(String)
    quantity = Column(Float)
    client_price = Column(Float, nullable=True)

    marketplace_service_item_fulfillment = Column(Float)
    marketplace_service_item_pickup = Column(Float)
    marketplace_service_item_dropoff_pvz = Column(Float)
    marketplace_service_item_dropoff_sc = Column(Float)
    marketplace_service_item_dropoff_ff = Column(Float)
    marketplace_service_item_direct_flow_trans = Column(Float)
    marketplace_service_item_return_flow_trans = Column(Float)
    marketplace_service_item_deliv_to_customer = Column(Float)
    marketplace_service_item_return_not_deliv_to_customer = Column(Float)
    marketplace_service_item_return_part_goods_customer = Column(Float)
    marketplace_service_item_return_after_deliv_to_customer = Column(Float)

    cluster_from = Column(String, nullable=True)
    cluster_to = Column(String, nullable=True)

    client = relationship("Company", foreign_keys=[client_id])
