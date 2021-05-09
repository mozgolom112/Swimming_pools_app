# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\training_sessions_v1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TrainingSessionsWindow(object):
    def setupUi(self, TrainingSessionsWindow):
        TrainingSessionsWindow.setObjectName("TrainingSessionsWindow")
        TrainingSessionsWindow.resize(764, 570)
        self.centralwidget = QtWidgets.QWidget(TrainingSessionsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableTrainingSessionsWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableTrainingSessionsWidget.setObjectName("tableTrainingSessionsWidget")
        self.tableTrainingSessionsWidget.setColumnCount(0)
        self.tableTrainingSessionsWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableTrainingSessionsWidget)
        self.tableRedactorWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableRedactorWidget.sizePolicy().hasHeightForWidth())
        self.tableRedactorWidget.setSizePolicy(sizePolicy)
        self.tableRedactorWidget.setMinimumSize(QtCore.QSize(0, 40))
        self.tableRedactorWidget.setObjectName("tableRedactorWidget")
        self.tableRedactorWidget.setColumnCount(0)
        self.tableRedactorWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableRedactorWidget)
        self.btnCreate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreate.setObjectName("btnCreate")
        self.verticalLayout.addWidget(self.btnCreate)
        self.btnEdit = QtWidgets.QPushButton(self.centralwidget)
        self.btnEdit.setObjectName("btnEdit")
        self.verticalLayout.addWidget(self.btnEdit)
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setObjectName("btnDelete")
        self.verticalLayout.addWidget(self.btnDelete)
        TrainingSessionsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TrainingSessionsWindow)
        QtCore.QMetaObject.connectSlotsByName(TrainingSessionsWindow)

    def retranslateUi(self, TrainingSessionsWindow):
        _translate = QtCore.QCoreApplication.translate
        TrainingSessionsWindow.setWindowTitle(_translate("TrainingSessionsWindow", "MainWindow"))
        self.label.setText(_translate("TrainingSessionsWindow", "Мои тренировки"))
        self.btnCreate.setText(_translate("TrainingSessionsWindow", "Создать"))
        self.btnEdit.setText(_translate("TrainingSessionsWindow", "Редактировать"))
        self.btnDelete.setText(_translate("TrainingSessionsWindow", "Удалить"))