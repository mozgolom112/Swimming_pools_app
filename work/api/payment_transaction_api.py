import json

path_to_payment_transactions = './work/api/key-value-database/payment_transactions.json'

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

def getAllPaymentTransaction(client_id):
    #Можно запрашивать пароль. Но для упрощения админу разрешено
    if client_id > 0:
        return []
    else:
        with open(path_to_payment_transactions, 'r') as read_file:
            tr = json.load(read_file)
        data = []

        for transact in tr['Transactions']:
            tup = (transact['uuid'], transact['ticket_info']['id_pool'], transact['ticket_info']['id_ticket'],transact['payment_info']['time_payment'],transact['payment_info']['time_append_ticket_from_db'])
            data.append(tup)
        
        return data

if __name__ == '__main__': 
    getAllPaymentTransaction(-1)
