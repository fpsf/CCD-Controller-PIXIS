# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tg.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import os
import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from actions.actions import Actions
from actions.console import ConsoleThreadOutput
from ui.settingsWindow import UiSelf


class UiMainwindow(QtWidgets.QMainWindow):
    message = "This application is probably in prototype stage, " \
              "so it may display flaws in a regular basis.\n\n" \
              "The ideal way to use this application, that is, without experiencing crashes, " \
              "as of now, is that before doing anything, the program should be closed, and the " \
              "CCD camera should be manually turned on and off.\n\n" \
              "When returning to he program, to make a successful connection, " \
              "the user should make sure that " \
              "the camera's temperature " \
              "is equal to or next to 25ºC.\n\n" \
              "After that, the program should be restarted, and then, only the 'Connect' and 'Run' " \
              "buttons should be clicked for a successful acquisition cycle."

    def setup_ui(self):

        self.settings = UiSelf()
        self.actionsMenu = Actions()
        # self.actionsMenu.signal_console.connect(self.write_to_console)
        self.console = ConsoleThreadOutput()

        self.setObjectName("self")
        self.setFixedSize(470, 268)

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
        self.actionSettings.triggered.connect(self.open_settings)

        self.actionExit = QtWidgets.QAction(self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(dir_orientation + "Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon5)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.close)

        self.actionPicFolder = QtWidgets.QAction(self)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(dir_orientation + "Folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPicFolder.setIcon(icon6)
        self.actionPicFolder.setObjectName("actionPicFolder")
        self.actionPicFolder.triggered.connect(self.pics_folder)

        self.actionGetTemp = QtWidgets.QAction(self)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(dir_orientation + "Temp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGetTemp.setIcon(icon7)
        self.actionGetTemp.setObjectName("actionGetTemp")
        self.actionGetTemp.triggered.connect(self.show_temp)

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
        self.toolBar.addAction(self.actionGetTemp)
        self.toolBar.addSeparator()

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

        QtWidgets.QMessageBox.about(self, "CCD Controller 3.0.0 (Pixis)", self.message)

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
        '''
        self.actionPicFolder.setText(_translate("MainWindow", "PicFolder"))
        '''
        self.actionPicFolder.setToolTip(_translate("MainWindow", "Open Pictures Folder"))
        self.actionGetTemp.setToolTip(_translate("MainWindow", "Get Current Temperature"))

    def open_settings(self):
        if not self.actionsMenu.shooter.isRunning():
            self.settings.setup_ui()
        else:
            self.console.write_to_console("Unavailable During Acquisition.", 2)

    def show_temp(self):
        if self.actionsMenu.is_connected:
            if self.actionsMenu.shooter.isRunning():
                self.console.write_to_console("Unavailable during acquisition.", 2)
            else:
                self.console.write_to_console("Current Temperature: " +
                                              "{0:.2f}".format(self.actionsMenu.get_temp() / 100, 0), 0)
        else:
            self.console.write_to_console("Not Connected.", 2)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.actionsMenu.is_connected:
                if self.actionsMenu.shooter.shoot_on:
                    self.actionsMenu.stop()
                while self.actionsMenu.shooter.shoot_on:
                    continue
            # self.close()
            event.accept()
        else:
            event.ignore()

    def pics_folder(self):
        try:
            if not os.path.exists(self.actionsMenu.cs.path):
                os.makedirs(self.actionsMenu.cs.path)
            if os.name == "nt":
                os.startfile(self.actionsMenu.cs.path)
            else:
                subprocess.Popen(["xdg-open", self.actionsMenu.cs.path])
        except Exception as e:
            self.console.write_to_console("Failed to open images folder: " + str(e), 3)
        # TODO Darwin?
        """
        elif os.name == "Darwin":
            os.subprocess.Popen(["open", path])
        """
