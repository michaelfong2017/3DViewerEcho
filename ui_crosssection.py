# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crosssection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import mainwindow_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(242, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_13 = QPushButton(Form)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setMinimumSize(QSize(240, 0))
        self.pushButton_13.setMaximumSize(QSize(240, 16777215))
        self.pushButton_13.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_10.addWidget(self.pushButton_13)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(240, 240))
        self.label_8.setMaximumSize(QSize(240, 240))
        self.label_8.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_8.setScaledContents(True)

        self.verticalLayout_10.addWidget(self.label_8)

        self.pushButton_9 = QPushButton(Form)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setMinimumSize(QSize(240, 0))
        self.pushButton_9.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_10.addWidget(self.pushButton_9)


        self.verticalLayout.addLayout(self.verticalLayout_10)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_13.setText(QCoreApplication.translate("Form", u"Transverse Section at Aortic Valve Level", None))
        self.label_8.setText("")
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"Export as PNG", None))
    # retranslateUi

