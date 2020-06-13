#!/usr/bin/env python
# encoding:utf-8

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_Form


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.login_Button.clicked.connect(self.display)
        self.cancel_Button.clicked.connect(self.close)

    def display(self):
        username = self.user_lineEdit.text()
        password = self.pwd_lineEdit.text()


        
        self.user_textBrowser.setText("登录成功!\n" + "用户名是: " + username + ", 密码是: " + password)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
