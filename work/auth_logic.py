import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication
import qt_ui.auth as auth

from api.authorization_api import *
from menu_for_client_logic import MenuForClientApp
from menu_for_administator_logic import MenuForAdministrationApp

def showMessage(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()

class AuthApp(QtWidgets.QMainWindow, auth.Ui_AuthWindow):
    connection = []
    client_id = []

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.btnEnter.clicked.connect(self.pushBtnEnter)
        self.radioBtnShowPass.toggled.connect(self.showPass)

    def showPass(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.linePass.setEchoMode(QLineEdit.Normal)
        else:
            self.linePass.setEchoMode(QLineEdit.Password)

    def pushBtnEnter(self):
        print('enter')
        login = self.lineLogin.text()
        password = self.linePass.text()
        if (login == '' or password == ''):
            showMessage("Ошибка", "Введите логин и пароль")
        else:
            message, client_id = findUser(login, password)
            if (client_id == 0):
                showMessage("Ошибка авторизции", message)
            else:
                connection, db_session = getConnectionWithDataBase(client_id)
                self.client_id = client_id
                self.connection = connection
                if (self.client_id > 0):
                    #значит клиент
                    self.w1 = MenuForClientApp(self.connection, self.client_id)
                    self.w1.show()
                    self.hide()
                else:
                    #значит администратор
                    self.w1 = MenuForAdministrationApp(self.connection, self.client_id)
                    self.w1.show()
                    self.hide()
                
                
                



        

def openAuthWindow():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AuthApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__': 
    openAuthWindow()