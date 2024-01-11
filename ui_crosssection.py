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

from clickableqlabel import ClickableQLabel

import mainwindow_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(422, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_13 = QPushButton(Form)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy1)
        self.pushButton_13.setMinimumSize(QSize(0, 0))
        self.pushButton_13.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_13.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_10.addWidget(self.pushButton_13)

        self.label_8 = ClickableQLabel(Form)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(0, 240))
        self.label_8.setMaximumSize(QSize(16777215, 240))
        self.label_8.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_8.setScaledContents(False)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_8)

        self.pushButton_9 = QPushButton(Form)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy1.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy1)
        self.pushButton_9.setMinimumSize(QSize(0, 0))
        self.pushButton_9.setMaximumSize(QSize(16777215, 16777215))

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

