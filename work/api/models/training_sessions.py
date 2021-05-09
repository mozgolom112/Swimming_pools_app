from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata = MetaData()

DeclarativeBase = declarative_base()

class Training_session(DeclarativeBase):
    __tablename__ = 'Training_sessions'

    id = Column('id',Integer, primary_key=True)
    duration = Column('duration', String)
    swam_distance = Column('swam_distance', Integer)
    heart_rate = Column('heart_rate', Integer)
    spO2 = Column('spO2', Integer)
    crawl = Column('crawl', Integer)
    backstroke = Column('backstroke', Integer)
    breaststroke = Column('breaststroke', Integer)
    butterfly = Column('butterfly', Integer)
    type_of_water = Column('type_of_water', Integer)
    swolf = Column('swolf', Integer)
    kilocalories = Column('kilocalories', Integer)

    def __repr__(self):
        return f"{self.id}"
    
    def getUpdate(edited_data):
        update_dict = {}
        if (edited_data[1] != 'None'):
            update_dict.update({Training_session.duration:edited_data[1]})
        else:
            update_dict.update({Training_session.duration:'00:00:00'})
        if (edited_data[2] != 'None'):
            update_dict.update({Training_session.swam_distance:int(edited_data[2])})
        else:
            update_dict.update({Training_session.swam_distance:0})
        if (edited_data[3] != 'None'):
            update_dict.update({Training_session.heart_rate:int(edited_data[3])})
        else:
            update_dict.update({Training_session.heart_rate:None})
        if (edited_data[4] != 'None'):
            update_dict.update({Training_session.spO2:int(edited_data[4])})
        else:
            update_dict.update({Training_session.spO2:None})
        if (edited_data[5] != 'None'):
            update_dict.update({Training_session.crawl:int(edited_data[5])})
        else:
            update_dict.update({Training_session.crawl:None})
        if (edited_data[6] != 'None'):
            update_dict.update({Training_session.backstroke:int(edited_data[6])})
        else:
            update_dict.update({Training_session.backstroke:None})
        if (edited_data[7] != 'None'):
            update_dict.update({Training_session.breaststroke:int(edited_data[7])})
        else:
            update_dict.update({Training_session.breaststroke:None})
        if (edited_data[8] != 'None'):
            update_dict.update({Training_session.butterfly:int(edited_data[8])})
        else:
            update_dict.update({Training_session.butterfly:None})
        if (edited_data[9] != 'None'):
            update_dict.update({Training_session.type_of_water:int(edited_data[9])})
        else:
            update_dict.update({Training_session.type_of_water:1})
        if (edited_data[10] != 'None'):
            update_dict.update({Training_session.swolf:int(edited_data[10])})
        else:
            update_dict.update({Training_session.swolf:None})
        if (edited_data[11] != 'None'):
            update_dict.update({Training_session.kilocalories:int(edited_data[11])})
        else:
            update_dict.update({Training_session.kilocalories:None})
        # update_dict.update({Training_session.swam_distance:int(edited_data[2])})
        # update_dict.update({Training_session.heart_rate:int(edited_data[3])})
        # update_dict.update({Training_session.spO2:int(edited_data[4])})
        # update_dict.update({Training_session.crawl:int(edited_data[5])})
        # update_dict.update({Training_session.backstroke:int(edited_data[6])})
        # update_dict.update({Training_session.breaststroke:int(edited_data[7])})
        # update_dict.update({Training_session.butterfly:int(edited_data[8])})
        # update_dict.update({Training_session.type_of_water:int(edited_data[9])})
        # update_dict.update({Training_session.swolf:int(edited_data[10])})
        # update_dict.update({Training_session.kilocalories:int(edited_data[11])})
        return update_dict

    def getData(row):
        data = []
        data.append(row.id)
        data.append(row.duration)
        data.append(row.swam_distance)
        data.append(row.heart_rate)
        data.append(row.spO2)
        data.append(row.crawl)
        data.append(row.backstroke)
        data.append(row.breaststroke)
        data.append(row.butterfly)
        data.append(row.type_of_water)
        data.append(row.swolf)
        data.append(row.kilocalories)
        return tuple(data)
    
    def getTrainingSession(data):
     
        train = Training_sessions_table.insert().values(duration = data[1],
        swam_distance = None if data[2] == 'None' else int(data[2]),
        heart_rate = None if data[3] == 'None' else int(data[3]),
        spO2 = None if data[4] == 'None' else int(data[4]),
        crawl = None if data[5] == 'None' else int(data[5]),
        backstroke = None if data[6] == 'None' else int(data[6]),
        breaststroke = None if data[7] == 'None' else int(data[7]),
        butterfly = None if data[8] == 'None' else int(data[8]),
        type_of_water = None if data[9] == 'None' else int(data[9]),
        swolf = None if data[10] == 'None' else int(data[10]),
        kilocalories = None if data[11] == 'None' else int(data[11])
        )
        
        return train

Training_sessions_table = Table('Training_sessions',metadata, 
    Column('id', Integer, primary_key=True),
    Column('duration', String),
    Column('swam_distance', Integer),
    Column('heart_rate', Integer),
    Column('spO2', Integer),
    Column('crawl', Integer),
    Column('backstroke', Integer),
    Column('breaststroke', Integer),
    Column('butterfly', Integer),
    Column('type_of_water', Integer),
    Column('swolf', Integer),
    Column('kilocalories', Integer)
    )
