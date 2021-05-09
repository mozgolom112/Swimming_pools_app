import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication
import qt_ui.person as person

from api.authorization_api import *
from api.clients_api import *
class PersonApp(QtWidgets.QMainWindow, person.Ui_PersonWindow):
    connection = []
    client_id = []
    client_info = []
    def __init__(self,connection, client_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self) 
        self.connection = connection
        self.client_id = client_id   
        self.client_info = getClientInfoById(self.connection, self.client_id) 
        self.labelSurname.setText(self.client_info[0])
        self.labelName.setText(self.client_info[1])
        self.labelPatronymic.setText(self.client_info[2])
        self.linePhoneEdit.setText(self.client_info[3])
        self.label_4.setText(f'Дата регистрации: {str(self.client_info[4])}')
        
        self.btnEditPhone.clicked.connect(self.btnEditPhoneClick)
        self.btnDeleteClient.clicked.connect(self.btnDeleteAccount)


    def btnDeleteAccount(self):
        msg_box = QMessageBox()
        msg_box.setText('Вы точно уверенны что хотите удалить свой аккаунт?')
        msg_box.setWindowTitle("Удаление аккаунта")
        msg_box.setInformativeText(f"Если вы удалите аккаунт, то пропадет вся ваша информация!")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        buttonReply = msg_box.exec_()

        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            deleteClient(self.connection, self.client_id)
            msg = QMessageBox()
            msg.setWindowTitle("Спасибо!")
            msg.setText("Ждем вас снова)")
            msg.exec_()
            self.close()
        else:
            print('No clicked.')

    def btnEditPhoneClick(self):
        
        if len(self.linePhoneEdit.text())!=12 or self.linePhoneEdit.text()[:2]!='+7':
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка редактирования")
            msg.setText("Номер телефона должен быть формата +7XXXXXXXXXX")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText('Вы уверены, что хотите поменять текущий номер на новый?')
            msg_box.setWindowTitle("Изменение номера")
            msg_box.setInformativeText(f"{self.client_info[3]} --> {self.linePhoneEdit.text()}")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            buttonReply = msg_box.exec_()

            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
                updatePhoneClientById(self.connection, self.client_id, self.linePhoneEdit.text())
                
            else:
                print('No clicked.')
                self.linePhoneEdit.setText(self.client_info[3])


def openPersonWindow(connection, client_id):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = PersonApp(connection, client_id)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__': 
    login = "admin"#"ngolovanov"#input("Введите логин: ")
    password = "admin"#input("Введите пароль: ")
    message, client_id = findUser(login, password)
           
    connection, db_session = getConnectionWithDataBase(client_id)
    client_id = 6
    openPersonWindow(connection, client_id)