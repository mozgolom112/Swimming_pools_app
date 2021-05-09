from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()


DeclarativeBase = declarative_base()

class Daily_earning(DeclarativeBase):
    __tablename__ = 'Daily_earnings'
    
    date = Column('date_',Integer)
    id_pool = Column('id_pool', Integer, ForeignKey('Swimming_pools.id'))
    clients = Column('clients', Integer)
    workload = Column('workload', Float)
    proceeds = Column('proceeds', Float)
    monetary_policy = Column('monetary_policy', Integer, ForeignKey('monetary_policies.id'))
    discount_clients = Column('discount_clients', Integer)
    report_uuid = Column('report_id', String, primary_key=True)

    def __repr__(self):
        return f"{self.id_pool}"

