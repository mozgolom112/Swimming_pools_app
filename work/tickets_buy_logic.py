import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QCalendarWidget
import qt_ui.tickets as tickets
import datetime

from api.swimming_pools_api import *
from api.authorization_api import *
from api.tickets_api import *

class TicketBuyApp(QtWidgets.QMainWindow, tickets.Ui_TicketWindow):
    connection = []
    client_id = []
    pools_info = []
    price_policy_info = []
    avalible_date = []
    avalible_time = []

    choosen_pool = []
    current_price_policy = []
    choosen_money_policy = None
    choosen_date = None
    choosen_time = None

    final_session = None
    myTicket = []
    labels = ("ID Билета", "Бассейн", "Тип бассейна", "Дата сеанса", "Время сеанса","ID тренировки")
    def __init__(self, connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.client_id = client_id
        self.connection = connection
        self.btnBuyTicket.setEnabled(True)
        self.pools_info = getAllPools(self.connection) 
        self.price_policy_info = getTicketTypes(self.connection)
        self.fullfillPools()
        self.fullfillPricePolicy()
        
        self.setAvalibleDate()
        self.boxTicketTypeChoosed()
        
        self.btnBuyTicket.clicked.connect(self.buyTicket)
        self.setMyTicketTable()

    def setMyTicketTable(self):
        table = self.tableWidgetMyTickets

        self.myTicket = getAllClientTickets(self.connection, self.client_id)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.myTicket))
        table.setHorizontalHeaderLabels(self.labels)
        
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #устанавливаем значения
        row = 0
        for tup in self.myTicket:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1
        table.resizeColumnsToContents()
        table.setSortingEnabled(True)


    def buyTicket(self):
        if (self.final_session != None):
            nessassry_info = (self.client_id, self.choosen_pool, self.choosen_money_policy, str(self.choosen_date), self.choosen_time)
            print(nessassry_info)
            uuid_ticket, id_ticket = paymentTransact(self.connection, self.choosen_pool, str(self.choosen_date), str(self.choosen_time), self.choosen_money_policy, self.client_id)
            if (id_ticket != 0):
                msg = QMessageBox()
                msg.setWindowTitle("Оплата успешна!")
                msg.setText(f"\tСпасибо за покупку! \nВаш сеанс {str(self.choosen_date)} в {str(self.choosen_time)} \nНомер вашего билета: {id_ticket} \nНомер вашей транзакции {uuid_ticket}")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.setMyTicketTable()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Оплата не успешна!")
                msg.setText(f"К сожалению оплата не прошл. Обратитесь в кассу.")
                msg.setIcon(QMessageBox.warning)
                msg.exec_()
                


    def fullfillPricePolicy(self):
        box = self.comboBoxPricePolicy
        for item in self.price_policy_info:
            box.addItem(item[1])
        self.choosen_money_policy = self.price_policy_info[0][0]
        box.activated[str].connect(self.boxTicketTypeChoosed) 

    def fullfillPools(self):
        box = self.comboBoxBath
        for item in self.pools_info:
            box.addItem(item[1])
        self.choosen_pool = self.pools_info[0][0]
        self.current_price_policy = self.pools_info[0][2]
        box.activated[str].connect(self.boxPoolChoosed)   
    
    def boxTimeChoosed(self):
        box = self.comboBoxAvalibleSessions
        currentChoose = box.currentText()

        for i in self.avalible_time:
            if (str(i[1]) == currentChoose):
                self.choosen_time = currentChoose
                self.final_session = i[0]
                self.btnBuyTicket.setEnabled(True)
                if (i[2] < 0.4):
                    self.labelWorkload.setText(f'Низкая')
                elif (i[2] > 0.4 and i[2] < 0.7):
                    self.labelWorkload.setText(f'Средняя')
                else:
                    self.labelWorkload.setText(f'Высокая') 
                 
        print(currentChoose)

    def fullfillsessionTime(self):
        box = self.comboBoxAvalibleSessions
        box.clear()
        for item in self.avalible_time:
            box.addItem(str(item[1]))
        self.choosen_time = self.avalible_time[0][0]
        box.activated[str].connect(self.boxTimeChoosed) 

    def chooseDate(self):
        calendary = self.calendarWidget
        choose_date = calendary.selectedDate().toPyDate()
        self.choosen_date = choose_date
        self.final_session = None
        self.btnBuyTicket.setEnabled(False)
        self.avalible_time = getAvalibleSessionTime(self.connection, self.choosen_pool, choose_date)
        self.avalible_time = sorted(self.avalible_time)
        self.fullfillsessionTime()
        
        

    #устанавливаем календарь
    def setAvalibleDate(self):
        self.avalible_date = getAvalibleSessionDates(self.connection, self.choosen_pool)
        calendary = self.calendarWidget
        calendary.clicked.connect(self.chooseDate)
        if (len(self.avalible_date)==0):
            calendary.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)
            self.choosen_date = None
            self.avalible_date = None
            self.avalible_time = None
            self.comboBoxAvalibleSessions.clear()
            self.btnBuyTicket.setEnabled(False)
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка выбора даты")
            msg.setText("К сожалению, в выбранный бассейн нет доступных дат для записи")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            calendary.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
            l_date = min(self.avalible_date)
            h_date = max(self.avalible_date)
            calendary.setDateRange(l_date, h_date)
            calendary.setSelectedDate(l_date)
            self.choosen_date = l_date
            self.chooseDate()
            print('r')

    def boxPoolChoosed(self):
        box = self.comboBoxBath
        currentChoose = int(box.currentText().split('|')[0])
        print(currentChoose)
        if (currentChoose != self.choosen_pool):
            self.choosen_pool = currentChoose
            
            for i in self.pools_info:
                if (i[0] == currentChoose):
                    self.current_price_policy = i[2]
                    break

            self.setAvalibleDate()
            self.choosen_date = None
            self.choosen_time = None
            self.final_session = None
            self.btnBuyTicket.setEnabled(False)
        self.boxTicketTypeChoosed()
            

    def boxTicketTypeChoosed(self):
        box = self.comboBoxPricePolicy
        currentChoose = int(box.currentText().split('|')[0])
        print(currentChoose)
        
        if (currentChoose == 1):
            #полная стоимость
            self.labelPrice.setText(f'{self.current_price_policy[0]} р.')
        else:
            self.labelPrice.setText(f'{self.current_price_policy[0]*self.current_price_policy[1]} р.')
        
        
        
        

def openTicketWindow(connection, client_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = TicketBuyApp(connection, client_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__': 
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
    
    connection, db_session = getConnectionWithDataBase(client_id)
    client_id = 6
    openTicketWindow(connection, client_id)