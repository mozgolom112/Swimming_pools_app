# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\swimming_sessions.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SwimmingSessionWindow(object):
    def setupUi(self, SwimmingSessionWindow):
        SwimmingSessionWindow.setObjectName("SwimmingSessionWindow")
        SwimmingSessionWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SwimmingSessionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableSwimmingSession = QtWidgets.QTableWidget(self.centralwidget)
        self.tableSwimmingSession.setObjectName("tableSwimmingSession")
        self.tableSwimmingSession.setColumnCount(0)
        self.tableSwimmingSession.setRowCount(0)
        self.verticalLayout.addWidget(self.tableSwimmingSession)
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setObjectName("btnUpdate")
        self.verticalLayout.addWidget(self.btnUpdate)
        SwimmingSessionWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SwimmingSessionWindow)
        QtCore.QMetaObject.connectSlotsByName(SwimmingSessionWindow)

    def retranslateUi(self, SwimmingSessionWindow):
        _translate = QtCore.QCoreApplication.translate
        SwimmingSessionWindow.setWindowTitle(_translate("SwimmingSessionWindow", "Сеансы"))
        self.label.setText(_translate("SwimmingSessionWindow", "Сеансы"))
        self.btnUpdate.setText(_translate("SwimmingSessionWindow", "Обновить"))
