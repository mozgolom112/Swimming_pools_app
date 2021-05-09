from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

DeclarativeBase = declarative_base()

class Ticket(DeclarativeBase):
    __tablename__ = 'Tickets'

    id = Column('id',Integer, primary_key=True)
    id_client = Column('id_client', Integer, ForeignKey('Clients.id'))
    id_training = Column('id_training', Integer, ForeignKey('Training_sessions.id'))
    id_pool = Column('id_pool', Integer, ForeignKey('Swimming_pools.id'))
    type = Column('type', Integer, ForeignKey('Ticket_types.type'))
    date_and_time = Column('date_and_time', String)

    def __repr__(self):
        return f"{self.surname}"

    def getTicketInsert(data):
     
        ticket = Ticket_table.insert().values(
        id_client = None if data[0] == None else int(data[0]),
        id_pool = None if data[1] == 'None' else int(data[1]),
        type = None if data[2] == 'None' else int(data[2]),
        date_and_time = None if data[3] == 'None' else data[3]
        )
        
        return ticket
Ticket_table = Table('Tickets', metadata, 
    Column('id',Integer, primary_key=True),
    Column('id_client', Integer, ForeignKey('Clients.id')),
    Column('id_training', Integer, ForeignKey('Training_sessions.id')),
    Column('id_pool', Integer),
    Column('type', Integer, ForeignKey('Ticket_types.type')),
    Column('date_and_time', String)
    )
