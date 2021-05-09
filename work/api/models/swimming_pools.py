from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

DeclarativeBase = declarative_base()

class Swimming_pool(DeclarativeBase):
    __tablename__ = 'Swimming_pools'

    id = Column('id',Integer, primary_key=True)
    lines = Column('lines', Integer)
    location = Column('location', Integer, ForeignKey('Pools_locations.id'))
    type_of_water = Column('type_of_water', Integer, ForeignKey('Types_of_water.type'))
    capacity = Column('capacity', Integer)
    monetary_policy = Column('monetary_policy', Integer, ForeignKey('monetary_policies.id'))

    def __repr__(self):
        return f"{self.id}"

class Pool_location(DeclarativeBase):
    __tablename__ = 'Pools_locations'

    id = Column('id',Integer, primary_key=True)
    address = Column('address', String)
    city = Column('city', Integer, ForeignKey('Cities.id'))

class City(DeclarativeBase):
    __tablename__ = 'Cities'

    id = Column('id', Integer, primary_key=True)
    city = Column('city', String)
    
    def __repr__(self):
        return f'{self.id}: {self.city}'

class Type_of_water(DeclarativeBase):
    __tablename__ = 'Types_of_water'

    type = Column('type',Integer, primary_key=True)
    capacity_per_line = Column('capacity_per_line', Integer)
    description = Column('description', String)

class Monetary_policy(DeclarativeBase):
    __tablename__ = 'Monetary_policies'

    id = Column('id',Integer, primary_key=True)
    ticket_price = Column('ticket_price', Integer)
    discount = Column('preferential_discount', Float)
    date_of_adoption = Column('date_of_adoption', String)

class Ticket_type(DeclarativeBase):
    __tablename__ = 'Ticket_types'

    type = Column('type',Integer, primary_key=True)
    description = Column('description', String)

Swimming_pool_table = Table('Tickets', metadata, 
    Column('id',Integer, primary_key=True),
    Column('lines', Integer),
    Column('location', Integer, ForeignKey('Pools_locations.id')),
    Column('type_of_water', Integer, ForeignKey('Types_of_water.type')),
    Column('capacity', Integer),
    Column('monetary_policy', Integer, ForeignKey('monetary_policies.id'))
    )
