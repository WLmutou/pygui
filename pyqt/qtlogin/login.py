# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(579, 287)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 40, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 67, 17))
        self.label_2.setObjectName("label_2")
        self.user_lineEdit = QtWidgets.QLineEdit(Form)
        self.user_lineEdit.setGeometry(QtCore.QRect(120, 30, 113, 25))
        self.user_lineEdit.setObjectName("lineEdit")
        self.pwd_lineEdit = QtWidgets.QLineEdit(Form)
        self.pwd_lineEdit.setGeometry(QtCore.QRect(120, 90, 113, 25))
        self.pwd_lineEdit.setObjectName("lineEdit_2")
        self.login_Button = QtWidgets.QPushButton(Form)
        self.login_Button.setGeometry(QtCore.QRect(10, 140, 89, 25))
        self.login_Button.setObjectName("pushButton")
        self.cancel_Button = QtWidgets.QPushButton(Form)
        self.cancel_Button.setGeometry(QtCore.QRect(130, 140, 89, 25))
        self.cancel_Button.setObjectName("pushButton_2")
        self.user_textBrowser = QtWidgets.QTextEdit(Form)
        self.user_textBrowser.setGeometry(QtCore.QRect(280, 30, 251, 131))
        self.user_textBrowser.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "用户名"))
        self.label_2.setText(_translate("Form", "密码"))
        self.login_Button.setText(_translate("Form", "登录"))
        self.cancel_Button.setText(_translate("Form", "退出"))
