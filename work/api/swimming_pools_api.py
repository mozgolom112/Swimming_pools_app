from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from api.models.swimming_pools import Swimming_pool, Pool_location, City, Type_of_water, Monetary_policy, Ticket_type
from api.models.swimming_sessions import Swimming_session
from api.authorization_api import *

from itertools import groupby
import datetime

def getAllSwimmingSessions(connection):
    Session = sessionmaker(bind=connection)
    session = Session()

    query = session.query(Swimming_session, Swimming_pool, Pool_location, City, Type_of_water)
    query = query.join(Swimming_pool, Swimming_pool.id == Swimming_session.id_pool)
    query = query.join(Pool_location, Pool_location.id == Swimming_pool.location)
    query = query.join(City, City.id == Pool_location.city)
    query = query.join(Type_of_water, Type_of_water.type == Swimming_pool.type_of_water)
    

    record = query.all()

    data = []

    for swim_s, sp, loc, city, tw in record:
        tup = (swim_s.id, swim_s.date_and_time.date(),swim_s.date_and_time.time(), f'{city.city}, {loc.address}', tw.description, sp.lines, sp.capacity, swim_s.workload,swim_s.entry_tickets, swim_s.discount_tickets)
        data.append(tup)
    data = sorted(data, key=lambda rec: rec[0])
    return data

def getAllPools(connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    # query = session.query(Swimming_pool, Pool_location)
    
    # #query = query.join(Swimming_pool, Swimming_pool.type_of_water == Type_of_water.type)

    # record = query.all()

    # for sp, loc in record:
    #     print(f'{sp.id}| {loc.address}| ')

    query = session.query(Swimming_pool, Pool_location, City, Type_of_water, Monetary_policy)
    query = query.join(Pool_location, Pool_location.id == Swimming_pool.location)
    query = query.join(City, City.id == Pool_location.city)
    query = query.join(Type_of_water, Type_of_water.type == Swimming_pool.type_of_water)
    query = query.join(Monetary_policy, Monetary_policy.id == Swimming_pool.monetary_policy)
    record = query.all()

    data = []

    for sp, loc, city, tw, mp in record:
        info_str = f'{sp.id}| {city.city}, {loc.address}| {tw.description}| Кол-во дорожек: x{sp.lines}'
        tup = (sp.id,info_str, (mp.ticket_price, mp.discount))
        data.append(tup)
        #print(f'{sp.id}| {city.city}, {loc.address}| {tw.description}| Дорожки: x{sp.lines}')
    
    return data


def getTicketTypes(connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Ticket_type)

    record = query.all()

    data = []
    for tt in record:
        tup = (tt.type, f'{tt.type}| {tt.description}')
        data.append(tup)
        #print(tt.description)
    return data

def getAvalibleSessionTime(connection, pool_id, date):
    Session = sessionmaker(bind=connection)
    session = Session()
    up_date = date + datetime.timedelta(days=1)
    query = session.query(Swimming_session).filter(Swimming_session.id_pool == pool_id ,Swimming_session.date_and_time >= str(date) , Swimming_session.date_and_time < str(up_date), Swimming_session.workload < 1)

    record = query.all()

    data = []
    for sw_s in record:
        tup = (sw_s.id, sw_s.date_and_time.time(), sw_s.workload)
        data.append(tup)
    return data

def getAvalibleSessionDates(connection, pool_id):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Swimming_session).filter(Swimming_session.id_pool == pool_id) 
    
    record = query.all()
    data = []
    for sw_s in record:
        data.append(sw_s.date_and_time.date())
    data = [el for el, _ in groupby(data)]
    return data

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    getAllSwimmingSessions(connection)
    # getAllPools(connection)  # то запускаем функцию main()
    # getTicketTypes(connection)
    # getAvalibleSessionDates(connection, 1)
    # getAvalibleSessionTime(connection, 1, datetime.date(2021,1,1))