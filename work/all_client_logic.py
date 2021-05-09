import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication

from api.authorization_api import *
from api.clients_api import *
import qt_ui.allclients as allclients

class AllClientApp(QtWidgets.QMainWindow, allclients.Ui_AllClientsWindow):
    connection = []
    client_id = []

    all_clients = []

    labels = ('Уникальный номер', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Дата регистрации', 'Номер')
    empty_row=('X','Иванов', 'Иван', 'Иванович', '2020-01-20', '2020-01-20','+79991112233')

    def __init__(self,connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connection = connection
        self.client_id = client_id
        
        self.setAllClientTable()

        table1 = self.tableDeleteOrCreate
        table1.setColumnCount(len(self.labels))
        table1.setHorizontalHeaderLabels(self.labels)
        table1.setRowCount(1)

        self.btnCreate.clicked.connect(self.createRow)
        self.btnDelete.clicked.connect(self.deleteAccount)

    def deleteAccount(self):
        if (self.tableDeleteOrCreate.item(0, 0) != None):
            if (self.tableDeleteOrCreate.item(0, 0).text() != 'X'):
                delete_id = int(self.tableDeleteOrCreate.item(0, 0).text())
                msg_box = QMessageBox()
                msg_box.setText(f'Вы точно уверенны что хотите удалить аккаунт {delete_id}?')
                msg_box.setWindowTitle("Удаление аккаунта")
                msg_box.setInformativeText(f"Если вы удалите аккаунт, то пропадет вся информация пользователя!")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                buttonReply = msg_box.exec_()

                if buttonReply == QMessageBox.Yes:
                    print('Yes clicked.')
                    deleteClient(self.connection, delete_id)
                    msg = QMessageBox()
                    msg.setWindowTitle("Удаление завершено")
                    msg.setText("Не забудьте уведомить пользователя!")
                    msg.exec_()
                    self.setAllClientTable()
                else:
                    print('No clicked.')
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка Удаления")
                msg.setText("Вы не можете удалить недобавленного клиента")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка Удаления")
            msg.setText("Выберете строку, которую хотите удалить")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        

        
    
    def setAllClientTable(self):
        table = self.tableAllClients
        #настройки таблицы
        self.all_clients = getAllClients(self.connection)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.all_clients))
        table.setHorizontalHeaderLabels(self.labels)
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Устанавливаем событие на выбор item
        table.itemSelectionChanged.connect(self.setCurrentItem)
        #устанавливаем значения
        row = 0
        for tup in self.all_clients:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1
        table.resizeColumnsToContents()

    def createRow(self):
        table = self.tableDeleteOrCreate
        #необходимо проверить, пустой ли у нас список. Если да, то повторное нажатие сохранит
        if (table.item(0,0)!=None):
            if (table.item(0,0).text()=='X'):
                print(table.item(0,0).text())
                insert_data = []
                for i in range(1,table.columnCount()):
                    if (table.item(0, i) != None):
                        it = table.item(0, i).text()
                        insert_data.append(it)
                    else:
                        insert_data.append(None)
                    
                index = insertNewClient(self.connection,insert_data)
                login = ''
                while login == '':
                    login, okPressed = QInputDialog.getText(self, "Установка входных данных","Логин:", QLineEdit.Normal, "")
                    if okPressed and login != '':
                        login = login
                #ставим временный пароль
                password = ''
                while password == '':
                    password, okPressed = QInputDialog.getText(self, "Установка входных данных","Пароль:", QLineEdit.Normal, "")
                    if okPressed and password != '':
                        password = password
                insertNewPairLogPass(login, password, index)
                self.setAllClientTable()
                table.removeRow(0)
                table.setRowCount(1)       
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

    def setCurrentItem(self):
        item = self.tableAllClients.currentItem()
        table = self.tableDeleteOrCreate

        table.setColumnCount(len(self.labels))
        table.setHorizontalHeaderLabels(self.labels)
        table.setRowCount(1)

        choosedRow = item.row()
        for i in range(table.columnCount()):
            it = self.tableAllClients.item(choosedRow, i).clone()
            it.setFlags(QtCore.Qt.ItemIsEnabled)
            table.setItem(0, i, it)
        table.resizeColumnsToContents()

def openAllClientApp(connection, cliend_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AllClientApp(connection, cliend_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    openAllClientApp(connection, client_id)  # то запускаем функцию main()