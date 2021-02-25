import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QDesktopWidget,
                             QDialog, QTextEdit, QGridLayout, QPushButton, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

import serial
import test
from time import sleep

class Chat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.populateUI()

        self.resize(400, 400)
        self.center()
        self.setWindowTitle('RF-Chat')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def populateUI(self):
        self.createMenu()
        self.statusBar()
        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)

    def createMenu(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.createExitAction())

        helpMenu = menuBar.addMenu('&Help')
        helpMenu.addAction(self.createAboutAction())

    def createExitAction(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        return exitAction

    def createAboutAction(self):
        aboutAction = QAction(QIcon('info.png'), '&About', self)
        aboutAction.setShortcut('Ctrl+H')
        aboutAction.setStatusTip('Information about the program')
        aboutAction.triggered.connect(self.createAboutDialog)
        return aboutAction

    def createAboutDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('About')
        dialog.setWindowIcon(QIcon('info.png'))
        dialog.resize(200, 200)
        dialog.exec_()

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        def send_callback():
            cur_text = self.ribbon.toPlainText()
            msg = self.chat.toPlainText()
            msg_fmt = "{}: {}".format(self.name, msg)
            self.ribbon.setPlainText("{}{}\n".format(cur_text, msg_fmt))
            test.send_to_ser(msg_fmt)
            print("Sent!")

        def nameChange_callback():
            name_text = self.nameText.toPlainText()
            self.name = name_text
            cur_text = self.ribbon.toPlainText()
            msg = self.chat.toPlainText()
            msg_fmt = "{}: {}".format(self.name, msg)
            self.ribbon.setPlainText("{}{}\n".format(cur_text, msg_fmt))
            print("Name changed to: {}\n".format(name_text))

        # self.nameText = QTextEdit()
        # nameBtn = QPushButton('Change name')
        self.ribbon = QTextEdit()
        self.ribbon.setReadOnly(True)
        self.chat = QTextEdit()
        sendBtn = QPushButton('Send')
        sendBtn.clicked.connect(send_callback)
        self.name = "Noam"
        class RecvThread(QThread):
            # notifyProgress = QtCore.pyqtSignal(int)
            def __init__(self, ribbon, parent=None):
                QThread.__init__(self, parent)
                self.got_msg = pyqtSignal()
                self.ribbon = ribbon
            def run(self):
                while True:
                    print("getting from ser...")
                    msg = test.get_from_ser()
                    print("Got from Ser!")
                    # cur_text = self.ribbon.toPlainText()
                    # self.ribbon.setPlainText("{}{}\n".format(cur_text, msg))
                    self.got_msg.emit(msg)
                    sleep(1000)
        def update_ribbon_recv(msg):
            cur_text = self.ribbon.toPlainText()
            self.ribbon.setPlainText("{}{}\n".format(cur_text, msg))

        self.recvThread = RecvThread(self.ribbon)
        self.recvThread.start()
        self.recvThread.got_msg.connect(update_ribbon_recv)

        grid = QGridLayout()
        grid.setSpacing(3)
        grid.addWidget(self.ribbon, 0, 0, 1, 3)
        grid.addWidget(self.chat, 1, 0, 1, 1)
        grid.addWidget(sendBtn, 1, 2)

        self.setLayout(grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat = Chat()
    sys.exit(app.exec_())