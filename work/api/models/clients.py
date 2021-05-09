from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

DeclarativeBase = declarative_base()

class Client(DeclarativeBase):
    __tablename__ = 'Clients'

    id = Column('id',Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    patronymic_name = Column('patronymic_name', String)
    date_registration = Column('date_registration', String)
    birth = Column('birth', String)
    phone = Column('phone', String)

    def __repr__(self):
        return f"{self.surname}"

    def getClientInsert(data):
        client = Client_table.insert().values(
        name = 'Unknown' if data[0] == None else str(data[0]),
        surname = 'Unknown' if data[1] == None else str(data[1]),
        patronymic_name = None if data[2] == None else str(data[2]),
        birth = '2020-01-01' if data[3] == None else str(data[3]),
        date_registration = '2020-01-01' if data[4] == None else str(data[4]),
        phone = '+7000000000' if data[5] == 'None' else str(data[5]),
        )
        
        return client
Client_table = Table('Clients', metadata, 
    Column('id',Integer, primary_key=True),
    Column('name', String),
    Column('surname', String),
    Column('patronymic_name', String),
    Column('date_registration', String),
    Column('birth', String),
    Column('phone', String)
    )
