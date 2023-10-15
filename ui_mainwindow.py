# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from myglwidget import MyGLWidget
from qjumpslider import QJumpSlider

import mainwindow_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 299, 1260, 371))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 2000, 352))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy1)
        self.scrollAreaWidgetContents_3.setMinimumSize(QSize(2000, 240))
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_11 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"font: 20px \"MS Shell Dlg 2\";")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_11.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label_11)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_13 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setMinimumSize(QSize(240, 0))
        self.pushButton_13.setMaximumSize(QSize(240, 16777215))
        self.pushButton_13.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_10.addWidget(self.pushButton_13)

        self.label_8 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(240, 240))
        self.label_8.setMaximumSize(QSize(240, 240))
        self.label_8.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_8.setScaledContents(True)

        self.verticalLayout_10.addWidget(self.label_8)

        self.pushButton_9 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setMinimumSize(QSize(240, 0))
        self.pushButton_9.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_10.addWidget(self.pushButton_9)


        self.horizontalLayout_3.addLayout(self.verticalLayout_10)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pushButton_8 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QSize(240, 0))
        self.pushButton_8.setMaximumSize(QSize(240, 16777215))
        self.pushButton_8.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_9.addWidget(self.pushButton_8)

        self.label_7 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(240, 240))
        self.label_7.setMaximumSize(QSize(240, 240))
        self.label_7.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_7.setScaledContents(True)

        self.verticalLayout_9.addWidget(self.label_7)

        self.pushButton_14 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)
        self.pushButton_14.setMinimumSize(QSize(240, 0))
        self.pushButton_14.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_9.addWidget(self.pushButton_14)


        self.horizontalLayout_3.addLayout(self.verticalLayout_9)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.pushButton_7 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setMinimumSize(QSize(240, 0))
        self.pushButton_7.setMaximumSize(QSize(240, 16777215))
        self.pushButton_7.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_8.addWidget(self.pushButton_7)

        self.label_6 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(240, 240))
        self.label_6.setMaximumSize(QSize(240, 240))
        self.label_6.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_6.setScaledContents(True)

        self.verticalLayout_8.addWidget(self.label_6)

        self.pushButton_15 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy)
        self.pushButton_15.setMinimumSize(QSize(240, 0))
        self.pushButton_15.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_8.addWidget(self.pushButton_15)


        self.horizontalLayout_3.addLayout(self.verticalLayout_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_6 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QSize(240, 0))
        self.pushButton_6.setMaximumSize(QSize(240, 16777215))
        self.pushButton_6.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_7.addWidget(self.pushButton_6)

        self.label_5 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(240, 240))
        self.label_5.setMaximumSize(QSize(240, 240))
        self.label_5.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_5.setScaledContents(True)

        self.verticalLayout_7.addWidget(self.label_5)

        self.pushButton_16 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy)
        self.pushButton_16.setMinimumSize(QSize(240, 0))
        self.pushButton_16.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_7.addWidget(self.pushButton_16)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_5 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QSize(240, 0))
        self.pushButton_5.setMaximumSize(QSize(240, 16777215))
        self.pushButton_5.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_6.addWidget(self.pushButton_5)

        self.label_4 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(240, 240))
        self.label_4.setMaximumSize(QSize(240, 240))
        self.label_4.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_4.setScaledContents(True)

        self.verticalLayout_6.addWidget(self.label_4)

        self.pushButton_17 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setMinimumSize(QSize(240, 0))
        self.pushButton_17.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_6.addWidget(self.pushButton_17)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_4 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QSize(240, 0))
        self.pushButton_4.setMaximumSize(QSize(240, 16777215))
        self.pushButton_4.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_5.addWidget(self.pushButton_4)

        self.label_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(240, 240))
        self.label_3.setMaximumSize(QSize(240, 240))
        self.label_3.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_3.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.label_3)

        self.pushButton_18 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_18.setObjectName(u"pushButton_18")
        sizePolicy.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy)
        self.pushButton_18.setMinimumSize(QSize(240, 0))
        self.pushButton_18.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_5.addWidget(self.pushButton_18)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_3 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QSize(240, 0))
        self.pushButton_3.setMaximumSize(QSize(240, 16777215))
        self.pushButton_3.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_4.addWidget(self.pushButton_3)

        self.label_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(240, 240))
        self.label_2.setMaximumSize(QSize(240, 240))
        self.label_2.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_2.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.label_2)

        self.pushButton_19 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_19.setObjectName(u"pushButton_19")
        sizePolicy.setHeightForWidth(self.pushButton_19.sizePolicy().hasHeightForWidth())
        self.pushButton_19.setSizePolicy(sizePolicy)
        self.pushButton_19.setMinimumSize(QSize(240, 0))
        self.pushButton_19.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_4.addWidget(self.pushButton_19)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(240, 0))
        self.pushButton.setMaximumSize(QSize(240, 16777215))
        self.pushButton.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.label = QLabel(self.scrollAreaWidgetContents_3)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(240, 240))
        self.label.setMaximumSize(QSize(240, 240))
        self.label.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.label)

        self.pushButton_20 = QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_20.setObjectName(u"pushButton_20")
        sizePolicy.setHeightForWidth(self.pushButton_20.sizePolicy().hasHeightForWidth())
        self.pushButton_20.setSizePolicy(sizePolicy)
        self.pushButton_20.setMinimumSize(QSize(240, 0))
        self.pushButton_20.setMaximumSize(QSize(240, 16777215))

        self.verticalLayout_3.addWidget(self.pushButton_20)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(80, 60, 191, 41))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(u"font: 20px \"MS Shell Dlg 2\";")
        self.horizontalSlider = QJumpSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(60, 200, 251, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(40, 150, 281, 41))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")
        self.pushButton_10 = QPushButton(self.centralwidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(940, 30, 301, 51))
        self.pushButton_10.setFont(font)
        self.pushButton_10.setStyleSheet(u"font: 17px \"MS Shell Dlg 2\";")
        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(940, 140, 301, 51))
        self.pushButton_11.setFont(font)
        self.pushButton_11.setStyleSheet(u"font: 17px \"MS Shell Dlg 2\";")
        self.pushButton_12 = QPushButton(self.centralwidget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(940, 210, 301, 51))
        self.pushButton_12.setFont(font)
        self.pushButton_12.setStyleSheet(u"font: 17px \"MS Shell Dlg 2\";")
        self.openGLWidget = MyGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName(u"openGLWidget")
        self.openGLWidget.setGeometry(QRect(376, 0, 528, 297))
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 190, 41, 41))
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(320, 190, 41, 41))
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(Qt.LeftToRight)
        self.label_13.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"3D Viewer Echo", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Select below to load cross section:", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Aortic Valve Level", None))
        self.label_8.setText("")
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Mitral Valve Level", None))
        self.label_7.setText("")
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Papillary Muscle Level", None))
        self.label_6.setText("")
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Longitudinal Section through Interatrial Septum", None))
        self.label_5.setText("")
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Longitudinal Section through Pulmonary Trunk", None))
        self.label_4.setText("")
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Longitudinal Section through Aorta", None))
        self.label_3.setText("")
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Pulmonary Valve Level", None))
        self.label_2.setText("")
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Tricuspid Valve Level", None))
        self.label.setText("")
        self.pushButton_20.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Import DICOM file", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Selected time frame index: 0", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Save edited landmarks to the\n"
"current cross-section", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Export all cross-section images\n"
"in the current time frame", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Export all cross-section images\n"
"in all time frames", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"99", None))
    # retranslateUi

