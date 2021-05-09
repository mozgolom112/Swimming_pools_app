import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QCalendarWidget
import qt_ui.daily_earnings as daily_earnings
import datetime

from api.swimming_pools_api import *
from api.authorization_api import *
from api.tickets_api import *
from api.daily_earnings_api import *

class DailyEarningsApp(QtWidgets.QMainWindow, daily_earnings.Ui_DailyEarningsWindow):
    connection = []
    client_id = []
    pools_info = []
    avalible_date = []

    choosen_pool = []
    choosen_date = None

    daily_earnings_info = []

    labels = ("UUID", f"ID\nбассейна","Дата отчета", f"Кол-во\nпроданных билетов",f"Кол-во\nльготных клиетов\n(из общего кол-ва)", "Выручка", "Загруженность",f"ID\nплатежной политики","Полная цена билета","Льготная цена билета", f"Дата принятия\nплатежной политики")
    def __init__(self, connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.client_id = client_id
        self.connection = connection

        self.pools_info = getAllPools(self.connection) 
        self.fullfillPools()
        self.btnUpdateAdd.clicked.connect(self.UpdateOrAddDailyEarnings)
        self.setDailyEarningsinfo()

    def setDailyEarningsinfo(self):
        table = self.tableWidgetDailyEarnigs

        self.daily_earnings_info = getAllDailyEarnings(self.connection)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.daily_earnings_info))
        table.setHorizontalHeaderLabels(self.labels)
        
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #устанавливаем значения
        row = 0
        for tup in self.daily_earnings_info:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1
        table.resizeColumnsToContents()
        table.setSortingEnabled(True)


    def fullfillPools(self):
        box = self.comboBoxBath
        for item in self.pools_info:
            box.addItem(item[1])
        self.choosen_pool = self.pools_info[0][0]
        box.activated[str].connect(self.boxPoolChoosed)   

        self.setAvalibleDate()
        self.choosen_date = None
        self.btnUpdateAdd.setEnabled(False)
    
    def boxPoolChoosed(self):
        box = self.comboBoxBath
        currentChoose = int(box.currentText().split('|')[0])
        print(currentChoose)
        if (currentChoose != self.choosen_pool):
            self.choosen_pool = currentChoose
            
            for i in self.pools_info:
                if (i[0] == currentChoose):
                    break
        
            self.setAvalibleDate()
            self.choosen_date = None
            self.btnUpdateAdd.setEnabled(False)
    
    #устанавливаем календарь
    def setAvalibleDate(self):
        self.avalible_date = getAvalibleSessionDates(self.connection, self.choosen_pool)
        calendary = self.calendarWidget
        calendary.clicked.connect(self.chooseDate)
        if (len(self.avalible_date)==0):
            calendary.setSelectionMode(QCalendarWidget.SelectionMode.NoSelection)
            self.choosen_date = None
            self.avalible_date = None
            self.btnUpdateAdd.setEnabled(False)
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка выбора даты")
            msg.setText("К сожалению, в выбранный бассейн нет доступных дат, так как нет не одного сеанса в какую либо дату.")
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

    def chooseDate(self):
        calendary = self.calendarWidget
        choose_date = calendary.selectedDate().toPyDate()
        self.choosen_date = choose_date
        self.btnUpdateAdd.setEnabled(True)

    def UpdateOrAddDailyEarnings(self):
        print( self.choosen_date, self.choosen_pool)
        isExist = isDailyEarnAlreadyExist(connection, self.choosen_pool, str(self.choosen_date))
        if (isExist):
            msg_box = QMessageBox()
            msg_box.setText(f'Для этого дня уже сформирован отчет. Вы точно уверенны что хотите обновить отчет?')
            msg_box.setWindowTitle("Обновление отчета")
            msg_box.setInformativeText(f"При обновлении отчета, старый удаляется и формируется новый отчет")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            buttonReply = msg_box.exec_()
            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
                insertDailyEarnings(connection, self.choosen_pool, str(self.choosen_date), isExist)
                msg = QMessageBox()
                msg.setWindowTitle("Обновление отчета")
                msg.setText(f"Обновление отчета для бассейна с id ({self.choosen_pool}) на дату {str(self.choosen_date)}\nвыполненно успешно!")
                msg.exec_()
                self.setDailyEarningsinfo()
            else:
                print('No clicked.')
        else:
            insertDailyEarnings(connection, self.choosen_pool, str(self.choosen_date), isExist)
            msg = QMessageBox()
            msg.setWindowTitle("Создание отчета")
            msg.setText(f"Создание отчета для бассейна с id ({self.choosen_pool}) на дату {str(self.choosen_date)}\nвыполненно успешно!")
            msg.exec_()
            self.setDailyEarningsinfo()

def openDailyEarningsApp(connection, client_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = DailyEarningsApp(connection, client_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__': 
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
    
    connection, db_session = getConnectionWithDataBase(client_id)
    client_id = -1
    openDailyEarningsApp(connection, client_id)