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
        sleep(3)
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

    def test_create_delete_host_pointer_records(self):
        fzone_name = ('00000000.%s.com' % randomName(10)).lower()
        create_zone(self.creds.get_domain(), fzone_name, self.creds.get_username(), self.creds.get_password())
        self.zones.append(fzone_name)
        ip1 = randint(1, 254)
        ip2 = randint(1, 254)
        ip3 = randint(1, 254)
        rzone_name = '%d.%d.%d.in-addr.arpa' % (ip3, ip2, ip1)
        create_zone(self.creds.get_domain(), rzone_name, self.creds.get_username(), self.creds.get_password())
        self.zones.append(rzone_name)
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Space') # Expand Forward Lookup Zones
        self.__select_zone(fzone_name)

        ### Create Host/Pointer records ###
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('│New Host \(A or AAAA\)\.\.\.\s*│')
        self.press('Enter') # New Host
        self.assertSeen('Name \(uses parent domain name if blank\):')
        name = '00000000%s' % randomName(10)
        self.press(name)
        self.press('Tab')
        ip4 = randint(1,254)
        ip_addr = '%d.%d.%d.%d' % (ip1, ip2, ip3, ip4)
        self.press(ip_addr)
        self.press('Tab')
        self.press('Space')
        self.assertSeen('\[x\] Create associated pointer \(PTR\) record')
        self.press('Tab')
        self.press('Enter') # Add Host
        self.assertSeen('Record added successfully')
        self.press('Enter') # Ok
        self.assertSeen('%s\s*│Host \(A\)\s*│%s' % (name, ip_addr))
        ### Delete Host record ###
        self.press('Up')
        self.press('Down')
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Action
        self.assertSeen('│Delete\s*│')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete the record %s from the server?' % name)
        self.press('Enter') # Yes
        self.assertSeen('Record deleted successfully')
        self.press('Enter') # Ok
        ### Verify deletion of Pointer record ###
        sleep(3)
        self.press('BTab')
        timeout = 0
        while timeout < 50:
            self.press('Down')
            if '%s│\s*│' % ip_addr in self.at.screenshot():
                break
            timeout+=1
        self.press('Space')
        self.assertSeen('[└├]──%s' % rzone_name)
        timeout = 0
        while timeout < 50:
            self.press('Down')
            self.assertNotSeen(ip_addr)
            timeout+=1

    def test_create_delete_cname_record(self):
        fzone_name = ('00000000.%s.com' % randomName(10)).lower()
        create_zone(self.creds.get_domain(), fzone_name, self.creds.get_username(), self.creds.get_password())
        self.zones.append(fzone_name)
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Space') # Expand Forward Lookup Zones
        self.__select_zone(fzone_name)

        ### Create CNAME record ###
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('│New Alias \(CNAME\)\.\.\.\s*│')
        self.press('Down')
        self.press('Enter') # New Alias
        self.assertSeen('New Resource Record')
        self.press('Tab')
        alias = '00000000%s' % randomName(10)
        self.press(alias)
        self.press('Tab')
        self.press(self.creds.get_domain().lower())
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Record added successfully')
        self.press('Enter') # Ok
        self.assertSeen('│%s\s*│Alias \(CNAME\)\s*│%s\.\s*│' % (alias, self.creds.get_domain().lower()))

        ### Delete CNAME record ###
        self.press('Up')
        self.press('Down')
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Action
        self.assertSeen('│Delete\s*│')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete the record %s from the server\?' % alias)
        self.press('Enter') # Yes
        self.assertSeen('Record deleted successfully')
        self.press('Enter') # Ok
        sleep(3)
        self.assertNotSeen(alias)

    def test_create_delete_mx_record(self):
        fzone_name = ('00000000.%s.com' % randomName(10)).lower()
        create_zone(self.creds.get_domain(), fzone_name, self.creds.get_username(), self.creds.get_password())
        self.zones.append(fzone_name)
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Space') # Expand Forward Lookup Zones
        self.__select_zone(fzone_name)

        ### Create MX record ###
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('│New Mail Exchanger \(MX\)\.\.\.\s*│')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Enter') # New Mail Exchanger
        self.assertSeen('New Resource Record')
        self.press('Tab')
        mx = '00000000%s' % randomName(10)
        self.press(mx)
        self.press('Tab')
        self.press(self.creds.get_domain().lower())
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Record added successfully')
        self.press('Enter') # Ok
        self.assertSeen('│%s\s*│Mail Exchanger \(MX\)\s*│\[10\] %s\.\s*│' % (mx, self.creds.get_domain().lower()))

        ### Delete MX record ###
        self.press('Up')
        self.press('Down')
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Action
        self.assertSeen('│Delete\s*│')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete the record %s from the server\?' % mx)
        self.press('Enter') # Yes
        self.assertSeen('Record deleted successfully')
        self.press('Enter') # Ok
        sleep(3)
        self.assertNotSeen(mx)

    def test_create_delete_txt_record(self):
        fzone_name = ('00000000.%s.com' % randomName(10)).lower()
        create_zone(self.creds.get_domain(), fzone_name, self.creds.get_username(), self.creds.get_password())
        self.zones.append(fzone_name)
        self.__open_dns()
        self.press('Tab')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Space') # Expand Forward Lookup Zones
        self.__select_zone(fzone_name)

        ### Create the TXT record ###
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('Other New Records...')
        for _ in range(0, 4):
            self.press('Down')
        self.press('Enter') # Other New Records
        self.assertSeen('New Resource Record Type')
        for _ in range(0, 5):
            self.press('Down') # Text (TXT)
        self.press('Tab')
        self.press('Enter') # Create Record
        self.assertSeen('Record name')
        self.press('Tab')
        rname = randomName(10)
        self.press(rname)
        self.press('Tab')
        rtext = ' '.join([randomName(5) for _ in range(0, 4)])
        self.press(rtext)
        self.press('Tab')
        self.press('Enter') # OK
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Done
        self.assertSeen('Record added successfully')
        self.press('Enter') # Ok

        ### Verify the TXT record ###
        self.press('Enter') # Record Properties
        self.assertSeen('%s Properties' % rname)
        self.assertSeen(rtext)
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Enter') # Cancel

        ### Delete the TXT record ###
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Action
        self.assertSeen('Delete')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete the record %s from the server?' % rname)
        self.press('Enter') # Yes
        self.assertSeen('Record deleted successfully')
        self.press('Enter') # Ok
        self.assertNotSeen(rname)

    def setUp(self):
        super(TestDNS, self).setUp()
        self.zones = []

    def tearDown(self):
        for zone in self.zones:
            delete_zone(self.creds.get_domain(), zone, self.creds.get_username(), self.creds.get_password())
        super(TestDNS, self).tearDown()
