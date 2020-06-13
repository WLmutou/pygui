# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bg.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("切换背景图片")
        Form.resize(928, 623)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 40, 931, 521))
        self.label.setStyleSheet("border-image: url(:/img/PlutoCrescent_ZH-CN3538488331_1920x1080.jpg);")
        self.label.setObjectName("label")
        self.selectBgBtn = QtWidgets.QPushButton(Form)
        self.selectBgBtn.setGeometry(QtCore.QRect(10, 10, 89, 25))
        self.selectBgBtn.setObjectName("selectBgBtn")
        self.okbtn = QtWidgets.QDialogButtonBox(Form)
        self.okbtn.setGeometry(QtCore.QRect(640, 590, 166, 25))
        self.okbtn.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.okbtn.setObjectName("okbtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "切换背景图片"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.selectBgBtn.setText(_translate("Form", "选择背景图片"))
import test_rc
