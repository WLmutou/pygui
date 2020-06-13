#!/usr/bin/env python
# encoding:utf-8

import sys 
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow,  QFileDialog
from PyQt5.QtGui import  QPixmap

from bg import  Ui_Form



class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        
        self.selectBgBtn.clicked.connect(self.changeBg)
        self.okbtn.accepted.connect(self.accepted)
        self.okbtn.rejected.connect(self.rejected)

    def changeBg(self):
        print ("change bg")
        fileName,fileType = QFileDialog.getOpenFileName(self, "选取文件",
                                                        os.getcwd(),
                                                        "*.jpg;;*.png;;*.jpeg")
        with open(fileName, "rb") as f:
            photo = QPixmap()
            photo.loadFromData(f.read())
            self.label.setPixmap(photo)
        
        pass
        
    def accepted(self):
        print ("accepted")
        
    def rejected(self):
        print ("rejected ...")
        sys.exit(0)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
