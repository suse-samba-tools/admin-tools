import unittest
import hecate
from time import sleep
from common import AdminToolsTestCase, randomName

class TestADUC(AdminToolsTestCase):
    def __open_aduc(self):
        self.assertSeen('Administrative Tools')
        self.press('Down')
        self.press('Enter')
        self.assertSeen('ADSI Edit')
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('Connect to...')
        self.press('Enter')
        for _ in range(0, 5):
            self.press('Tab')
        self.press('Space')
        self.press('Tab')
        self.press(self.creds.get_domain())
        for _ in range(0, 8):
            self.press('BTab')
        self.press('Enter') # OK
        self.assertSeen('To continue, type an Active Directory administrator password')
        for _ in range(0, 50): # Delete current username
            self.press('BSpace')
        self.press(self.creds.get_username())
        self.press('Tab')
        self.press(self.get_password())
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Default naming context')

    def test_authentication(self):
        self.__open_aduc()
