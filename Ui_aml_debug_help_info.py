# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\code\Python\amlogic_debug_tool\aml_debug_help_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AmlDebugHelpAboutInfo_Dialog(object):
    def setupUi(self, AmlDebugHelpAboutInfo_Dialog):
        AmlDebugHelpAboutInfo_Dialog.setObjectName("AmlDebugHelpAboutInfo_Dialog")
        AmlDebugHelpAboutInfo_Dialog.resize(517, 313)
        self.AmlDebugHelpAboutCancel_pushButton = QtWidgets.QPushButton(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutCancel_pushButton.setGeometry(QtCore.QRect(280, 240, 101, 31))
        self.AmlDebugHelpAboutCancel_pushButton.setObjectName("AmlDebugHelpAboutCancel_pushButton")
        self.AmlDebugHelpAboutInfo_Label = QtWidgets.QLabel(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutInfo_Label.setGeometry(QtCore.QRect(30, 20, 471, 141))
        self.AmlDebugHelpAboutInfo_Label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.AmlDebugHelpAboutInfo_Label.setObjectName("AmlDebugHelpAboutInfo_Label")
        self.AmlDebugHelpAboutUpdate_Label = QtWidgets.QLabel(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutUpdate_Label.setGeometry(QtCore.QRect(200, 200, 301, 21))
        self.AmlDebugHelpAboutUpdate_Label.setObjectName("AmlDebugHelpAboutUpdate_Label")
        self.AmlDebugHelpAboutUpdateNow_pushButton = QtWidgets.QPushButton(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutUpdateNow_pushButton.setGeometry(QtCore.QRect(30, 240, 161, 31))
        self.AmlDebugHelpAboutUpdateNow_pushButton.setObjectName("AmlDebugHelpAboutUpdateNow_pushButton")
        self.AmlDebugHelpAboutCheckUpdate_pushButton = QtWidgets.QPushButton(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutCheckUpdate_pushButton.setGeometry(QtCore.QRect(30, 200, 161, 31))
        self.AmlDebugHelpAboutCheckUpdate_pushButton.setObjectName("AmlDebugHelpAboutCheckUpdate_pushButton")

        self.retranslateUi(AmlDebugHelpAboutInfo_Dialog)
        self.AmlDebugHelpAboutCancel_pushButton.clicked.connect(AmlDebugHelpAboutInfo_Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AmlDebugHelpAboutInfo_Dialog)

    def retranslateUi(self, AmlDebugHelpAboutInfo_Dialog):
        _translate = QtCore.QCoreApplication.translate
        AmlDebugHelpAboutInfo_Dialog.setWindowTitle(_translate("AmlDebugHelpAboutInfo_Dialog", "Amlogic Debug Tool"))
        self.AmlDebugHelpAboutCancel_pushButton.setText(_translate("AmlDebugHelpAboutInfo_Dialog", "Close"))
        self.AmlDebugHelpAboutInfo_Label.setText(_translate("AmlDebugHelpAboutInfo_Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.AmlDebugHelpAboutUpdate_Label.setText(_translate("AmlDebugHelpAboutInfo_Dialog", "<html><head/><body><p align=\"center\">check for updates.</p></body></html>"))
        self.AmlDebugHelpAboutUpdateNow_pushButton.setText(_translate("AmlDebugHelpAboutInfo_Dialog", "Update Now"))
        self.AmlDebugHelpAboutCheckUpdate_pushButton.setText(_translate("AmlDebugHelpAboutInfo_Dialog", "Check For Updates"))
