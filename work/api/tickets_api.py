from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from api.models.swimming_pools import Swimming_pool, Pool_location, Type_of_water
from api.models.tickets import Ticket
from api.authorization_api import *
import uuid
import datetime
import json
import copy
template = {
    'uuid':0,
    'ticket_info': {
        'id_client': 0,
        'id_pool': 1,
        'date': 0,
        'time': 0,
        'id_ticket': -1
    },
    'payment_info':{
        'card':0,
        'time_payment': 0,
        'time_append_ticket_from_db': 0
    }
}

path_to_payment_transactions = './work/api/key-value-database/payment_transactions.json'

def paymentTransact(connection, id_pool, date, time, ticket_type, id_client=None):
    
    #Сохранем в key-value бд

    with open(path_to_payment_transactions, 'r') as read_file:
        tr = json.load(read_file)
    
    #new_id_transact = len(tr["Transactions"])+1
    new_uuid = str(uuid.uuid1())
    temp = copy.deepcopy(template)
    temp['uuid'] = new_uuid
    temp['ticket_info']['id_client'] = id_client
    temp['ticket_info']['id_pool'] = id_pool
    temp['ticket_info']['date'] = date
    temp['ticket_info'][ 'time'] = time
    temp['payment_info']['time_payment'] = str(datetime.datetime.now())

    #Сохраняем, считая что транзакия прошла успешно
    tr["Transactions"].append(temp)
    with open(path_to_payment_transactions, 'w') as file:
        json.dump(tr, file, indent=4)

    #отправляем запрос в бд
    Session = sessionmaker(bind=connection)
    session = Session()
    choosen_date = date +' '+ time
    ticket_info = [id_client, id_pool, ticket_type,choosen_date]

    ticket_insert = Ticket.getTicketInsert(ticket_info)
    index = connection.execute(ticket_insert) #вставили данные
    inserted_index = index.inserted_primary_key[0]

    #для демонстрации
    #Записываем id тикета и сохраняем время ответа от бд
    for transact in tr["Transactions"]:
        if (transact['uuid'] == new_uuid):
            print(transact['uuid'])
            transact['ticket_info']['id_ticket'] = inserted_index
            transact['payment_info']['time_append_ticket_from_db'] = str(datetime.datetime.now())
            break

    with open(path_to_payment_transactions, 'w') as file:
        json.dump(tr, file, indent=4)
    return new_uuid, inserted_index

def getAllClientTickets(connection, client_id):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Ticket, Swimming_pool, Pool_location, Type_of_water).filter(Ticket.id_client == client_id)
    query = query.join(Swimming_pool, Swimming_pool.id == Ticket.id_pool)
    query = query.join(Pool_location, Pool_location.id == Swimming_pool.location)
    query = query.join(Type_of_water, Type_of_water.type == Swimming_pool.type_of_water)
    record = query.all()

    data = []
    for ticket, sw_pool, location, tw in record:
        tup = (ticket.id, location.address, tw.description, ticket.date_and_time.date(),ticket.date_and_time.time(), ticket.id_training)
        data.append(tup)
    
    return data



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    date = str(datetime.date(2021,1,1))
    time =  str(datetime.time(11,0))
    getAllClientTickets(connection, 1)
    #paymentTransact(connection, 1,date , time, 1, 1)  # то запускаем функцию main()
