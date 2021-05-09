from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from api.models.clients import Client
from api.authorization_api import *
import json

path_to_authorization = "./work/api/key-value-database/authorization.json"

def getClientInfoById(connection, client_id):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Client).filter(Client.id == client_id)
    record = query.first()
    print(record)
    data = (record.surname, record.name, record.patronymic_name, record.phone, record.date_registration)
    return data

def updatePhoneClientById(connection, client_id, new_phone):
    Session = sessionmaker(bind=connection)
    session = Session()
    session.query(Client).filter(Client.id == client_id).update({Client.phone:new_phone}, synchronize_session = False)
    session.commit()

    return 0

def getAllClients(connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    query = session.query(Client)
    records = query.all()
    
    data = []
    for person in records:
        tup = (person.id, person.surname, person.name, person.patronymic_name, person.birth, person.date_registration, person.phone)
        data.append(tup)
    
    return data

def insertNewClient(connection, client_info):
    client_insert = Client.getClientInsert(client_info)
    index = connection.execute(client_insert) #вставили данные
    inserted_index = index.inserted_primary_key[0]

    return inserted_index

def insertNewPairLogPass(login, password, cliend_id):
    with open(path_to_authorization, 'r') as file:
        logs = json.load(file)
    logs['login'].append(
        {
        "login": login,
        "password": password,
        "id_client": cliend_id
        })
    with open(path_to_authorization, 'w') as file:
        json.dump(logs, file, indent=4)
    return 0

def deleteClient(connection, client_id):
    #удаляем из бд
    Session = sessionmaker(bind=connection)
    session = Session()
    session.query(Client).filter(Client.id == client_id).delete()
    session.commit()

    #удаляем логин и пароль
    with open(path_to_authorization, 'r') as file:
        logs = json.load(file)
    
    new_logs = [x for x in logs['login'] if int(x['id_client'])!=client_id]

    logs['login'] = new_logs
    with open(path_to_authorization, 'w') as file:
        json.dump(logs, file, indent=4)
    return 0

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    client_id = 3
    client_info = ('New', 'Era', 'rr', '10-10-2010', '10-10-2020', '+7111111111')
    #getClientInfoById(connection, client_id)
    #updatePhoneClientById(connection, client_id,"+77777772")
    #deleteClient(connection, client_id)
    #getAllClients(connection)
    #insertNewClient(connection, client_info)
    #insertNewPairLogPass('login', 'password', 55)
