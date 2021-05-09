import json

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from api.models.clients import Client
path_to_authorization = "./work/api/key-value-database/authorization.json" 

def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    engine = create_engine(url, client_encoding='utf8')
    db_session = scoped_session(sessionmaker(bind=engine))
    
    return engine, db_session

def getConnectionWithDataBase(client_id):
    with open(path_to_authorization, "r") as read_file:
        logs = json.load(read_file)
    if (client_id > 0):
        #логиним как обчного пользователя
        user = 'admin'#"user"
        password = logs["db_login"][user]
       
    elif (client_id == -1):
        #логиним как админа
        user = "admin"
        password = logs["db_login"][user]
    
    connection, db_session = connect(user, password, 'swimming_pools_db') 
    return connection, db_session

#взаимодействие с key-value бд
def findUser(login, password):
    
    with open(path_to_authorization, "r") as read_file:
        logs = json.load(read_file)
    
    message = ""
    client_id = 0
    for log in logs["login"]:
        if (login == log["login"] and password == log["password"]):
            client_id = log["id_client"]
            message = "200. Авторизация успешна"
            return message, int(client_id)
        elif (login == log["login"] and password != log["password"]):
            message = "401. Неверный пароль"
            return message, client_id

    message = "401. Нет такого пользователя"  
    return message, int(client_id)

def main():
    #Введите логин пароль
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)

    if client_id == 0:
        print(message)
    if client_id > 0:
        print(f"Клиент с id: {client_id}")
    if client_id == -1:
        print(f'Приветствую тебя, Админ!')
    
    connection, db_session = getConnectionWithDataBase(client_id)
    Session = sessionmaker(bind=connection)
    session = Session()

if __name__ == "__main__":
    main()