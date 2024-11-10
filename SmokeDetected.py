#SmokeDetected.py
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Smoke_Detected.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(700, 500)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.SDetect_message = QLabel(Dialog)
        self.SDetect_message.setObjectName(u"SDetect_message")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SDetect_message.sizePolicy().hasHeightForWidth())
        self.SDetect_message.setSizePolicy(sizePolicy)
        self.SDetect_message.setMinimumSize(QSize(0, 100))
        font = QFont()
        font.setPointSize(24)
        self.SDetect_message.setFont(font)
        self.SDetect_message.setStyleSheet(u"#SDetect_message{\n"
"	color: rgba(237, 112, 39, 1);\n"
"}")
        self.SDetect_message.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.SDetect_message, 1, 0, 1, 1)

        self.SDetect_header = QLabel(Dialog)
        self.SDetect_header.setObjectName(u"SDetect_header")
        sizePolicy.setHeightForWidth(self.SDetect_header.sizePolicy().hasHeightForWidth())
        self.SDetect_header.setSizePolicy(sizePolicy)
        self.SDetect_header.setMinimumSize(QSize(0, 200))
        font1 = QFont()
        font1.setPointSize(36)
        font1.setBold(True)
        self.SDetect_header.setFont(font1)
        self.SDetect_header.setStyleSheet(u"#SDetect_header{\n"
"	color:rgba(0, 9, 73, 1);\n"
"}")
        self.SDetect_header.setAlignment(Qt.AlignCenter)
        self.SDetect_header.setWordWrap(True)

        self.gridLayout.addWidget(self.SDetect_header, 0, 0, 1, 1)

        self.sd_btnbox = QGroupBox(Dialog)
        self.sd_btnbox.setObjectName(u"sd_btnbox")
        self.sd_btnbox.setStyleSheet(u"#sd_btnbox{\n"
"	border: none;\n"
"}")
        self.gridLayout_2 = QGridLayout(self.sd_btnbox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sd_yes = QPushButton(self.sd_btnbox)
        self.sd_yes.setObjectName(u"sd_yes")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sd_yes.sizePolicy().hasHeightForWidth())
        self.sd_yes.setSizePolicy(sizePolicy1)
        self.sd_yes.setMinimumSize(QSize(250, 50))
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        self.sd_yes.setFont(font2)
        self.sd_yes.setStyleSheet(u"#sd_yes{\n"
"\n"
"    border-radius: 5px;\n"
"	background-color: rgba(0, 9, 73, 1);\n"
"	color: white;\n"
"}\n"
"\n"
"#sd_yes:hover {\n"
"	background-color:rgba(0, 9, 73, 0.69);\n"
"}")

        self.gridLayout_2.addWidget(self.sd_yes, 0, 0, 1, 1)

        self.sd_no = QPushButton(self.sd_btnbox)
        self.sd_no.setObjectName(u"sd_no")
        sizePolicy1.setHeightForWidth(self.sd_no.sizePolicy().hasHeightForWidth())
        self.sd_no.setSizePolicy(sizePolicy1)
        self.sd_no.setMinimumSize(QSize(250, 50))
        self.sd_no.setFont(font2)
        self.sd_no.setStyleSheet(u"#sd_no{\n"
"\n"
"    border-radius: 5px;\n"
"	background-color: rgba(0, 9, 73, 1);\n"
"	color: white;\n"
"}\n"
"\n"
"#sd_no:hover {\n"
"	background-color:rgba(0, 9, 73, 0.69);\n"
"}")

        self.gridLayout_2.addWidget(self.sd_no, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.sd_btnbox, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.SDetect_message.setText(QCoreApplication.translate("Dialog", u"Would you like\n"
"to send a report to BFP?", None))
        self.SDetect_header.setText(QCoreApplication.translate("Dialog", u"A Smoke has been Detected!", None))
        self.sd_btnbox.setTitle("")
        self.sd_yes.setText(QCoreApplication.translate("Dialog", u"YES", None))
        self.sd_no.setText(QCoreApplication.translate("Dialog", u"NO", None))
    # retranslateUi

