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
from scrollareawidget import ScrollAreaWidget
from mygridwidget import MyGridWidget

import mainwindow_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_7 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")

        self.verticalLayout_16.addWidget(self.label_24)

        self.label_26 = QLabel(self.centralwidget)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_16.addWidget(self.label_26)

        self.label_25 = QLabel(self.centralwidget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_16.addWidget(self.label_25)


        self.verticalLayout_13.addLayout(self.verticalLayout_16)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_13.addItem(self.verticalSpacer_7)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")

        self.verticalLayout_15.addWidget(self.label_17)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_15.addWidget(self.label_16)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_15.addWidget(self.label_15)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_15.addWidget(self.label_9)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_15.addWidget(self.label_14)


        self.verticalLayout_13.addLayout(self.verticalLayout_15)


        self.verticalLayout_14.addLayout(self.verticalLayout_13)

        self.openGLWidget = MyGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)
        self.openGLWidget.setMinimumSize(QSize(480, 261))

        self.verticalLayout_14.addWidget(self.openGLWidget)

        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_14.addWidget(self.label_18)

        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_14.addWidget(self.label_19)

        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_14.addWidget(self.label_20)

        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.verticalLayout_14.addWidget(self.label_21)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_3)

        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"font: 13px \"MS Shell Dlg 2\";")

        self.verticalLayout_14.addWidget(self.label_22)


        self.horizontalLayout_7.addLayout(self.verticalLayout_14)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_21 = QPushButton(self.centralwidget)
        self.pushButton_21.setObjectName(u"pushButton_21")
        sizePolicy.setHeightForWidth(self.pushButton_21.sizePolicy().hasHeightForWidth())
        self.pushButton_21.setSizePolicy(sizePolicy)
        self.pushButton_21.setMaximumSize(QSize(28, 16777215))
        self.pushButton_21.setStyleSheet(u"image: url(:/images/icons8-play-button-48.png);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_5.addWidget(self.pushButton_21)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(Qt.LeftToRight)
        self.label_12.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_12)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalSpacer = QSpacerItem(250, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_11.addItem(self.verticalSpacer)

        self.horizontalSlider = QJumpSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_11.addWidget(self.horizontalSlider)

        self.verticalSpacer_2 = QSpacerItem(250, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_11.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(Qt.LeftToRight)
        self.label_13.setStyleSheet(u"font: 18px \"MS Shell Dlg 2\";")
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_13)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout_12.addLayout(self.verticalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setEnabled(False)
        self.pushButton_11.setMinimumSize(QSize(200, 0))
        self.pushButton_11.setStyleSheet(u"font: 12px \"MS Shell Dlg 2\";")

        self.horizontalLayout_3.addWidget(self.pushButton_11)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.label_23 = QLabel(self.centralwidget)
        self.label_23.setObjectName(u"label_23")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)
        self.label_23.setStyleSheet(u"font: 15px \"MS Shell Dlg 2\";")

        self.horizontalLayout_3.addWidget(self.label_23)


        self.verticalLayout_12.addLayout(self.horizontalLayout_3)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout_12.addWidget(self.progressBar)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy3)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = ScrollAreaWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 753, 963))
        sizePolicy4 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy4)
        self.scrollAreaWidgetContents_3.setMinimumSize(QSize(0, 0))
        self.scrollAreaWidgetContents_3.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_11 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"font: 20px \"MS Shell Dlg 2\";")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_11.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label_11)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridWidget = MyGridWidget(self.scrollAreaWidgetContents_3)
        self.gridWidget.setObjectName(u"gridWidget")
        sizePolicy3.setHeightForWidth(self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy3)
        self.gridLayout_2 = QGridLayout(self.gridWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_13 = QPushButton(self.gridWidget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy6)
        self.pushButton_13.setMinimumSize(QSize(0, 0))
        self.pushButton_13.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_13.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.horizontalLayout_2.addWidget(self.pushButton_13)

        self.pushButton_2 = QPushButton(self.gridWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMaximumSize(QSize(23, 16777215))
        self.pushButton_2.setStyleSheet(u"image: url(:/images/Counterclockwise_rotating_circular_arrow_symbol.png);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_10 = QPushButton(self.gridWidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)
        self.pushButton_10.setMaximumSize(QSize(23, 16777215))
        self.pushButton_10.setStyleSheet(u"image: url(:/images/Clockwise_rotating_circular_arrow_symbol.png);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_2.addWidget(self.pushButton_10)


        self.verticalLayout_10.addLayout(self.horizontalLayout_2)

        self.label_8 = QLabel(self.gridWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setMinimumSize(QSize(0, 240))
        self.label_8.setMaximumSize(QSize(16777215, 16777215))
        self.label_8.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_8.setScaledContents(True)

        self.verticalLayout_10.addWidget(self.label_8)

        self.pushButton_9 = QPushButton(self.gridWidget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy6.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy6)
        self.pushButton_9.setMinimumSize(QSize(0, 0))
        self.pushButton_9.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_10.addWidget(self.pushButton_9)


        self.gridLayout_2.addLayout(self.verticalLayout_10, 0, 0, 1, 1)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pushButton_8 = QPushButton(self.gridWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy6.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy6)
        self.pushButton_8.setMinimumSize(QSize(0, 0))
        self.pushButton_8.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_8.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_9.addWidget(self.pushButton_8)

        self.label_7 = QLabel(self.gridWidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setMinimumSize(QSize(0, 240))
        self.label_7.setMaximumSize(QSize(16777215, 16777215))
        self.label_7.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_7.setScaledContents(True)

        self.verticalLayout_9.addWidget(self.label_7)

        self.pushButton_14 = QPushButton(self.gridWidget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy6.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy6)
        self.pushButton_14.setMinimumSize(QSize(0, 0))
        self.pushButton_14.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_9.addWidget(self.pushButton_14)


        self.gridLayout_2.addLayout(self.verticalLayout_9, 0, 1, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_6 = QPushButton(self.gridWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy6.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy6)
        self.pushButton_6.setMinimumSize(QSize(0, 0))
        self.pushButton_6.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_6.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_7.addWidget(self.pushButton_6)

        self.label_5 = QLabel(self.gridWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMinimumSize(QSize(0, 240))
        self.label_5.setMaximumSize(QSize(16777215, 16777215))
        self.label_5.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_5.setScaledContents(True)

        self.verticalLayout_7.addWidget(self.label_5)

        self.pushButton_16 = QPushButton(self.gridWidget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy6.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy6)
        self.pushButton_16.setMinimumSize(QSize(0, 0))
        self.pushButton_16.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_7.addWidget(self.pushButton_16)


        self.gridLayout_2.addLayout(self.verticalLayout_7, 1, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_5 = QPushButton(self.gridWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy6.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy6)
        self.pushButton_5.setMinimumSize(QSize(0, 0))
        self.pushButton_5.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_5.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_6.addWidget(self.pushButton_5)

        self.label_4 = QLabel(self.gridWidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setMinimumSize(QSize(0, 240))
        self.label_4.setMaximumSize(QSize(16777215, 16777215))
        self.label_4.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_4.setScaledContents(True)

        self.verticalLayout_6.addWidget(self.label_4)

        self.pushButton_17 = QPushButton(self.gridWidget)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy6.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy6)
        self.pushButton_17.setMinimumSize(QSize(0, 0))
        self.pushButton_17.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.pushButton_17)


        self.gridLayout_2.addLayout(self.verticalLayout_6, 1, 1, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.pushButton_7 = QPushButton(self.gridWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy6.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy6)
        self.pushButton_7.setMinimumSize(QSize(0, 0))
        self.pushButton_7.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_7.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_8.addWidget(self.pushButton_7)

        self.label_6 = QLabel(self.gridWidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        self.label_6.setMinimumSize(QSize(0, 240))
        self.label_6.setMaximumSize(QSize(16777215, 16777215))
        self.label_6.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_6.setScaledContents(True)

        self.verticalLayout_8.addWidget(self.label_6)

        self.pushButton_15 = QPushButton(self.gridWidget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy6.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy6)
        self.pushButton_15.setMinimumSize(QSize(0, 0))
        self.pushButton_15.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_8.addWidget(self.pushButton_15)


        self.gridLayout_2.addLayout(self.verticalLayout_8, 0, 2, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_4 = QPushButton(self.gridWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy6.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy6)
        self.pushButton_4.setMinimumSize(QSize(0, 0))
        self.pushButton_4.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_4.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_5.addWidget(self.pushButton_4)

        self.label_3 = QLabel(self.gridWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(0, 240))
        self.label_3.setMaximumSize(QSize(16777215, 16777215))
        self.label_3.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_3.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.label_3)

        self.pushButton_18 = QPushButton(self.gridWidget)
        self.pushButton_18.setObjectName(u"pushButton_18")
        sizePolicy6.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy6)
        self.pushButton_18.setMinimumSize(QSize(0, 0))
        self.pushButton_18.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_5.addWidget(self.pushButton_18)


        self.gridLayout_2.addLayout(self.verticalLayout_5, 1, 2, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_3 = QPushButton(self.gridWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy6.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy6)
        self.pushButton_3.setMinimumSize(QSize(0, 0))
        self.pushButton_3.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_3.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_4.addWidget(self.pushButton_3)

        self.label_2 = QLabel(self.gridWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setMinimumSize(QSize(0, 240))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_2.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.label_2)

        self.pushButton_19 = QPushButton(self.gridWidget)
        self.pushButton_19.setObjectName(u"pushButton_19")
        sizePolicy6.setHeightForWidth(self.pushButton_19.sizePolicy().hasHeightForWidth())
        self.pushButton_19.setSizePolicy(sizePolicy6)
        self.pushButton_19.setMinimumSize(QSize(0, 0))
        self.pushButton_19.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_4.addWidget(self.pushButton_19)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 2, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton = QPushButton(self.gridWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy6.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy6)
        self.pushButton.setMinimumSize(QSize(0, 0))
        self.pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.label = QLabel(self.gridWidget)
        self.label.setObjectName(u"label")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy7)
        self.label.setMinimumSize(QSize(0, 240))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.label.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.label)

        self.pushButton_20 = QPushButton(self.gridWidget)
        self.pushButton_20.setObjectName(u"pushButton_20")
        sizePolicy6.setHeightForWidth(self.pushButton_20.sizePolicy().hasHeightForWidth())
        self.pushButton_20.setSizePolicy(sizePolicy6)
        self.pushButton_20.setMinimumSize(QSize(0, 0))
        self.pushButton_20.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.pushButton_20)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.gridWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_12.addWidget(self.scrollArea)


        self.horizontalLayout_7.addLayout(self.verticalLayout_12)

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
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Patient Info:", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Height: 170cm", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Weight: 60kg", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"DICOM File (Video) Info:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Video - Number of Frames: ", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Video - Average Frame Time: ", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Video - FPS: ", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Video - Total Duration: ", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Press W to zoom in, S to zoom out", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Press Q to move camera upward, E to move camera downward", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Press A to move camera leftward, D to move camera rightward", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Left click and drag the mouse for arcball rotation", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"v1.0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Selected time frame index: 0", None))
        self.pushButton_21.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"99", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Analyze A2C && A4C videos", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"[78.637375 68.21405  73.799355 56.29574  62.208237 59.00993 ]", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Click view name to highlight cross section:", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"A2C", None))
        self.pushButton_2.setText("")
        self.pushButton_10.setText("")
        self.label_8.setText("")
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"A4C", None))
        self.label_7.setText("")
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"SAXM", None))
        self.label_5.setText("")
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"SAXMV", None))
        self.label_4.setText("")
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"ALAX", None))
        self.label_6.setText("")
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.label_3.setText("")
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_2.setText("")
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Tricuspid Valve Level", None))
        self.label.setText("")
        self.pushButton_20.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
    # retranslateUi

