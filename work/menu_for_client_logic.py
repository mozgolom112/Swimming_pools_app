import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication
import qt_ui.menu_for_client as menu_for_client
from person_logic import PersonApp
from training_sessions_logic import TrainingSessionsApp
from tickets_buy_logic import TicketBuyApp

class MenuForClientApp(QtWidgets.QMainWindow, menu_for_client.Ui_MenuForClientWindow):
    connection = []
    client_id = []

    def __init__(self, connection, cliend_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  
        self.connection = connection
        self.client_id = cliend_id

        self.btnGoToPerson.clicked.connect(self.goToPerson)
        self.btnGoToTickets.clicked.connect(self.goToTickets)
        self.btnGoToTraining.clicked.connect(self.goToTraining)

    def goToPerson(self):  
        self.w1 = PersonApp(self.connection, self.client_id)
        self.w1.show()
        self.showMinimized()
        
    def goToTickets(self):  
        self.w2 = TicketBuyApp(self.connection, self.client_id)
        self.w2.show()
        self.showMinimized()
        
    def goToTraining(self):  
        self.w3 = TrainingSessionsApp(self.connection, self.client_id)
        self.w3.show()
        self.showMinimized()

