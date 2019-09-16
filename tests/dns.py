import unittest
import hecate
from time import sleep
from common import AdminToolsTestCase, randomName
from getpass import getpass
from random import randint
from SambaToolDnsAPI import zonelist, query, add_record, delete_record, delete_zone, create_zone, update_record

class TestDNS(AdminToolsTestCase):
    def __open_dns(self):
        password = self.get_password()
        self.assertSeen('Administrative Tools')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('DNS Manager')
        self.press('BTab')
        sleep(1)
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
        self.press(password)
        for _ in range(0, 3):
            self.press('BTab')
        self.press('Enter') # OK
        self.assertSeen('Forward Lookup Zones')

    def __select_zone(self, name):
        timeout = 0
        while timeout < 50:
            self.press('Down')
            self.press('Tab')
            self.press('Enter')
            self.press('BTab')
            if '%s Properties' % name in self.at.screenshot():
                break
            self.press('Enter') # Cancel
            self.press('BTab')
            timeout += 1
        self.press('Enter') # Cancel
        self.press('BTab')
        self.press('Up')
        self.press('Down')

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
        self.__select_zone(fzone_name)
        self.assertSeen(fzone_name)
        results = zonelist(self.creds.get_domain(), self.creds.get_username(), self.creds.get_password())
        self.assertIn(fzone_name, results.keys())

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
        results = zonelist(self.creds.get_domain(), self.creds.get_username(), self.creds.get_password())
        self.assertNotIn(fzone_name, results.keys())

    def test_create_delete_reverse_zone(self):
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 3):
            self.press('Down')

        ### Create a reverse lookup zone ###
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('New Zone...')
        self.press('Enter')
        self.assertSeen('New Zone Wizard')
        self.assertSeen('\(x\) IPv4 Reverse Lookup Zone')
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Next
        self.assertSeen('\(x\) Network ID:')
        self.press('Tab')
        ip1 = randint(1, 254)
        self.press('%d' % ip1)
        self.press('Tab')
        ip2 = randint(1, 254)
        self.press('%d' % ip2)
        self.press('Tab')
        ip3 = randint(1, 254)
        self.press('%d' % ip3)
        rzone_name = '%d.%d.%d.in-addr.arpa' % (ip3, ip2, ip1)
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Finish
        self.assertSeen('Zone %s created successfully' % rzone_name)
        self.press('Enter') # Ok
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Space')
        self.assertSeen('[├└]──%s' % rzone_name)
        results = zonelist(self.creds.get_domain(), self.creds.get_username(), self.creds.get_password())
        self.assertIn(rzone_name, results.keys())

        ### Delete a reverse lookup zone ###
        self.__select_zone(rzone_name)
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('│Delete\s*│')
        for _ in range(0, 4):
            self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete the zone %s from the server?' % rzone_name)
        self.press('Enter') # Yes
        self.assertSeen('Zone %s deleted successfully' % rzone_name)
        self.press('Enter') # Ok
        sleep(3)
        for _ in range(0, 3):
            self.press('Tab')
        for _ in range(0, 3):
            self.press('Down')
        self.press('Space')
        sleep(1)
        self.assertNotSeen(rzone_name)
        results = zonelist(self.creds.get_domain(), self.creds.get_username(), self.creds.get_password())
        self.assertNotIn(rzone_name, results.keys())
