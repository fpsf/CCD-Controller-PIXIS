# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'tg_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtGui

from saving.camera_settings import CameraSettings
from saving.default_settings import DefaultSettings


class UiSelf(QtWidgets.QWidget):

    def setup_ui(self):
        self.setObjectName("self")
        self.resize(287, 223)

        self.default = DefaultSettings
        self.cs = CameraSettings()
        self.cs.load_settings()
        self.path = ""

        # Gain:

        self.selfLayoutWidget = QtWidgets.QWidget(self)
        self.selfLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 221))
        self.selfLayoutWidget.setObjectName("selfLayoutWidget")
        self.selfLayout = QtWidgets.QselfLayout(self.selfLayoutWidget)
        self.selfLayout.setContentsMargins(0, 0, 0, 0)
        self.selfLayout.setObjectName("selfLayout")
        self.label = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label.setObjectName("label")
        self.selfLayout.setWidget(0, QtWidgets.QselfLayout.LabelRole, self.label)

        self.comboBox = QtWidgets.QComboBox(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")

        # TODO ?(x2, x4, x8)?
        self.comboBox.addItems([self.tr("1"), self.tr("2"), self.tr("3")])
        self.comboBox.setCurrentIndex(self.cs.gain)

        # Gain
        '''
        Gain/Temperature
        '''
        # Temperature:

        self.selfLayout.setWidget(0, QtWidgets.QselfLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.selfLayout.setWidget(1, QtWidgets.QselfLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setValidator(QtGui.QIntValidator(-70, 25))
        self.lineEdit.setText(self.cs.temp)

        # Temperature
        '''
        Temperature/Shooting Time
        '''
        # Shooting Time:

        self.selfLayout.setWidget(1, QtWidgets.QselfLayout.FieldRole, self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.selfLayout.setWidget(2, QtWidgets.QselfLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setValidator(QtGui.QIntValidator(60, 600))
        self.lineEdit_2.setText(self.cs.time_shooting)

        # Shooting Time
        '''
        Shooting Time/Time Between Images 
        '''
        # Time Between Images:

        self.selfLayout.setWidget(2, QtWidgets.QselfLayout.FieldRole, self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.selfLayout.setWidget(3, QtWidgets.QselfLayout.LabelRole, self.label_4)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setValidator(QtGui.QIntValidator(5, 60))
        self.lineEdit_3.setText(self.cs.acq_wait)

        # Time Between Images
        '''
        Time Between Images/Binning 
        '''
        # Binning:

        self.selfLayout.setWidget(3, QtWidgets.QselfLayout.FieldRole, self.lineEdit_3)
        self.label_5 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.selfLayout.setWidget(4, QtWidgets.QselfLayout.LabelRole, self.label_5)

        self.comboBox_2 = QtWidgets.QComboBox(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setMinimumContentsLength(0)
        self.comboBox_2.setObjectName("comboBox_2")

        self.comboBox_2.addItems([self.tr("1x1"), self.tr("2x2"), self.tr("3x3")])
        self.comboBox_2.setCurrentIndex(self.cs.binning)

        # Binning
        '''
        Binning/Exposure Time
        '''
        # Exposure Time:

        self.selfLayout.setWidget(4, QtWidgets.QselfLayout.FieldRole, self.comboBox_2)
        self.label_6 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.selfLayout.setWidget(5, QtWidgets.QselfLayout.LabelRole, self.label_6)

        self.lineEdit_4 = QtWidgets.QLineEdit(self.selfLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setValidator(QtGui.QIntValidator(5, 60))
        self.lineEdit_4.setText(self.cs.exp)

        # Exposure Time
        '''
        Exposure Time/Images Path
        '''
        # Images Path:

        self.selfLayout.setWidget(5, QtWidgets.QselfLayout.FieldRole, self.lineEdit_4)
        self.label_7 = QtWidgets.QLabel(self.selfLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.selfLayout.setWidget(6, QtWidgets.QselfLayout.LabelRole, self.label_7)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.selfLayoutWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setText(self.cs.path)
        self.lineEdit_5.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEdit_5)

        self.toolButton = QtWidgets.QToolButton(self.selfLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.toolButton.triggered.connect(self.get_dir)

        self.selfLayout.setLayout(6, QtWidgets.QselfLayout.FieldRole, self.horizontalLayout)

        # Images Path
        '''
        Images Path/Buttons
        '''
        # Buttons:

        self.buttonBox = QtWidgets.QDialogButtonBox(self.selfLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.RestoreDefaults | QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.selfLayout.setWidget(7, QtWidgets.QselfLayout.SpanningRole, self.buttonBox)
        self.buttonBox.clicked(QAbstractButton=QtWidgets.QDialogButtonBox.Save).connect(self.save_settings)
        self.buttonBox.clicked(QAbstractButton=QtWidgets.QDialogButtonBox.RestoreDefaults).connect(self.defaults)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.show()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Settings"))
        self.label.setText(_translate("self", "Gain:"))
        self.label_2.setText(_translate("self", "Temperature (ºC):"))
        self.label_3.setText(_translate("self", "Shooting Time (s):"))
        self.label_4.setText(_translate("self", "Time Between Images (s):"))
        self.label_5.setText(_translate("self", "Binning:"))
        self.label_6.setText(_translate("self", "Exposure Time:"))
        self.label_7.setText(_translate("self", "Images Path"))
        self.toolButton.setText(_translate("self", "..."))

    def get_dir(self):
        imgs_dir = QtWidgets.QFileDialog()
        self.lineEdit_5.setText(str(imgs_dir))
        self.path = imgs_dir

    def save_settings(self):
        self.cs.gain = self.comboBox.currentIndex()
        self.cs.temp = int(self.lineEdit.text())
        self.cs.time_shooting = int(self.lineEdit_2.text())
        self.cs.acq_wait = int(self.lineEdit_3.text())
        self.cs.binning = self.comboBox_2.currentIndex()
        self.cs.exp = int(self.lineEdit_4.text())
        self.cs.path = self.lineEdit_5.text()
        self.cs.save_settings()
