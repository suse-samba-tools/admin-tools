import unittest
import hecate
from time import sleep
from common import AdminToolsTestCase, randomName
from getpass import getpass

class TestDNS(AdminToolsTestCase):
    def __open_dns(self):
        if not self.creds.get_password():
            self.creds.set_password(getpass('\nPassword for %s: ' % self.creds.get_username()))
        self.assertSeen('Administrative Tools')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('DNS Manager')
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('Connect to DNS Server...')
        self.press('Enter')
        self.assertSeen('Connect to DNS Server\s')
        self.press('Tab')
        self.press('Enter')
        self.press(self.creds.get_domain())
        self.press('Tab')
        self.press('Enter')
        self.assertSeen('To continue, type an Active Directory administrator password')
        for _ in range(0, 50):
            self.press('BSpace')
        self.press(self.creds.get_username())
        self.press('Tab')
        self.press(self.creds.get_password())
        for _ in range(0, 3):
            self.press('BTab')
        self.press('Enter') # OK
        self.assertSeen('Forward Lookup Zones')

    def test_create_delete_forward_zone(self):
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')

        ### Create a forward lookup zone ###
        fzone_name = ('00000000.%s.com' % randomName(10)).lower()
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('New Zone...')
        self.press('Enter')
        self.assertSeen('New Zone Wizard')
        self.press(fzone_name)
        self.press('Tab')
        self.press('Enter') # Finish
        self.assertSeen('Zone %s created successfully' % fzone_name)
        self.press('Enter') # Ok
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Space') # Expand Forward Lookup Zones
        self.press('Down')
        self.assertSeen(fzone_name)

        ### Delete a forward lookup zone ###
        self.press('BTab')
        self.press('Enter') # Action
        for _ in range(0, 5):
            self.press('Down')
        self.assertSeen('│Delete\s*│')
        self.press('Enter')
        self.assertSeen('Do you want to delete the zone %s from the server?' % fzone_name)
        self.press('Enter') # Yes
        self.assertSeen('Zone %s deleted successfully' % fzone_name)
        self.press('Enter') # Ok
        sleep(3)
        for _ in range(0, 3):
            self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Space')
        sleep(1)
        self.assertNotSeen(fzone_name)
