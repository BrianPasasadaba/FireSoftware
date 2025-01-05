#MainWindowFeed.py
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowFeed.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1103, 1000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.MainHeader_box = QGroupBox(self.centralwidget)
        self.MainHeader_box.setObjectName(u"MainHeader_box")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainHeader_box.sizePolicy().hasHeightForWidth())
        self.MainHeader_box.setSizePolicy(sizePolicy)
        self.MainHeader_box.setMaximumSize(QSize(16777215, 120))
        self.MainHeader_box.setStyleSheet(u"#header_bbox{\n"
"	border: none;\n"
"}")
        self.gridLayout_2 = QGridLayout(self.MainHeader_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.header_left = QGroupBox(self.MainHeader_box)
        self.header_left.setObjectName(u"header_left")
        self.gridLayout_3 = QGridLayout(self.header_left)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.hdleft_label = QLabel(self.header_left)
        self.hdleft_label.setObjectName(u"hdleft_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.hdleft_label.sizePolicy().hasHeightForWidth())
        self.hdleft_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(22)
        font.setBold(False)
        self.hdleft_label.setFont(font)

        self.gridLayout_3.addWidget(self.hdleft_label, 0, 0, 1, 1)

        self.feed_ipselect = QComboBox(self.header_left)
        self.feed_ipselect.setObjectName(u"feed_ipselect")
        sizePolicy1.setHeightForWidth(self.feed_ipselect.sizePolicy().hasHeightForWidth())
        self.feed_ipselect.setSizePolicy(sizePolicy1)
        self.feed_ipselect.setMinimumSize(QSize(400, 40))
        self.feed_ipselect.setMaximumSize(QSize(300, 50))
        font1 = QFont()
        font1.setFamilies([u"MS Sans Serif"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setUnderline(False)
        self.feed_ipselect.setFont(font1)
        self.feed_ipselect.setStyleSheet(u"#feed_ipselect{\n"
"	background-color: white;\n"
"	selection-background-color: qlineargradient(spread:pad, x1:0.04, y1:0.085, x2:0.949, y2:0.994, stop:0.198864 rgba(30, 52, 128, 255), stop:0.607955 rgba(99, 115, 170, 255), stop:1 rgba(202, 207, 225, 255));\n"
"}\n"
"")

        self.gridLayout_3.addWidget(self.feed_ipselect, 0, 1, 1, 1)

        self.hdleft_btnbox = QGroupBox(self.header_left)
        self.hdleft_btnbox.setObjectName(u"hdleft_btnbox")
        self.hdleft_btnbox.setMinimumSize(QSize(200, 0))
        self.horizontalLayout = QHBoxLayout(self.hdleft_btnbox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_btn = QPushButton(self.hdleft_btnbox)
        self.add_btn.setObjectName(u"add_btn")
        font2 = QFont()
        font2.setBold(True)
        self.add_btn.setFont(font2)
        self.add_btn.setStyleSheet(u"#add_btn{\n"
"	border-radius: 5px;\n"
"	background-color: rgba(0, 9, 73, 1);\n"
"	color: white;\n"
"	width: 85px;\n"
"	height: 30px;\n"
"}\n"
"\n"
"#add_btn:hover {\n"
"	background-color:rgba(0, 9, 73, 0.69);\n"
"}")

        self.horizontalLayout.addWidget(self.add_btn)

        self.remove_btn = QPushButton(self.hdleft_btnbox)
        self.remove_btn.setObjectName(u"remove_btn")
        self.remove_btn.setFont(font2)
        self.remove_btn.setStyleSheet(u"#remove_btn{\n"
"	border-radius: 5px;\n"
"	background-color: rgba(0, 9, 73, 1);\n"
"	color: white;\n"
"	width: 85px;\n"
"	height: 30px;\n"
"}\n"
"\n"
"#remove_btn:hover {\n"
"	background-color:rgba(0, 9, 73, 0.69);\n"
"}")

        self.horizontalLayout.addWidget(self.remove_btn)

        self.remove_ipselect = QComboBox(self.hdleft_btnbox)
        self.remove_ipselect.setObjectName(u"remove_ipselect")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.remove_ipselect.sizePolicy().hasHeightForWidth())
        self.remove_ipselect.setSizePolicy(sizePolicy2)
        self.remove_ipselect.setMinimumSize(QSize(150, 30))
        self.remove_ipselect.setStyleSheet(u"#remove_ipselect{\n"
"	background-color: lightpink;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(179, 38, 38);\n"
"}")

        self.horizontalLayout.addWidget(self.remove_ipselect)


        self.gridLayout_3.addWidget(self.hdleft_btnbox, 0, 2, 1, 1)


        self.gridLayout_2.addWidget(self.header_left, 0, 0, 1, 1)

        self.header_right = QGroupBox(self.MainHeader_box)
        self.header_right.setObjectName(u"header_right")
        sizePolicy1.setHeightForWidth(self.header_right.sizePolicy().hasHeightForWidth())
        self.header_right.setSizePolicy(sizePolicy1)
        self.header_right.setMinimumSize(QSize(0, 0))
        self.header_right.setMaximumSize(QSize(400, 16777215))
        self.formLayout = QFormLayout(self.header_right)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.hdr_timelabel = QLabel(self.header_right)
        self.hdr_timelabel.setObjectName(u"hdr_timelabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.hdr_timelabel.sizePolicy().hasHeightForWidth())
        self.hdr_timelabel.setSizePolicy(sizePolicy3)
        self.hdr_timelabel.setMinimumSize(QSize(0, 0))
        self.hdr_timelabel.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(16)
        font3.setBold(True)
        self.hdr_timelabel.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.hdr_timelabel)

        self.header_time = QLabel(self.header_right)
        self.header_time.setObjectName(u"header_time")
        font4 = QFont()
        font4.setPointSize(12)
        self.header_time.setFont(font4)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.header_time)

        self.hdr_datelabel = QLabel(self.header_right)
        self.hdr_datelabel.setObjectName(u"hdr_datelabel")
        self.hdr_datelabel.setFont(font3)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.hdr_datelabel)

        self.header_date = QLabel(self.header_right)
        self.header_date.setObjectName(u"header_date")
        self.header_date.setFont(font4)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.header_date)


        self.gridLayout_2.addWidget(self.header_right, 0, 2, 1, 1)

        self.header_bbox = QGroupBox(self.MainHeader_box)
        self.header_bbox.setObjectName(u"header_bbox")
        sizePolicy3.setHeightForWidth(self.header_bbox.sizePolicy().hasHeightForWidth())
        self.header_bbox.setSizePolicy(sizePolicy3)
        self.header_bbox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.header_bbox, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.MainHeader_box, 0, 0, 1, 1)

        self.MainBody_box = QGroupBox(self.centralwidget)
        self.MainBody_box.setObjectName(u"MainBody_box")
        self.gridLayout_4 = QGridLayout(self.MainBody_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.MainFeed_box = QGroupBox(self.MainBody_box)
        self.MainFeed_box.setObjectName(u"MainFeed_box")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.MainFeed_box.sizePolicy().hasHeightForWidth())
        self.MainFeed_box.setSizePolicy(sizePolicy4)
        self.MainFeed_box.setMinimumSize(QSize(0, 500))
        self.MainFeed_box.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_6 = QGridLayout(self.MainFeed_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ipinfo_feed1 = QLabel(self.MainFeed_box)
        self.ipinfo_feed1.setObjectName(u"ipinfo_feed1")
        sizePolicy.setHeightForWidth(self.ipinfo_feed1.sizePolicy().hasHeightForWidth())
        self.ipinfo_feed1.setSizePolicy(sizePolicy)
        font5 = QFont()
        font5.setPointSize(14)
        font5.setBold(True)
        font5.setUnderline(True)
        self.ipinfo_feed1.setFont(font5)
        self.ipinfo_feed1.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.ipinfo_feed1, 0, 0, 1, 1)

        self.lb_feed1 = QLabel(self.MainFeed_box)
        self.lb_feed1.setObjectName(u"lb_feed1")
        sizePolicy4.setHeightForWidth(self.lb_feed1.sizePolicy().hasHeightForWidth())
        self.lb_feed1.setSizePolicy(sizePolicy4)
        self.lb_feed1.setMaximumSize(QSize(16777215, 16777215))
        font6 = QFont()
        font6.setPointSize(28)
        font6.setBold(True)
        self.lb_feed1.setFont(font6)
        self.lb_feed1.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lb_feed1, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.MainFeed_box, 0, 0, 1, 1)

        self.SubFeed_box = QGroupBox(self.MainBody_box)
        self.SubFeed_box.setObjectName(u"SubFeed_box")
        sizePolicy4.setHeightForWidth(self.SubFeed_box.sizePolicy().hasHeightForWidth())
        self.SubFeed_box.setSizePolicy(sizePolicy4)
        self.SubFeed_box.setMinimumSize(QSize(300, 300))
        self.SubFeed_box.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout = QVBoxLayout(self.SubFeed_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_7 = QGroupBox(self.SubFeed_box)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_8 = QGridLayout(self.groupBox_7)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.ipinfo_feed2 = QLabel(self.groupBox_7)
        self.ipinfo_feed2.setObjectName(u"ipinfo_feed2")
        sizePolicy.setHeightForWidth(self.ipinfo_feed2.sizePolicy().hasHeightForWidth())
        self.ipinfo_feed2.setSizePolicy(sizePolicy)
        self.ipinfo_feed2.setFont(font5)
        self.ipinfo_feed2.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.ipinfo_feed2, 0, 0, 1, 1)

        self.lb_feed2 = QLabel(self.groupBox_7)
        self.lb_feed2.setObjectName(u"lb_feed2")
        self.lb_feed2.setFont(font6)
        self.lb_feed2.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lb_feed2, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_7)

        self.groupBox_6 = QGroupBox(self.SubFeed_box)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lb_feed3 = QLabel(self.groupBox_6)
        self.lb_feed3.setObjectName(u"lb_feed3")
        self.lb_feed3.setFont(font6)
        self.lb_feed3.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lb_feed3, 1, 0, 1, 1)

        self.ipinfo_feed3 = QLabel(self.groupBox_6)
        self.ipinfo_feed3.setObjectName(u"ipinfo_feed3")
        sizePolicy.setHeightForWidth(self.ipinfo_feed3.sizePolicy().hasHeightForWidth())
        self.ipinfo_feed3.setSizePolicy(sizePolicy)
        self.ipinfo_feed3.setFont(font5)
        self.ipinfo_feed3.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.ipinfo_feed3, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.groupBox_8 = QGroupBox(self.SubFeed_box)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_9 = QGridLayout(self.groupBox_8)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.ipinfo_feed4 = QLabel(self.groupBox_8)
        self.ipinfo_feed4.setObjectName(u"ipinfo_feed4")
        sizePolicy.setHeightForWidth(self.ipinfo_feed4.sizePolicy().hasHeightForWidth())
        self.ipinfo_feed4.setSizePolicy(sizePolicy)
        self.ipinfo_feed4.setFont(font5)
        self.ipinfo_feed4.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.ipinfo_feed4, 0, 0, 1, 1)

        self.lb_feed4 = QLabel(self.groupBox_8)
        self.lb_feed4.setObjectName(u"lb_feed4")
        self.lb_feed4.setFont(font6)
        self.lb_feed4.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.lb_feed4, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_8)


        self.gridLayout_4.addWidget(self.SubFeed_box, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.MainBody_box, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1103, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.MainHeader_box.setTitle(QCoreApplication.translate("MainWindow", u"Header", None))
        self.header_left.setTitle("")
        self.hdleft_label.setText(QCoreApplication.translate("MainWindow", u"CCTV:", None))
        self.hdleft_btnbox.setTitle("")
        self.add_btn.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.remove_btn.setText(QCoreApplication.translate("MainWindow", u"REMOVE", None))
        self.header_right.setTitle("")
        self.hdr_timelabel.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.header_time.setText(QCoreApplication.translate("MainWindow", u"1:11", None))
        self.hdr_datelabel.setText(QCoreApplication.translate("MainWindow", u"Date:", None))
        self.header_date.setText(QCoreApplication.translate("MainWindow", u"October 26, 2024", None))
        self.header_bbox.setTitle("")
        self.MainBody_box.setTitle("")
        self.MainFeed_box.setTitle(QCoreApplication.translate("MainWindow", u"Main Feed", None))
        self.ipinfo_feed1.setText(QCoreApplication.translate("MainWindow", u"IP LOCATION", None))
        self.lb_feed1.setText(QCoreApplication.translate("MainWindow", u"FEED 1", None))
        self.SubFeed_box.setTitle(QCoreApplication.translate("MainWindow", u"Sub-Feed", None))
        self.groupBox_7.setTitle("")
        self.ipinfo_feed2.setText(QCoreApplication.translate("MainWindow", u"IP LOCATION", None))
        self.lb_feed2.setText(QCoreApplication.translate("MainWindow", u"FEED 2", None))
        self.groupBox_6.setTitle("")
        self.lb_feed3.setText(QCoreApplication.translate("MainWindow", u"FEED 3", None))
        self.ipinfo_feed3.setText(QCoreApplication.translate("MainWindow", u"IP LOCATION", None))
        self.groupBox_8.setTitle("")
        self.ipinfo_feed4.setText(QCoreApplication.translate("MainWindow", u"IP LOCATION", None))
        self.lb_feed4.setText(QCoreApplication.translate("MainWindow", u"FEED 4", None))
    # retranslateUi

