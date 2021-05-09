import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication

from api.authorization_api import *
from api.swimming_pools_api import *
import qt_ui.swimming_sessions as swimming_sessions

class SwimmingSessionsApp(QtWidgets.QMainWindow, swimming_sessions.Ui_SwimmingSessionWindow):
    connection = []
    client_id = []
    all_sessions = []
    labels = (f'Номер\nсеанса','Дата', 'Время', 'Бассейн', f'Тип\nводы', f'Кол-во\nдорожек', 'Вместимость', 'Загруженность', f'Кол-во\nпроданных билетов',f'Кол-во\nльготных билетов\n(из общего числа)')

    def __init__(self,connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connection = connection
        self.client_id = client_id

        self.setAllSwimmingSessions()
        self.btnUpdate.clicked.connect(self.setAllSwimmingSessions)
    
    def setAllSwimmingSessions(self):
        table = self.tableSwimmingSession
        #настройки таблицы
        self.all_sessions = getAllSwimmingSessions(self.connection)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.all_sessions))
        table.setHorizontalHeaderLabels(self.labels)
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        row = 0
        for tup in self.all_sessions:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                table.setItem(row, col, cellinfo)
                col += 1
            row += 1
        table.resizeColumnsToContents()
        table.setSortingEnabled(True)

def openSwimmingSessionsApp(connection, cliend_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = SwimmingSessionsApp(connection, cliend_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    openSwimmingSessionsApp(connection, client_id)  # то запускаем функцию main()
        