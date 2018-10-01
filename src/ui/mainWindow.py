# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tg.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMessageBox

from actions.actions import Actions


class UiMainwindow(object):

    def setup_ui(self, main_window):

        self.actions = Actions()
        self.actions.signal_console.connect(self.write_to_console)

        main_window.setObjectName("main_window")
        main_window.resize(464, 268)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())

        main_window.setSizePolicy(size_policy)
        main_window.setWindowTitle("CCD Controller 3.0.0 (Pixis)")

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(True)

        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(11)

        self.plainTextEdit.setFont(font)
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plainTextEdit.setToolTip("")
        self.plainTextEdit.setStatusTip("")
        self.plainTextEdit.setWhatsThis("")
        self.plainTextEdit.setAccessibleName("")
        self.plainTextEdit.setAccessibleDescription("")
        # color: rgb(0, 255, 0)
        self.plainTextEdit.setStyleSheet("color: green; background-color: rgb(0, 0, 0);")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)
        main_window.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(main_window)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(48, 48))
        self.toolBar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.actionConnect = QtWidgets.QAction(main_window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/Connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.triggered.connect(self.actions.connect)

        self.actionDisconnect = QtWidgets.QAction(main_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/Disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDisconnect.setIcon(icon1)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionConnect.triggered.connect(self.actions.disconnect)

        self.actionRun = QtWidgets.QAction(main_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/Run_Manual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon2)
        self.actionRun.setObjectName("actionRun")
        self.actionConnect.triggered.connect(self.actions.shoot)

        self.actionStop = QtWidgets.QAction(main_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/Stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon3)
        self.actionStop.setObjectName("actionStop")
        self.actionConnect.triggered.connect(self.actions.stop)

        self.actionSettings = QtWidgets.QAction(main_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/Settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon4)
        self.actionSettings.setObjectName("actionSettings")

        self.actionExit = QtWidgets.QAction(main_window)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon5)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.closeEvent)

        self.actionPicFolder = QtWidgets.QAction(main_window)
        self.actionPicFolder.setObjectName("actionPicFolder")

        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addAction(self.actionDisconnect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPicFolder)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow", "PlaceholderText"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionConnect.setToolTip(_translate("MainWindow", "Connect"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionDisconnect.setToolTip(_translate("MainWindow", "Disconnect"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionRun.setToolTip(_translate("MainWindow", "Run"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionStop.setToolTip(_translate("MainWindow", "Stop"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit"))
        self.actionPicFolder.setText(_translate("MainWindow", "PicFolder"))
        self.actionPicFolder.setToolTip(_translate("MainWindow", "Open Pictures Folder"))

    def write_to_console(self, message, level):
        if level == 1:
            self.plainTextEdit.setStyleSheet("color: blue; background-color: rgb(0, 0, 0);")
        elif level == 2:
            self.plainTextEdit.setStyleSheet("color: yellow; background-color: rgb(0, 0, 0);")
        elif level == 3:
            self.plainTextEdit.setStyleSheet("color: red; background-color: rgb(0, 0, 0);")
        else:
            self.plainTextEdit.setStyleSheet("color: green; background-color: rgb(0, 0, 0);")

        self.plainTextEdit.moveCursor(QTextCursor.End)
        self.plainTextEdit.insertPlainText(message + '\n')
        self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.actions.shoot_on:
                self.actions.stop()
            while self.actions.get_temp() != 2500:
                continue
            event.accept()
        else:
            event.ignore()


# import pixis_rf_rc
