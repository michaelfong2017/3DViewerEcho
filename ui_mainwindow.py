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

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"font: 14px \"MS Shell Dlg 2\";")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_17 = QVBoxLayout(self.tab)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.scrollArea = QScrollArea(self.tab)
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
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 729, 972))
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

        self.verticalLayout_17.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_27 = QVBoxLayout(self.tab_2)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy3.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy3)
        self.scrollArea_2.setMinimumSize(QSize(0, 0))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = ScrollAreaWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 729, 972))
        sizePolicy4.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy4)
        self.scrollAreaWidgetContents_4.setMinimumSize(QSize(0, 0))
        self.scrollAreaWidgetContents_4.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_27 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_27.setObjectName(u"label_27")
        sizePolicy5.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy5)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet(u"font: 20px \"MS Shell Dlg 2\";")
        self.label_27.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_27.setWordWrap(False)

        self.horizontalLayout_4.addWidget(self.label_27)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_18.addLayout(self.horizontalLayout_4)

        self.gridWidget_2 = MyGridWidget(self.scrollAreaWidgetContents_4)
        self.gridWidget_2.setObjectName(u"gridWidget_2")
        sizePolicy3.setHeightForWidth(self.gridWidget_2.sizePolicy().hasHeightForWidth())
        self.gridWidget_2.setSizePolicy(sizePolicy3)
        self.gridLayout_3 = QGridLayout(self.gridWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_22 = QPushButton(self.gridWidget_2)
        self.pushButton_22.setObjectName(u"pushButton_22")
        sizePolicy6.setHeightForWidth(self.pushButton_22.sizePolicy().hasHeightForWidth())
        self.pushButton_22.setSizePolicy(sizePolicy6)
        self.pushButton_22.setMinimumSize(QSize(0, 0))
        self.pushButton_22.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_22.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.horizontalLayout_8.addWidget(self.pushButton_22)

        self.pushButton_12 = QPushButton(self.gridWidget_2)
        self.pushButton_12.setObjectName(u"pushButton_12")
        sizePolicy.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy)
        self.pushButton_12.setMaximumSize(QSize(23, 16777215))
        self.pushButton_12.setStyleSheet(u"image: url(:/images/Counterclockwise_rotating_circular_arrow_symbol.png);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_8.addWidget(self.pushButton_12)

        self.pushButton_23 = QPushButton(self.gridWidget_2)
        self.pushButton_23.setObjectName(u"pushButton_23")
        sizePolicy.setHeightForWidth(self.pushButton_23.sizePolicy().hasHeightForWidth())
        self.pushButton_23.setSizePolicy(sizePolicy)
        self.pushButton_23.setMaximumSize(QSize(23, 16777215))
        self.pushButton_23.setStyleSheet(u"image: url(:/images/Clockwise_rotating_circular_arrow_symbol.png);\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_8.addWidget(self.pushButton_23)


        self.verticalLayout_19.addLayout(self.horizontalLayout_8)

        self.label_28 = QLabel(self.gridWidget_2)
        self.label_28.setObjectName(u"label_28")
        sizePolicy3.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy3)
        self.label_28.setMinimumSize(QSize(0, 240))
        self.label_28.setMaximumSize(QSize(16777215, 16777215))
        self.label_28.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_28.setScaledContents(True)

        self.verticalLayout_19.addWidget(self.label_28)

        self.pushButton_24 = QPushButton(self.gridWidget_2)
        self.pushButton_24.setObjectName(u"pushButton_24")
        sizePolicy6.setHeightForWidth(self.pushButton_24.sizePolicy().hasHeightForWidth())
        self.pushButton_24.setSizePolicy(sizePolicy6)
        self.pushButton_24.setMinimumSize(QSize(0, 0))
        self.pushButton_24.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_19.addWidget(self.pushButton_24)


        self.gridLayout_3.addLayout(self.verticalLayout_19, 0, 0, 1, 1)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.pushButton_25 = QPushButton(self.gridWidget_2)
        self.pushButton_25.setObjectName(u"pushButton_25")
        sizePolicy6.setHeightForWidth(self.pushButton_25.sizePolicy().hasHeightForWidth())
        self.pushButton_25.setSizePolicy(sizePolicy6)
        self.pushButton_25.setMinimumSize(QSize(0, 0))
        self.pushButton_25.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_25.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_20.addWidget(self.pushButton_25)

        self.label_29 = QLabel(self.gridWidget_2)
        self.label_29.setObjectName(u"label_29")
        sizePolicy3.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy3)
        self.label_29.setMinimumSize(QSize(0, 240))
        self.label_29.setMaximumSize(QSize(16777215, 16777215))
        self.label_29.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_29.setScaledContents(True)

        self.verticalLayout_20.addWidget(self.label_29)

        self.pushButton_26 = QPushButton(self.gridWidget_2)
        self.pushButton_26.setObjectName(u"pushButton_26")
        sizePolicy6.setHeightForWidth(self.pushButton_26.sizePolicy().hasHeightForWidth())
        self.pushButton_26.setSizePolicy(sizePolicy6)
        self.pushButton_26.setMinimumSize(QSize(0, 0))
        self.pushButton_26.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_20.addWidget(self.pushButton_26)


        self.gridLayout_3.addLayout(self.verticalLayout_20, 0, 1, 1, 1)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.pushButton_27 = QPushButton(self.gridWidget_2)
        self.pushButton_27.setObjectName(u"pushButton_27")
        sizePolicy6.setHeightForWidth(self.pushButton_27.sizePolicy().hasHeightForWidth())
        self.pushButton_27.setSizePolicy(sizePolicy6)
        self.pushButton_27.setMinimumSize(QSize(0, 0))
        self.pushButton_27.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_27.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_21.addWidget(self.pushButton_27)

        self.label_30 = QLabel(self.gridWidget_2)
        self.label_30.setObjectName(u"label_30")
        sizePolicy3.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy3)
        self.label_30.setMinimumSize(QSize(0, 240))
        self.label_30.setMaximumSize(QSize(16777215, 16777215))
        self.label_30.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_30.setScaledContents(True)

        self.verticalLayout_21.addWidget(self.label_30)

        self.pushButton_28 = QPushButton(self.gridWidget_2)
        self.pushButton_28.setObjectName(u"pushButton_28")
        sizePolicy6.setHeightForWidth(self.pushButton_28.sizePolicy().hasHeightForWidth())
        self.pushButton_28.setSizePolicy(sizePolicy6)
        self.pushButton_28.setMinimumSize(QSize(0, 0))
        self.pushButton_28.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_21.addWidget(self.pushButton_28)


        self.gridLayout_3.addLayout(self.verticalLayout_21, 1, 0, 1, 1)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.pushButton_29 = QPushButton(self.gridWidget_2)
        self.pushButton_29.setObjectName(u"pushButton_29")
        sizePolicy6.setHeightForWidth(self.pushButton_29.sizePolicy().hasHeightForWidth())
        self.pushButton_29.setSizePolicy(sizePolicy6)
        self.pushButton_29.setMinimumSize(QSize(0, 0))
        self.pushButton_29.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_29.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_22.addWidget(self.pushButton_29)

        self.label_31 = QLabel(self.gridWidget_2)
        self.label_31.setObjectName(u"label_31")
        sizePolicy3.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy3)
        self.label_31.setMinimumSize(QSize(0, 240))
        self.label_31.setMaximumSize(QSize(16777215, 16777215))
        self.label_31.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_31.setScaledContents(True)

        self.verticalLayout_22.addWidget(self.label_31)

        self.pushButton_30 = QPushButton(self.gridWidget_2)
        self.pushButton_30.setObjectName(u"pushButton_30")
        sizePolicy6.setHeightForWidth(self.pushButton_30.sizePolicy().hasHeightForWidth())
        self.pushButton_30.setSizePolicy(sizePolicy6)
        self.pushButton_30.setMinimumSize(QSize(0, 0))
        self.pushButton_30.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_22.addWidget(self.pushButton_30)


        self.gridLayout_3.addLayout(self.verticalLayout_22, 1, 1, 1, 1)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.pushButton_31 = QPushButton(self.gridWidget_2)
        self.pushButton_31.setObjectName(u"pushButton_31")
        sizePolicy6.setHeightForWidth(self.pushButton_31.sizePolicy().hasHeightForWidth())
        self.pushButton_31.setSizePolicy(sizePolicy6)
        self.pushButton_31.setMinimumSize(QSize(0, 0))
        self.pushButton_31.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_31.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_23.addWidget(self.pushButton_31)

        self.label_32 = QLabel(self.gridWidget_2)
        self.label_32.setObjectName(u"label_32")
        sizePolicy3.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy3)
        self.label_32.setMinimumSize(QSize(0, 240))
        self.label_32.setMaximumSize(QSize(16777215, 16777215))
        self.label_32.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_32.setScaledContents(True)

        self.verticalLayout_23.addWidget(self.label_32)

        self.pushButton_32 = QPushButton(self.gridWidget_2)
        self.pushButton_32.setObjectName(u"pushButton_32")
        sizePolicy6.setHeightForWidth(self.pushButton_32.sizePolicy().hasHeightForWidth())
        self.pushButton_32.setSizePolicy(sizePolicy6)
        self.pushButton_32.setMinimumSize(QSize(0, 0))
        self.pushButton_32.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_23.addWidget(self.pushButton_32)


        self.gridLayout_3.addLayout(self.verticalLayout_23, 0, 2, 1, 1)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.pushButton_33 = QPushButton(self.gridWidget_2)
        self.pushButton_33.setObjectName(u"pushButton_33")
        sizePolicy6.setHeightForWidth(self.pushButton_33.sizePolicy().hasHeightForWidth())
        self.pushButton_33.setSizePolicy(sizePolicy6)
        self.pushButton_33.setMinimumSize(QSize(0, 0))
        self.pushButton_33.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_33.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_24.addWidget(self.pushButton_33)

        self.label_33 = QLabel(self.gridWidget_2)
        self.label_33.setObjectName(u"label_33")
        sizePolicy3.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy3)
        self.label_33.setMinimumSize(QSize(0, 240))
        self.label_33.setMaximumSize(QSize(16777215, 16777215))
        self.label_33.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_33.setScaledContents(True)

        self.verticalLayout_24.addWidget(self.label_33)

        self.pushButton_34 = QPushButton(self.gridWidget_2)
        self.pushButton_34.setObjectName(u"pushButton_34")
        sizePolicy6.setHeightForWidth(self.pushButton_34.sizePolicy().hasHeightForWidth())
        self.pushButton_34.setSizePolicy(sizePolicy6)
        self.pushButton_34.setMinimumSize(QSize(0, 0))
        self.pushButton_34.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_24.addWidget(self.pushButton_34)


        self.gridLayout_3.addLayout(self.verticalLayout_24, 1, 2, 1, 1)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.pushButton_35 = QPushButton(self.gridWidget_2)
        self.pushButton_35.setObjectName(u"pushButton_35")
        sizePolicy6.setHeightForWidth(self.pushButton_35.sizePolicy().hasHeightForWidth())
        self.pushButton_35.setSizePolicy(sizePolicy6)
        self.pushButton_35.setMinimumSize(QSize(0, 0))
        self.pushButton_35.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_35.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_25.addWidget(self.pushButton_35)

        self.label_34 = QLabel(self.gridWidget_2)
        self.label_34.setObjectName(u"label_34")
        sizePolicy3.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy3)
        self.label_34.setMinimumSize(QSize(0, 240))
        self.label_34.setMaximumSize(QSize(16777215, 16777215))
        self.label_34.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_34.setScaledContents(True)

        self.verticalLayout_25.addWidget(self.label_34)

        self.pushButton_36 = QPushButton(self.gridWidget_2)
        self.pushButton_36.setObjectName(u"pushButton_36")
        sizePolicy6.setHeightForWidth(self.pushButton_36.sizePolicy().hasHeightForWidth())
        self.pushButton_36.setSizePolicy(sizePolicy6)
        self.pushButton_36.setMinimumSize(QSize(0, 0))
        self.pushButton_36.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_25.addWidget(self.pushButton_36)


        self.gridLayout_3.addLayout(self.verticalLayout_25, 2, 0, 1, 1)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.pushButton_37 = QPushButton(self.gridWidget_2)
        self.pushButton_37.setObjectName(u"pushButton_37")
        sizePolicy6.setHeightForWidth(self.pushButton_37.sizePolicy().hasHeightForWidth())
        self.pushButton_37.setSizePolicy(sizePolicy6)
        self.pushButton_37.setMinimumSize(QSize(0, 0))
        self.pushButton_37.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_37.setStyleSheet(u"font: 10px \"MS Shell Dlg 2\";")

        self.verticalLayout_26.addWidget(self.pushButton_37)

        self.label_35 = QLabel(self.gridWidget_2)
        self.label_35.setObjectName(u"label_35")
        sizePolicy7.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy7)
        self.label_35.setMinimumSize(QSize(0, 240))
        self.label_35.setMaximumSize(QSize(16777215, 16777215))
        self.label_35.setPixmap(QPixmap(u":/images/annotated_heart_sample.png"))
        self.label_35.setScaledContents(True)

        self.verticalLayout_26.addWidget(self.label_35)

        self.pushButton_38 = QPushButton(self.gridWidget_2)
        self.pushButton_38.setObjectName(u"pushButton_38")
        sizePolicy6.setHeightForWidth(self.pushButton_38.sizePolicy().hasHeightForWidth())
        self.pushButton_38.setSizePolicy(sizePolicy6)
        self.pushButton_38.setMinimumSize(QSize(0, 0))
        self.pushButton_38.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_26.addWidget(self.pushButton_38)


        self.gridLayout_3.addLayout(self.verticalLayout_26, 2, 1, 1, 1)


        self.verticalLayout_18.addWidget(self.gridWidget_2)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_27.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_12.addWidget(self.tabWidget)


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

        self.tabWidget.setCurrentIndex(0)


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
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"v2.0", None))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Single frame predictions", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Click view name to highlight cross section:", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"A2C", None))
        self.pushButton_12.setText("")
        self.pushButton_23.setText("")
        self.label_28.setText("")
        self.pushButton_24.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_25.setText(QCoreApplication.translate("MainWindow", u"A4C", None))
        self.label_29.setText("")
        self.pushButton_26.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_27.setText(QCoreApplication.translate("MainWindow", u"SAXM", None))
        self.label_30.setText("")
        self.pushButton_28.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_29.setText(QCoreApplication.translate("MainWindow", u"SAXMV", None))
        self.label_31.setText("")
        self.pushButton_30.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_31.setText(QCoreApplication.translate("MainWindow", u"ALAX", None))
        self.label_32.setText("")
        self.pushButton_32.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_33.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.label_33.setText("")
        self.pushButton_34.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_35.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_34.setText("")
        self.pushButton_36.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.pushButton_37.setText(QCoreApplication.translate("MainWindow", u"Transverse Section at Tricuspid Valve Level", None))
        self.label_35.setText("")
        self.pushButton_38.setText(QCoreApplication.translate("MainWindow", u"Export as PNG", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Advanced predictions", None))
    # retranslateUi

