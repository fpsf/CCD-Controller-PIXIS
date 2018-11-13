import sys

from PyQt5 import QtWidgets

from ui.mainWindow import UiMainwindow

try:
    app = QtWidgets.QApplication(sys.argv)
    '''
    acessa a classe mainWindow/testmain.py para criacao da interface
    '''
    ex = UiMainwindow()
    ex.setup_ui()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
