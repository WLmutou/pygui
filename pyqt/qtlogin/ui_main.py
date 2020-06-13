#!/usr/bin/env python
# encoding:utf-8


from PyQt5.QtWidgets import QApplication, QMainWindow, QMainWindow
from main_win import Ui_MainForm


class Ui_Main(QMainWindow, Ui_MainForm):
    def __init__(self, parent=None):
        super(Ui_Main, self).__init__(parent)
        self.setupUi(self)


