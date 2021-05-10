from .Google_Calendar.gcalendar import *
from .Google_Drive.gDrive import *

class GoogleClient(object):

    def __init__(self):
        self.google_drive = None
        self.google_calendar = None


    def set_client(self, auth):
        self.google_drive = Google_Drive(auth)
        self.google_calendar = Google_Calendar(auth)
