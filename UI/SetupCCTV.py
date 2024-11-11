#SetupCCTV.py
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetupCCTV.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(700, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(700, 600))
        Dialog.setSizeGripEnabled(False)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.blank_Box = QGroupBox(Dialog)
        self.blank_Box.setObjectName(u"blank_Box")
        sizePolicy.setHeightForWidth(self.blank_Box.sizePolicy().hasHeightForWidth())
        self.blank_Box.setSizePolicy(sizePolicy)
        self.blank_Box.setMaximumSize(QSize(16777215, 100))
        self.blank_Box.setStyleSheet(u"#blank_Box{\n"
"	border: none;\n"
"}")

        self.gridLayout.addWidget(self.blank_Box, 5, 0, 1, 2)

        self.btn_box = QGroupBox(Dialog)
        self.btn_box.setObjectName(u"btn_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_box.sizePolicy().hasHeightForWidth())
        self.btn_box.setSizePolicy(sizePolicy1)
        self.btn_box.setMinimumSize(QSize(100, 100))
        self.btn_box.setMaximumSize(QSize(700, 300))
        self.btn_box.setLayoutDirection(Qt.LeftToRight)
        self.btn_box.setStyleSheet(u"#btn_box{\n"
"	border: none;\n"
"}\n"
"")
        self.btn_box.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.horizontalLayout = QHBoxLayout(self.btn_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.pbtn_submit = QPushButton(self.btn_box)
        self.pbtn_submit.setObjectName(u"pbtn_submit")
        self.pbtn_submit.setMaximumSize(QSize(200, 50))
        font = QFont()
        font.setFamilies([u"MS Sans Serif"])
        font.setPointSize(12)
        font.setBold(True)
        self.pbtn_submit.setFont(font)
        self.pbtn_submit.setStyleSheet(u"#pbtn_submit{\n"
"\n"
"    border-radius: 5px;\n"
"	background-color: rgba(0, 9, 73, 1);\n"
"	color: white;\n"
"}\n"
"\n"
"#pbtn_submit:hover {\n"
"	background-color:rgba(0, 9, 73, 0.69);\n"
"}")

        self.horizontalLayout.addWidget(self.pbtn_submit)


        self.gridLayout.addWidget(self.btn_box, 4, 0, 1, 2)

        self.form_box = QGroupBox(Dialog)
        self.form_box.setObjectName(u"form_box")
        sizePolicy1.setHeightForWidth(self.form_box.sizePolicy().hasHeightForWidth())
        self.form_box.setSizePolicy(sizePolicy1)
        self.form_box.setMaximumSize(QSize(700, 400))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.form_box.setFont(font1)
        self.form_box.setStyleSheet(u"#form_box{\n"
"	border: none;\n"
"	margin-top:50px;\n"
"}\n"
"\n"
"#form_box QLineEdit {\n"
"    border: 1px solid gray;\n"
"	height: 30px;\n"
"	border-radius: 5px;\n"
"}\n"
"")
        self.form_box.setAlignment(Qt.AlignCenter)
        self.form_box.setFlat(False)
        self.form_box.setCheckable(False)
        self.formLayout = QFormLayout(self.form_box)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setContentsMargins(50, 80, 90, 10)
        self.label_ip = QLabel(self.form_box)
        self.label_ip.setObjectName(u"label_ip")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        font2.setBold(False)
        self.label_ip.setFont(font2)
        self.label_ip.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_ip)

        self.lineEdit_ip = QLineEdit(self.form_box)
        self.lineEdit_ip.setObjectName(u"lineEdit_ip")
        self.lineEdit_ip.setFont(font2)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_ip)

        self.label_usern = QLabel(self.form_box)
        self.label_usern.setObjectName(u"label_usern")
        self.label_usern.setFont(font2)
        self.label_usern.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_usern)

        self.lineEdit_usern = QLineEdit(self.form_box)
        self.lineEdit_usern.setObjectName(u"lineEdit_usern")
        self.lineEdit_usern.setFont(font2)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_usern)

        self.label_pass = QLabel(self.form_box)
        self.label_pass.setObjectName(u"label_pass")
        self.label_pass.setFont(font2)
        self.label_pass.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_pass)

        self.lineEdit_pass = QLineEdit(self.form_box)
        self.lineEdit_pass.setObjectName(u"lineEdit_pass")
        self.lineEdit_pass.setFont(font2)
        self.lineEdit_pass.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_pass)

        self.label_ccloc = QLabel(self.form_box)
        self.label_ccloc.setObjectName(u"label_ccloc")
        self.label_ccloc.setFont(font2)
        self.label_ccloc.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_ccloc)

        self.lineEdit_ccloc = QLineEdit(self.form_box)
        self.lineEdit_ccloc.setObjectName(u"lineEdit_ccloc")
        self.lineEdit_ccloc.setFont(font2)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_ccloc)

        self.error_msg = QLabel(self.form_box)
        self.error_msg.setObjectName(u"error_msg")
        self.error_msg.setStyleSheet(u"#error_msg{\n"
"	color: red;\n"
"}")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.error_msg)


        self.gridLayout.addWidget(self.form_box, 0, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.blank_Box.setTitle("")
        self.btn_box.setTitle("")
        self.pbtn_submit.setText(QCoreApplication.translate("Dialog", u"SUBMIT", None))
        self.form_box.setTitle(QCoreApplication.translate("Dialog", u"CCTV SETUP", None))
        self.label_ip.setText(QCoreApplication.translate("Dialog", u"IP:", None))
        self.label_usern.setText(QCoreApplication.translate("Dialog", u"Username:", None))
        self.label_pass.setText(QCoreApplication.translate("Dialog", u"Password:", None))
        self.label_ccloc.setText(QCoreApplication.translate("Dialog", u"CCTV Location:", None))
        self.error_msg.setText(QCoreApplication.translate("Dialog", u"Warning Message!", None))
    # retranslateUi

