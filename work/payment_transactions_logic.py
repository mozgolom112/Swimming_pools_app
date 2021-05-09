import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication

from api.authorization_api import *
from api.payment_transaction_api import *
import qt_ui.transactions as transactions

class PaymentTransactionsApp(QtWidgets.QMainWindow, transactions.Ui_PaymentTransactionsWindow):
    connection = []
    client_id = []
    all_transactions = []
    labels = (f'UUID','ID бассейна', 'ID билета', 'Время платежа', f'Время подтверждение от БД')

    def __init__(self,connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connection = connection
        self.client_id = client_id

        self.setAllPaymentTransactions()
        self.btnUpdate.clicked.connect(self.setAllPaymentTransactions)
    
    def setAllPaymentTransactions(self):
        table = self.tableTransactions
        #настройки таблицы
        self.all_transactions = getAllPaymentTransaction(self.client_id)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.all_transactions))
        table.setHorizontalHeaderLabels(self.labels)
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        row = 0
        for tup in self.all_transactions:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1
        table.resizeColumnsToContents()
        table.setSortingEnabled(False)

def openPaymentTransactionsApp(connection, cliend_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = PaymentTransactionsApp(connection, cliend_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    openPaymentTransactionsApp(connection, client_id)  # то запускаем функцию main()
        