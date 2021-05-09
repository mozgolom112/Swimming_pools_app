from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func

from api.models.swimming_pools import Swimming_pool, Pool_location, City, Type_of_water, Monetary_policy, Ticket_type
from api.models.swimming_sessions import Swimming_session
from api.models.daily_earnings import Daily_earning
from api.authorization_api import *

import datetime

def isDailyEarnAlreadyExist(connection, pool_id, date):
    Session = sessionmaker(bind=connection)
    session = Session()

    query = session.query(Daily_earning.date).filter(Daily_earning.id_pool == pool_id, Daily_earning.date == date)
    records = query.all()

    print('r')
    if (len(records)==0):
        return False
    else:
        return True

def insertDailyEarnings(connection, pool_id, date, isAlreadyExist):
    Session = sessionmaker(bind=connection)
    session = Session()
    
    if (isAlreadyExist):
        #необходимо удалить эту запись
        session.query(Daily_earning).filter(Daily_earning.id_pool == pool_id, Daily_earning.date == date).delete()
        session.commit()
    session.execute(func.public.culc_daily_earnings(pool_id, date))
    session.commit()


def getAllDailyEarnings(connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Daily_earning,  Monetary_policy)
    query = query.join(Monetary_policy, Monetary_policy.id == Daily_earning.monetary_policy)
    
    records_Daily_earning = query.all()


    data = []
    for de, mp in records_Daily_earning:
        tup = (
        de.report_uuid, 
        de.id_pool,
        de.date, 
        de.clients, 
        de.discount_clients,de.proceeds, 
        de.workload, 
        mp.id, 
        mp.ticket_price, 
        mp.ticket_price*mp.discount,
        mp.date_of_adoption)

        data.append(tup)
    
    return data

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    #isDailyEarnAlreadyExist(connection, 1, '2021-01-01')  
    insertDailyEarnings(connection, 1, '2021-01-01', True)
    #getAllDailyEarnings(connection)