# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tg.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMessageBox

from actions.actions import Actions
from actions.console import ConsoleThreadOutput
from ui.settingsWindow import UiSelf


class UiMainwindow(QtWidgets.QMainWindow):

    def setup_ui(self):

        self.settings = UiSelf()
        self.actionsMenu = Actions()
        # self.actionsMenu.signal_console.connect(self.write_to_console)
        self.console = ConsoleThreadOutput()

        self.setObjectName("self")
        self.setFixedSize(464, 268)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)
        self.setWindowTitle("CCD Controller 3.0.0 (Pixis)")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(True)

        font = QtGui.QFont()
        if os.name == "nt":
            font.setFamily("Terminal")
            font.setPointSize(11)
        else:
            font.setFamily("Noto")
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
        self.console.set_console(self.plainTextEdit)

        self.verticalLayout.addWidget(self.plainTextEdit)
        self.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(48, 48))
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        if os.name == "nt":
            dir_orientation = os.getcwd() + "\\ui\\icons\\"
        else:
            dir_orientation = os.getcwd() + "/ui/icons/"

        self.actionConnect = QtWidgets.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(dir_orientation + "Connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.triggered.connect(self.actionsMenu.connect)

        self.actionDisconnect = QtWidgets.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(dir_orientation + "Disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDisconnect.setIcon(icon1)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionDisconnect.triggered.connect(self.actionsMenu.disconnect_cam)

        self.actionRun = QtWidgets.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(dir_orientation + "Run_Manual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon2)
        self.actionRun.setObjectName("actionRun")
        self.actionRun.triggered.connect(self.actionsMenu.shoot)

        self.actionStop = QtWidgets.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(dir_orientation + "Stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon3)
        self.actionStop.setObjectName("actionStop")
        self.actionStop.triggered.connect(self.actionsMenu.stop)

        self.actionSettings = QtWidgets.QAction(self)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(dir_orientation + "Settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon4)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.settings.setup_ui)

        self.actionExit = QtWidgets.QAction(self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(dir_orientation + "Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon5)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.closeEvent)

        self.actionPicFolder = QtWidgets.QAction(self)
        self.actionPicFolder.setObjectName("actionPicFolder")
        self.actionPicFolder.triggered.connect(self.pics_folder)

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

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def retranslate_ui(self):
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.actionsMenu.is_connected:
                if self.actionsMenu.shoot_on:
                    self.actionsMenu.stop()
                while self.actionsMenu.get_temp() != 2500:
                    continue
            self.close()

    def pics_folder(self):
            if os.name == "nt":
                os.startfile(self.actionsMenu.cs.path)
            else:
                os.subprocess.Popen(["xdg-open", self.actionsMenu.cs.path])
            # TODO Darwin?
            """
            elif os.name == "Darwin":
                os.subprocess.Popen(["open", path])
            """


# import pixis_rf.qrc
