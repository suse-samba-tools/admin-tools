import unittest
import hecate
import random
import string
from time import sleep
from common import AdminToolsTestCase

def randomName(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length)).title()

class TestADUC(AdminToolsTestCase):
    def setUp(self):
        super(TestADUC, self).setUp()
        self.at = hecate.Runner("admin-tools", width=120, height=50)
        self.assertSeen('Administrative Tools', timeout=10)
        self.at.press('Enter')
        self.assertSeen('To continue, type an Active Directory administrator password', timeout=10)
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Enter')
        self.assertSeen('Active Directory Users and Computers', timeout=10)
        for _ in range(0, 50): # Select Users
            self.at.press('Down')
        # Make sure we see the Administrator in the Users list
        self.assertSeen('Administrator', timeout=10)

    def test_create_delete_group(self):
        # Open the Action Menu
        self.at.press('BTab')
        self.at.press('Enter')
        self.assertSeen('│New', timeout=10)
        # Select New
        self.at.press('Down')
        self.at.press('Enter')
        # Select Group
        self.assertSeen('│Group', timeout=10)
        for _ in range(0, 2):
            self.at.press('Down')
        self.at.press('Enter')
        self.assertSeen('New Object - Group')

        # Group name, etc
        gname = '00000000%s' % randomName(5)
        self.at.press(gname)
        self.at.press('Tab')
        self.at.press(gname)
        self.at.press('BTab')
        self.at.press('BTab')
        self.at.press('BTab')
        self.at.press('Enter')

        self.assertSeen(gname, 'Group not found')

        # Delete the group
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Down')
        self.at.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.at.press('Down')
        self.at.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % gname)
        self.at.press('Enter') # Yes
        self.assertNotSeen(gname, 'Group found after deletion!')

    def test_create_delete_user(self):
        # Open the Action Menu
        self.at.press('BTab')
        self.at.press('Enter')
        self.assertSeen('│New', timeout=10)
        # Select New
        self.at.press('Down')
        self.at.press('Enter')
        # Select User
        self.assertSeen('│User', timeout=10)
        for _ in range(0, 6):
            self.at.press('Down')
        self.at.press('Enter')
        self.assertSeen('New Object - User')

        # Username, etc
        fname = '00000000%s' % randomName(5)
        ini = randomName(1)
        lname = randomName(8)
        self.at.press(fname)
        self.at.press('Tab')
        self.at.press(ini)
        self.at.press('Tab')
        self.at.press(lname)
        self.at.press('Tab')
        self.at.press(' '.join([fname, ini, lname]))
        uname = ('%s%s' % (fname[0], lname)).lower()
        self.at.press('Tab')
        self.at.press(uname)
        self.at.press('Tab')
        self.at.press(uname)
        self.at.press('Tab')
        self.at.press('Enter') # Next

        self.assertSeen('UID number:')

        # Enter a GID
        self.at.press('Tab')
        self.at.press('1000')
        for _ in range(0, 5):
            self.at.press('Tab')
        self.at.press('Enter') # Next

        self.assertSeen('User must change password at next logon')

        # Enter password, etc
        self.at.press('locDCpass1')
        self.at.press('Tab')
        self.at.press('locDCpass1')
        self.at.press('Tab')
        self.at.press('Space') # Uncheck User must change password
        self.at.press('Tab')
        self.at.press('Space') # Check Password never expires
        self.at.press('Tab')
        # Do not disable the account
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Enter') # Click finish

        self.assertSeen(' '.join([fname, ini, lname]), 'User not found')

        # Delete the user
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Down')
        self.at.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.at.press('Down')
        self.at.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % ' '.join([fname, ini, lname]))
        self.at.press('Enter') # Yes
        self.assertNotSeen(' '.join([fname, ini, lname]), 'User found after deletion!')

    def test_create_delete_ou(self):
        # Highlight the domain
        for _ in range(0, 50):
            self.at.press('Up')
        self.at.press('Tab')
        self.at.press('Tab')

        # Open the Action Menu
        self.at.press('BTab')
        self.at.press('Enter')
        self.assertSeen('│New', timeout=10)
        # Select New
        self.at.press('Down')
        self.at.press('Enter')
        # Select Organizational Unit
        self.assertSeen('│Organizational Unit', timeout=10)
        for _ in range(0, 5):
            self.at.press('Down')
        self.at.press('Enter')
        self.assertSeen('New Object - Organizationalunit')

        # Provide an OU name
        name = '00000000%s' % randomName(10)
        self.at.press(name)
        self.at.press('Tab')
        self.at.press('Enter')

        self.assertSeen(name, 'OU not found')

        # Delete the OU
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Down')
        self.at.press('Up')
        self.at.press('Tab')
        self.at.press('Tab')
        self.at.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.at.press('Down')
        self.at.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % name)
        self.at.press('Enter') # Yes
        self.assertNotSeen(name, 'OU found after deletion!')

    def tearDown(self):
        self.at.shutdown()

if __name__ == "__main__":
    unittest.main()
