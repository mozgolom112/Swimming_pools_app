from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

DeclarativeBase = declarative_base()

class Swimming_session(DeclarativeBase):
    __tablename__ = 'Swimming_sessions'

    id = Column('id',Integer, primary_key=True)
    id_pool= Column('id_pool', Integer, ForeignKey('Swimming_pools.id'))
    entry_tickets = Column('entry_tickets', Integer)
    discount_tickets = Column('discount_tickets', Integer)
    workload = Column('workload', Float)
    date_and_time = Column('date_and_time', String)
    
    def __repr__(self):
        return f"{self.id} - {self.date_and_time}"