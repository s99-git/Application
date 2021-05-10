# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:03:37 2021

@author: Sam
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from .trello_pin_window import *

from trello import TrelloClient
from Functions.trello_api.ping_authorization import *
from os import path
import ast



class Ui_Login_Window(QtWidgets.QMainWindow):
    #
    # STYLES
    #
    styleLineEditOk = ("QLineEdit {\n"
                       "    border: 2px solid rgb(45, 45, 45);\n"
                       "    border-radius: 5px;\n"
                       "    padding: 15px;\n"
                       "    background-color: rgb(30, 30, 30);    \n"
                       "    color: rgb(100, 100, 100);\n"
                       "}\n"
                       "QLineEdit:hover {\n"
                       "    border: 2px solid rgb(55, 55, 55);\n"
                       "}\n"
                       "QLineEdit:focus {\n"
                       "    border: 2px solid rgb(255, 207, 0);    \n"
                       "    color: rgb(200, 200, 200);\n"
                       "}")

    styleLineEditError = ("QLineEdit {\n"
                          "    border: 2px solid rgb(255, 85, 127);\n"
                          "    border-radius: 5px;\n"
                          "    padding: 15px;\n"
                          "    background-color: rgb(30, 30, 30);    \n"
                          "    color: rgb(100, 100, 100);\n"
                          "}\n"
                          "QLineEdit:hover {\n"
                          "    border: 2px solid rgb(55, 55, 55);\n"
                          "}\n"
                          "QLineEdit:focus {\n"
                          "    border: 2px solid rgb(255, 207, 0);    \n"
                          "    color: rgb(200, 200, 200);\n"
                          "}")

    stylePopupError = ("background-color: rgb(207, 138, 0); border-radius: 5px;")
    stylePopupOk = ("background-color: rgb(207, 138, 0); border-radius: 5px;")

    def __init__(self, login_signal,db, trello):
        super(QtWidgets.QMainWindow, self).__init__()
        self.login_signal = login_signal
        self.db = db
        self.trello = trello

    def login_success(self):
        self.login_signal.emit()

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Pinguin"))
        self.label_error.setText(_translate("login_window", "Error"))
        self.lineEdit_user.setPlaceholderText(_translate("login_window", "USER"))
        self.lineEdit_password.setPlaceholderText(_translate("login_window", "PASSWORD"))
        self.checkBox_save_user.setText(_translate("login_window", "SAVE USER"))
        self.pushButton_login.setText(_translate("login_window", "Login"))
        self.pushButton_create.setText(_translate("login_window", "Create Account"))

    #   self.label_credits.setText(_translate("login_window", "Created by: Wanderson M. Pimenta"))

    @pyqtSlot()
    def create_account(self):
        self.acct_window = QtWidgets.QMainWindow(self)
        self.acct_window.setStyleSheet("QWidget {\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n")
        self.acct_window.resize(300, 300)
        self.acct_window.setWindowTitle("Pinguin")
        self.acct_window.setWindowIcon(QtGui.QIcon("447logoicon.ico"))

        self.acct_widget = QtWidgets.QWidget()
        self.acct_layout = QtWidgets.QVBoxLayout()
        self.acct_widget.setLayout(self.acct_layout)

        self.acct_label = QtWidgets.QLabel("Create Account")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.acct_label.setFont(font)
        self.acct_label.setAlignment(Qt.AlignCenter)

        self.acct_id_edit = QtWidgets.QLineEdit()
        self.acct_id_edit.setPlaceholderText("user@gmail.com")
        self.acct_id_edit.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 5px;\n"
"    background-color: rgb(30, 30, 30);    \n"
"    color: rgb(255,255,255);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(55, 55, 55);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(207, 138, 0);    \n"
"    color: rgb(255,255,255);\n"
"}")

        self.acct_name_edit = QtWidgets.QLineEdit()
        self.acct_name_edit.setPlaceholderText("Enter First Name")
        self.acct_name_edit.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 5px;\n"
"    background-color: rgb(30, 30, 30);    \n"
"    color: rgb(255,255,255);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(55, 55, 55);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(207, 138, 0);    \n"
"    color: rgb(255,255,255);\n"
"}")

        self.acct_pass_edit = QtWidgets.QLineEdit()
        self.acct_pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.acct_pass_edit.setPlaceholderText("Enter Password")
        self.acct_pass_edit.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 5px;\n"
"    background-color: rgb(30, 30, 30);    \n"
"    color: rgb(255,255,255);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(55, 55, 55);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(207, 138, 0);    \n"
"    color: rgb(255,255,255);\n"
"}")

        self.acct_confirm_pass_edit = QtWidgets.QLineEdit()
        self.acct_confirm_pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.acct_confirm_pass_edit.setPlaceholderText("Confirm Password")
        self.acct_confirm_pass_edit.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 5px;\n"
"    background-color: rgb(30, 30, 30);    \n"
"    color: rgb(255,255,255);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(55, 55, 55);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(207, 138, 0);    \n"
"    color: rgb(255,255,255);\n"
"}")

        self.acct_buttons_widget = QtWidgets.QWidget()
        self.acct_buttons_layout = QtWidgets.QHBoxLayout()
        self.acct_buttons_widget.setLayout(self.acct_buttons_layout)

        self.acct_accept_button = QtWidgets.QPushButton("Create")
        self.acct_accept_button.setStyleSheet("QPushButton {    \n"
"    background-color: rgb(50, 50, 50);\n"
"    border: 2px solid rgb(60, 60, 60);\n"
"    border-radius: 5px;\n"
"    color:white\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 60, 60);\n"
"    border: 2px solid rgb(70, 70, 70);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color:rgb(255, 170, 0);\n"
"    border: 2px solid rgb(207, 138, 0);\n"
"    color: rgb(35, 35, 35);\n"
"}")
        self.acct_accept_button.clicked.connect(self.create_account_accept)

        self.acct_cancel_button = QtWidgets.QPushButton("Cancel")
        self.acct_cancel_button.setStyleSheet("QPushButton {    \n"
"    background-color: rgb(50, 50, 50);\n"
"    border: 2px solid rgb(60, 60, 60);\n"
"    border-radius: 5px;\n"
"    color:white\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 60, 60);\n"
"    border: 2px solid rgb(70, 70, 70);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color:rgb(255, 170, 0);\n"
"    border: 2px solid rgb(207, 138, 0);\n"
"    color: rgb(35, 35, 35);\n"
"}")
        self.acct_cancel_button.clicked.connect(self.create_account_cancel)

        self.acct_buttons_layout.addWidget(self.acct_accept_button)
        self.acct_buttons_layout.addWidget(self.acct_cancel_button)

        self.acct_layout.addWidget(self.acct_label)
        self.acct_layout.addWidget(self.acct_id_edit)
        self.acct_layout.addWidget(self.acct_name_edit)
        self.acct_layout.addWidget(self.acct_pass_edit)
        self.acct_layout.addWidget(self.acct_confirm_pass_edit)
        self.acct_layout.addWidget(self.acct_buttons_widget)

        self.acct_window.setCentralWidget(self.acct_widget)

        self.acct_window.show()

    @pyqtSlot()
    def create_account_accept(self):
        email = self.acct_id_edit.text()
        name = self.acct_name_edit.text()
        password = self.acct_pass_edit.text()
        confirm_password = self.acct_confirm_pass_edit.text()

        if email == '':
            error_text = "Missing an email"

        elif name == '':
            error_text = "Missing first name"

        elif password == '':
            error_text = "Missing a password"

        elif confirm_password == '':
            error_text = "Confirm your password"

        elif email != '' and name+password+confirm_password == '':
            error_text = "Missing name / password / confirm password"

        elif name != '' and email+password+confirm_password == '':
            error_text = "Missing email / password /confirm password"

        elif password != '' and email+name+confirm_password == '':
            error_text = "Missing email / name / confirm password"

        elif confirm_password != '' and email+name+password == '':
            error_text = "Missing email / name / password"

        elif email != '' and name != '' and password+confirm_password == '':
            error_text = "Missing password / confirm password"

        elif email != '' and password != '' and name+confirm_password == '':
            error_text = "Missing name / confirm password"

        elif email != '' and confirm_password != '' and name+password == '':
            error_text = "Missing name / password"

        elif name != '' and password != '' and email+confirm_password == '':
            error_text = "Missing email / confirm password"

        elif name != '' and confirm_password != '' and email+password == '':
            error_text = "Missing email / password"

        elif password != '' and confirm_password != '' and email+name == '':
            error_text = "Missing email / name"

        elif email != '' and name != '' and password != '' and confirm_password == '':
            error_text = "Missing confirm password"

        elif email != '' and name != '' and confirm_password != '' and password == '':
            error_text = "Missing password"

        elif name != '' and password != '' and confirm_password != '' and email == '':
            error_text = "Missing email"

        elif email != '' and password != '' and confirm_password != '' and name == '':
            error_text = "Missing name"

        elif password != confirm_password:
            error_text = "Non-matching passwords"
        else:
            print(self.db.user_lookup_by_email(email))
            if self.db.user_lookup_by_email(email) == 0:
                print('adafa')
                self.trello_pin_window(email)
                print('A')
                self.db.create_account(email, password, name, self.trello.trello_id)
                print('B')
            else:
                error_text = "Email already exists"

    @pyqtSlot()
    def create_account_cancel(self):
        self.acct_window.close()

    def trello_pin_window(self, email):
        self.acct_trello_widget = QtWidgets.QWidget()
        self.acct_trello_window_ui = trello_pin_window_ext(self.trello, email, self.acct_window, self.db)

        self.acct_trello_window_ui.setupUi(self.acct_trello_widget)
        self.acct_window.setCentralWidget(self.acct_trello_widget)



    def enter_trello_pin(self):
        print(self.acct_trello_window_ui.trello_pin_edit.text())

    def send_url(self, url):
        QtGui.QDesktopServices.openUrl(url)

    def checkFields(self):
        textUser = ""
        textPassword = ""

        def showMessage(message):
            self.frame_error.show()
            self.label_error.setText(message)

        # CHECK USER
        if not self.lineEdit_user.text():
            textUser = " User Empty. "
            self.lineEdit_user.setStyleSheet(self.styleLineEditError)
        else:
            textUser = ""
            self.lineEdit_user.setStyleSheet(self.styleLineEditOk)

        # CHECK PASSWORD
        if not self.lineEdit_password.text():
            textPassword = " Password Empty. "
            self.lineEdit_password.setStyleSheet(self.styleLineEditError)
        else:
            textPassword = ""
            self.lineEdit_password.setStyleSheet(self.styleLineEditOk)

        # CHECK FIELDS
        if textUser + textPassword != '':
            text = textUser + textPassword
            showMessage(text)
            self.frame_error.setStyleSheet(self.stylePopupError)

        else:
            text = " Check User/Password. "
            if (self.db.login(self.lineEdit_user.text(), self.lineEdit_password.text())):
                self.login_success()

            if self.checkBox_save_user.isChecked():
                text = text + " | Saver user: OK "

            else:
                showMessage(text)
                self.frame_error.setStyleSheet(self.stylePopupOk)

    def action_setup(self, email):
        # if the config file already exists, use the existing tokens
        if path.exists("pinguin.config"):
            file = open("pinguin.config", "r")
            contents = file.read()
            # convert the file contents to a dictionary
            conf_dict = ast.literal_eval(contents)

            client = TrelloClient(
                api_key='2e0161c01eca7ad03bda843f811dac8b',
                api_secret='d4446e39644f0992f6db9859c77441754f0085ad5725d86699780d1ba86dfeea',
                # token = '3e1c54bc5ae2f18fe2e449c102c49b40400de0b39e2aca401dfc7a028c1ed33e',
                # token_secret = '298b5e59c4c09cff9666ba32fd381c5f'
                token=conf_dict["token"],
                token_secret=conf_dict["token_secret"]
            )
            self.client = client
        else:

            # CHANGE THE INPUT TO THE GUI'S RECIEVED PIN
            provided_pin = input("Enter your pin: ")
            ping_token = ping_oauth_pin(provided_pin)

            user_token = ping_token.get('oauth_token')
            user_token_secret = ping_token.get('oauth_token_secret')

            client = TrelloClient(
                api_key='2e0161c01eca7ad03bda843f811dac8b',
                api_secret='d4446e39644f0992f6db9859c77441754f0085ad5725d86699780d1ba86dfeea',
                # token = '3e1c54bc5ae2f18fe2e449c102c49b40400de0b39e2aca401dfc7a028c1ed33e',
                # token_secret = '298b5e59c4c09cff9666ba32fd381c5f'
                token=user_token,
                token_secret=user_token_secret
            )

            file = open("pinguin.config", "w")
            conf_dict = {"id": email, "token": user_token, "token_secret": user_token_secret}

            file.write(str(conf_dict))
            file.close()

            self.client = client

    def set_up_ui(self, login_window):
        login_window.setObjectName("login_window")
        login_window.resize(500, 700)
        login_window.setMinimumSize(QtCore.QSize(500, 700))
        login_font = QtGui.QFont()
        login_font.setFamily("Segoe UI")
        login_font.setPointSize(12)
        login_window.setFont(login_font)

        login_window.setWindowTitle("Pinguin")
        #login_window.setWindowIcon(QtGui.QIcon("url(:/447logoicon.ico)"))
        login_window.setStyleSheet("color: rgb(200, 200, 200);\n"
                                   "background-color: rgb(100,100,100);")

        self.login_widget = QtWidgets.QWidget(login_window)
        self.login_widget.setObjectName("login_widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.login_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.top_bar = QtWidgets.QFrame(self.login_widget)
        self.top_bar.setMaximumSize(QtCore.QSize(16777215, 35))
        self.top_bar.setStyleSheet("")
        self.top_bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_bar.setObjectName("top_bar")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.top_bar)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.frame_error = QtWidgets.QFrame(self.top_bar)
        self.frame_error.setMaximumSize(QtCore.QSize(450, 16777215))
        self.frame_error.setStyleSheet(self.stylePopupError)
        self.frame_error.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_error.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_error.setObjectName("frame_error")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_error)
        self.horizontalLayout_3.setContentsMargins(10, 3, 10, 3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label_error = QtWidgets.QLabel(self.frame_error)
        self.label_error.setStyleSheet("color: rgb(35, 35, 35);")
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error.setObjectName("label_error")

        self.horizontalLayout_3.addWidget(self.label_error)

        self.pushButton_close_popup = QtWidgets.QPushButton(self.frame_error)
        self.pushButton_close_popup.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_close_popup.setStyleSheet("QPushButton {\n"
                                                  "    border-radius: 5px;    \n"
                                                  "    background-position: center;    \n"
                                                  "    background-color: rgb(60, 60, 60);\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: rgb(50, 50, 50);    \n"
                                                  "    color: rgb(200, 200, 200);\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: rgb(35, 35, 35);    \n"
                                                  "    color: rgb(200, 200, 200);\n"
                                                  "}")
        self.pushButton_close_popup.setText("")
        self.pushButton_close_popup.setObjectName("pushButton_close_popup")
        self.horizontalLayout_3.addWidget(self.pushButton_close_popup)

        self.horizontalLayout_2.addWidget(self.frame_error)
        self.verticalLayout.addWidget(self.top_bar)

        self.content = QtWidgets.QFrame(self.login_widget)
        self.content.setStyleSheet("")
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content.setObjectName("content")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.content)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.login_area = QtWidgets.QFrame(self.content)
        self.login_area.setMaximumSize(QtCore.QSize(450, 550))
        self.login_area.setStyleSheet("border-radius: 10px;")
        self.login_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.login_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.login_area.setObjectName("login_area")

        self.login_area_title = QtWidgets.QLabel("Pinguin", self.login_widget)
        self.login_area_title_font = QtGui.QFont('Trebuchet MS')
        self.login_area_title_font.setPointSize(40)
        self.login_area_title.setFont(self.login_area_title_font)
        self.login_area_title.setAlignment(QtCore.Qt.AlignCenter)
        self.login_area_title.setGeometry(150, 45, 200, 100)
        # self.login_area_title.setGeometry(45, -200, 360, 200)
        # self.login_area_title.setStyleSheet("background-image: url(PinguinTitle.png);\n""background-repeat: no-repeat;\n""background-position: center;")
        # self.login_area_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.login_area_title.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.login_area_title.setObjectName("login_area_title")

        self.logo = QtWidgets.QFrame(self.login_area)
        self.logo.setGeometry(QtCore.QRect(45, -100, 360, 600))
        self.logo.setStyleSheet(
                                "background-repeat: no-repeat;\n"
                                "background-position: center;")
        self.logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo.setObjectName("logo")
        # removed avatar

        self.lineEdit_user = QtWidgets.QLineEdit(self.login_area)
        self.lineEdit_user.setGeometry(QtCore.QRect(85, 288, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit_user.setFont(font)

        self.lineEdit_user.setStyleSheet(self.styleLineEditOk)

        self.lineEdit_user.setMaxLength(32)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_password = QtWidgets.QLineEdit(self.login_area)
        self.lineEdit_password.setGeometry(QtCore.QRect(85, 340, 280, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lineEdit_password.setFont(font)

        self.lineEdit_password.setStyleSheet(self.styleLineEditOk)

        self.lineEdit_password.setMaxLength(16)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")

        self.checkBox_save_user = QtWidgets.QCheckBox(self.login_area)
        self.checkBox_save_user.setGeometry(QtCore.QRect(85, 395, 281, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.checkBox_save_user.setFont(font)
        self.checkBox_save_user.setStyleSheet("QCheckBox::indicator {\n"
                                              "    border: 3px solid rgb(100, 100, 100);\n"
                                              "    width: 15px;\n"
                                              "    height: 15px;\n"
                                              "    border-radius: 10px;    \n"
                                              "    background-color: rgb(135, 135, 135);\n"
                                              "}\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    border: 3px solid rgb(255, 205, 0);\n"
                                              "    background-color: rgb(255, 255, 0);\n"
                                              "}")
        self.checkBox_save_user.setObjectName("checkBox_save_user")

        self.pushButton_login = QtWidgets.QPushButton(self.login_area)
        self.pushButton_login.setGeometry(QtCore.QRect(85, 425, 280, 50))
        self.pushButton_login.setDefault(True)
        QtCore.QTimer.singleShot(0, self.pushButton_login.setFocus)
        self.pushButton_login.setStyleSheet("QPushButton {    \n"
                                            "    background-color: rgb(50, 50, 50);\n"
                                            "    border: 2px solid rgb(60, 60, 60);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "QPushButton:hover {    \n"
                                            "    background-color: rgb(60, 60, 60);\n"
                                            "    border: 2px solid rgb(70, 70, 70);\n"
                                            "}\n"
                                            "QPushButton:pressed {    \n"
                                            "    background-color: rgb(250, 230, 0);\n"
                                            "    border: 2px solid rgb(255, 165, 24);    \n"
                                            "    color: rgb(35, 35, 35);\n"
                                            "}")
        self.pushButton_login.setObjectName("pushButton_login")

        self.horizontalLayout.addWidget(self.login_area)

        self.verticalLayout.addWidget(self.content)

        # added
        self.pushButton_create = QtWidgets.QPushButton(self.login_area)
        self.pushButton_create.setGeometry(QtCore.QRect(85, 480, 280, 50))
        self.pushButton_create.setDefault(True)
        QtCore.QTimer.singleShot(0, self.pushButton_create.setFocus)
        self.pushButton_create.setStyleSheet("QPushButton {    \n"
                                             "    background-color: rgb(50, 50, 50);\n"
                                             "    border: 2px solid rgb(60, 60, 60);\n"
                                             "    border-radius: 5px;\n"
                                             "}\n"
                                             "QPushButton:hover {    \n"
                                             "    background-color: rgb(60, 60, 60);\n"
                                             "    border: 2px solid rgb(70, 70, 70);\n"
                                             "}\n"
                                             "QPushButton:pressed {    \n"
                                             "    background-color: rgb(250, 230, 0);\n"
                                             "    border: 2px solid rgb(255, 165, 24);    \n"
                                             "    color: rgb(35, 35, 35);\n"
                                             "}")
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_create.clicked.connect(self.create_account)

        """self.bottom = QtWidgets.QFrame(self.login_widget)
        self.bottom.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bottom.setStyleSheet("background-color: rgb(15, 15, 15)")
        self.bottom.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom.setObjectName("bottom")"""
        #self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bottom)
        #self.verticalLayout_2.setObjectName("verticalLayout_2")
        #self.label_credits = QtWidgets.QLabel(self.bottom)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        #self.label_credits.setFont(font)
        #self.label_credits.setStyleSheet("color: rgb(75, 75, 75);")
        #self.label_credits.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        #self.label_credits.setObjectName("label_credits")
        #self.verticalLayout_2.addWidget(self.label_credits)
        #self.verticalLayout.addWidget(self.bottom)
        login_window.setCentralWidget(self.login_widget)
        self.menubar = QtWidgets.QMenuBar(login_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 928, 21))
        self.menubar.setObjectName("menubar")
        login_window.setMenuBar(self.menubar)

        self.pushButton_close_popup.clicked.connect(lambda: self.frame_error.hide())

        # HIDE ERROR
        self.frame_error.hide()

        # BT LOGIN
        self.pushButton_login.clicked.connect(self.checkFields)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

        # login_window.show()
