import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from pydrive2.auth import GoogleAuth
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from GUI.main_window import Main_Window
from GUI.login_window import Ui_Login_Window
from Database.PinguinDB import PinguinDB
from Functions.google_client import GoogleClient
from Functions.trello_api.task_card import Trello

class Login_Window(QMainWindow):
	def __init__(self, login_signal, db, trello):
		super(QMainWindow, self).__init__()
		self.ui = Ui_Login_Window(login_signal, db, trello)
		self.ui.set_up_ui(self)


# This is the main menu window that appears after login is successful
# The default constructor will setup and instance of a Main Window set with the appropriate tabs
class Main_Menu(QMainWindow):
	def __init__(self, db, trello, google):
		super(QMainWindow, self).__init__()
		self.ui = Main_Window(db, trello, google)
		self.ui.setupUi(self)




# This is the driver class responsible for running the application
# Default constructor will build the other UIs needed
# To run the application use member function run
class Pinguin(QMainWindow):
	login_signal = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.db = PinguinDB()
		self.trello = Trello()
		self.auth = None
		self.google_client = GoogleClient()
		self.login_signal.connect(self.login_success)
		self.login_menu = Login_Window(self.login_signal, self.db, self.trello)
		self.main_window = Main_Menu(self.db, self.trello, self.google_client)

		#self.mutex = QMutex()

	@pyqtSlot()
	def login_success(self):
		self.main_window.show()
		self.login_menu.close()
		if self.trello.client == None:
			print("setting up trello client")
			print(self.db.user.user_id)
			self.trello.action_setup2(self.db.user.user_id)
			print("trello client all set")

		print("setting up google auth")
		#print(self.main_window.ui.google_client)
		self.auth = GoogleAuth()
		#print(auth)
		# Try to load saved client credentials
		self.auth.LoadCredentialsFile("Credentials.json")


		if self.auth.credentials is None:
			print("no creds")
			# Authenticate if they're not there
			self.auth.LocalWebserverAuth()

		elif self.auth.access_token_expired:
			print("creds expired")
			# Refresh them if expired
			self.auth.LocalWebserverAuth()
			#self.auth.Refresh()

			print("creds renewed")

		else:
			print("new creds")
			# Initialize the saved creds
			self.auth.Authorize()

		# Save the current credentials to a file
		#self.auth.SaveCredentialsFile("Credentials.json")
		print("authorization complete")

		self.google_client.set_client(self.auth)
		self.main_window.ui.google_client = self.google_client
		#print(self.main_window.ui.google_client)
		#self.main_window.ui.set_google_client(GoogleClient(self.auth))
		#self.main_window.show()
		print("heresdasd")
		self.main_window.ui.widgets_refresh()
		self.main_window.ui.widgets_timer.start(30000)


	def run(self):
		self.login_menu.show()

###############################################################################

def main():
	app = QApplication(sys.argv)
	ui = Pinguin()
	ui.run()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
