from PyQt5.QtGui import QTextCursor

from actions.singleton import Singleton


class ConsoleThreadOutput(metaclass=Singleton):

    # self.log.newLine(text, level)
    def set_console(self, widget):
        self.log = widget

    def write_to_console(self, message, level):
        if level == 1:
            self.log.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(0, 255, 0);")
        elif level == 2:
            self.log.setStyleSheet("background-color: rgb(0, 0, 0); color: yellow;")
        elif level == 3:
            self.log.setStyleSheet("background-color: rgb(0, 0, 0); color: red;")
        else:
            self.log.setStyleSheet("background-color: rgb(0, 0, 0); color: white;")

        self.log.moveCursor(QTextCursor.End)
        self.log.insertPlainText(message + '\n')
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
