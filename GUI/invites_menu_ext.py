from GUI.Uis.Invite_Menu_Ui.invites_menu import Ui_invites_menu

class invites_menu_ext(Ui_invites_menu):
    def __init__(self, signal, main_window):
        super().__init__()
        self.signal = signal
        self.main_window = main_window

    def setupUi(self, invites_menu):
        super().setupUi(invites_menu)
        self.invites_menu = invites_menu


        self.invites_error_frame.hide()
        self.invites_error_button.clicked.connect(self.error_hide)

        self.send_invites_button.clicked.connect(self.send_invites)
        self.cancel_invites_button.clicked.connect(self.cancel)

    def error_hide(self):
        self.invites_error_frame.hide()

    def error_show(self):
        self.invites_error_frame.show()

    def send_invites(self):
        emails = self.send_invites_edit.toPlainText().split(',')
        print(emails)
        if len(emails) <= 1 and emails[0] == '':
            print("here")
            error_text = "Enter emails to invite"
            self.invites_error_label.setText(error_text)
            self.invites_error_frame.show()

        else:
            print("here2")
            self.main_window.send_invites(emails)
            self.cancel()


    def cancel(self):
        self.invites_menu.close()
