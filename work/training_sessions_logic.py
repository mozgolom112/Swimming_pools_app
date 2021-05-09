import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication
import qt_ui.training_sessions as training_sessions

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, Integer

from api.authorization_api import *

from api.models.clients import Client
from api.models.training_sessions import Training_session, Training_sessions_table
from api.models.tickets import Ticket, Ticket_table


class TrainingSessionsApp(QtWidgets.QMainWindow, training_sessions.Ui_TrainingSessionsWindow):
    connection = []
    client_id = []
    data = []
    labels = ('Уникальный номер', f'Длительность тренировки\n(часы:минуты:секунды)','Проплытая дистанция, метры', 'Пульс, уд./cек', 'spO2', 'Кроль', 'На спине', 'Брасс', 'Баттерфляй', 'Тип воды', 'Swolf', 'Килокалории')
    empty_row=('X','00:00:00', 0, 'None', 'None', 0,0,0,0, 1,0,0)
    def __init__(self,connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.connection = connection
        self.client_id = client_id
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        
        self.updTable()
        
        tableEdit = self.tableRedactorWidget
        tableEdit.setColumnCount(len(self.labels))
        tableEdit.setRowCount(1)
        tableEdit.setHorizontalHeaderLabels(self.labels)
        tableEdit.resizeColumnsToContents()
        tableEdit.resizeRowsToContents()

        self.btnEdit.clicked.connect(self.editRow)
        self.btnDelete.clicked.connect(self.deleteRow)
        self.btnCreate.clicked.connect(self.createRow)
    
    def createRow(self):
        table = self.tableRedactorWidget
        #необходимо проверить, пустой ли у нас список. Если да, то повторное нажатие сохранит
        if (table.item(0,0)!=None):
            if (table.item(0,0).text()=='X'):
                #закидываем в бд в любую запись пользователя, если такова есть
                #Выберете нужный ваш сеанс
                print(table.item(0,0).text())
                avaliable_dates = self.getTicketWithoutTraining(self.client_id)
                if (len(avaliable_dates) == 0):
                    msg = QMessageBox()
                    msg.setWindowTitle("Ошибка выбора билета")
                    msg.setText("К сожалению, ко всем вашим билетам уже привязана статистика")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()
                else:
                    #просим пользователя выбрать нужный сеанс
                    items = [str(tuple[0])+'| '+str(tuple[1]) for tuple in avaliable_dates]
                    item, okPressed = QInputDialog.getItem(self, "Get item","Дата:", items, 0, False)
                    if okPressed and item:
                        print(item)
                        ticket_id = int(item.split('|')[0])
                    
                    insert_data = []
                    for i in range(self.tableRedactorWidget.columnCount()):
                        if (self.tableRedactorWidget.item(0, i) != None):
                            it = self.tableRedactorWidget.item(0, i).text()
                            insert_data.append(it)
                        else:
                            insert_data.append(None)
                    
                    self.insertData(ticket_id, insert_data)   
                    self.updTable()
                    self.tableRedactorWidget.removeRow(0)
                    self.tableRedactorWidget.setRowCount(1)
                    
            else:
                col = 0
                for item in self.empty_row:
                    cellinfo = QTableWidgetItem(str(item))
                    table.setItem(0, col, cellinfo)
                    if (col==0):
                        cellinfo.setFlags(QtCore.Qt.ItemIsEnabled)
                    col += 1
        #иначе создаем шаблон
        else:
            col = 0
            for item in self.empty_row:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(0, col, cellinfo)
                if (col==0):
                    cellinfo.setFlags(QtCore.Qt.ItemIsEnabled)
                col += 1
    def insertData(self, ticket_id, train):
        connection = self.connection
        Session = sessionmaker(bind=connection)
        session = Session()
        training_insert = Training_session.getTrainingSession(train)
        index = connection.execute(training_insert) #вставили данные
        inserted_index = index.inserted_primary_key[0]
        #необходимо привязать к тикету
        session.query(Ticket).filter(Ticket.id == ticket_id).update({Ticket.id_training:inserted_index}, synchronize_session = False)
        session.commit()
        print(inserted_index)

    def deleteData(self, delete_train_id):
        connection = self.connection
        Session = sessionmaker(bind=connection)
        session = Session()
        session.query(Ticket).filter(Ticket.id_training == delete_train_id).update({Ticket.id_training : None}, synchronize_session = False)
        session.query(Training_session).filter(Training_session.id == delete_train_id).delete()
        session.commit()
        self.updTable()
        self.tableRedactorWidget.removeRow(0)
        self.tableRedactorWidget.setRowCount(1)

    def deleteRow(self):
        if (self.tableRedactorWidget.item(0, 0) != None):
            if (self.tableRedactorWidget.item(0, 0).text() != 'x'):
                delete_id = int(self.tableRedactorWidget.item(0, 0).text())
                self.deleteData(delete_id)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка Удаления")
            msg.setText("Выберете строку, которую хотите удалить")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def updTable(self):
        table = self.tableTrainingSessionsWidget
        #настройки таблицы
        self.data =self.getAllTrainingSessions()
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.data))
        table.setHorizontalHeaderLabels(self.labels)
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Устанавливаем событие на выбор item
        table.itemSelectionChanged.connect(self.setCurrentItem)
        #устанавливаем значения
        row = 0
        for tup in self.data:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1

    def getTicketWithoutTraining(self, cliend_id):
        client_id = self.client_id
        connection = self.connection
        Session = sessionmaker(bind=connection)
        session = Session()

        no_training_session = session.query(Ticket.id, Ticket.id_training, Ticket.date_and_time).filter(Ticket.id_client==client_id).all()
        no_training_session = [(i[0], i[2]) for i in no_training_session if type(i[1])== type(None)]
        print(no_training_session)

        return no_training_session

    def getAllTrainingSessions(self):
        client_id = [self.client_id]
        connection = self.connection
        Session = sessionmaker(bind=connection)
        session = Session()

        training_session = session.query(Ticket.id_training).filter(Ticket.id_client.in_(client_id)).all()
        training_session = [i[0] for i in training_session if type(i[0])!= type(None)]


        sessions = session.query(Training_session).filter(Training_session.id.in_(training_session))
        data = []
        for row in sessions:
            tup = Training_session.getData(row)
            data.append(tup)
        
        return data

    def updateData(self, edited_data):
        print(edited_data)
        Training_session_id = int(edited_data[0])
        updateDict = Training_session.getUpdate(edited_data)
        connection = self.connection
        Session = sessionmaker(bind=connection)
        session = Session()

        session.query(Training_session).filter(Training_session.id == Training_session_id).update(updateDict, synchronize_session = False)
        session.commit()
        self.updTable()
  
    def editRow(self):
        edited_data = []
        if (self.tableRedactorWidget.item(0, 0) != None):
            if (self.tableRedactorWidget.item(0, 0).text() != 'x'):
                for i in range(self.tableTrainingSessionsWidget.columnCount()):
                    if (self.tableRedactorWidget.item(0, i) != None):
                        it = self.tableRedactorWidget.item(0, i).text()
                        edited_data.append(it)
                    else:
                        edited_data.append(None)
                self.updateData(edited_data)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка редактирования")
            msg.setText("Выберете строку для редактирования")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def setCurrentItem(self):
        item = self.tableTrainingSessionsWidget.currentItem()
        choosedRow = item.row()
        for i in range(self.tableTrainingSessionsWidget.columnCount()):
            it = self.tableTrainingSessionsWidget.item(choosedRow, i).clone()
            if (i==0):
                it.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableRedactorWidget.setItem(0, i, it)
        
def openTrainingSessionWindow(connection, cliend_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

    window = TrainingSessionsApp(connection, cliend_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    client_id = 1
    openTrainingSessionWindow(connection, client_id)  # то запускаем функцию main()