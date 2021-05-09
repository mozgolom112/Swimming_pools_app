import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QWidget, QPushButton, QLineEdit, QInputDialog, QApplication
import qt_ui.menu_for_administraion as menu_for_administraion
from all_client_logic import AllClientApp
from daily_earnings_logic import DailyEarningsApp
from payment_transactions_logic import PaymentTransactionsApp
from swimming_sessions_logic import SwimmingSessionsApp

class MenuForAdministrationApp(QtWidgets.QMainWindow, menu_for_administraion.Ui_MenuForAdministatorWindow):
    connection = []
    client_id = []

    def __init__(self, connection, cliend_id):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  
        self.connection = connection
        self.client_id = cliend_id

        self.btnClients.clicked.connect(self.goToAllClientApp)
        self.btnDailyEarnings.clicked.connect(self.goToDailyEarningsApp)
        self.btnPaymentTransactions.clicked.connect(self.goToPaymentTransactionsApp)
        self.btnSwimmingSessions.clicked.connect(self.goToSwimmingSessionsApp)

    def goToAllClientApp(self):  
        self.w1 = AllClientApp(self.connection, self.client_id)
        self.w1.show()
        self.showMinimized()
        
    def goToDailyEarningsApp(self):  
        self.w2 = DailyEarningsApp(self.connection, self.client_id)
        self.w2.show()
        self.showMinimized()
        
    def goToPaymentTransactionsApp(self):  
        self.w3 = PaymentTransactionsApp(self.connection, self.client_id)
        self.w3.show()
        self.showMinimized()
    
    def goToSwimmingSessionsApp(self):  
        self.w4 = SwimmingSessionsApp(self.connection, self.client_id)
        self.w4.show()
        self.showMinimized()

