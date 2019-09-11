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
        self.assertSeen('Administrative Tools')
        self.press('Enter')
        self.assertSeen('To continue, type an Active Directory administrator password')
        self.press('Tab')
        self.press('Tab')
        self.press('Enter')
        self.assertSeen('Active Directory Users and Computers')
        for _ in range(0, 50): # Select Users
            self.press('Down')
        # Make sure we see the Administrator in the Users list
        self.assertSeen('Administrator')
        self.assertNotSeen('00000000', 'You need to cleanup a previous failed run!')

    def test_create_delete_group(self):
        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('│New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Group
        self.assertSeen('│Group')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('New Object - Group')

        # Group name, etc
        gname = '00000000%s' % randomName(5)
        self.press(gname)
        self.press('Tab')
        self.press(gname)
        self.press('BTab')
        self.press('BTab')
        self.press('BTab')
        self.press('Enter')

        self.assertSeen(gname, 'Group not found')

        # Delete the group
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % gname)
        self.press('Enter') # Yes
        self.assertNotSeen(gname, 'Group found after deletion!')

    def test_create_delete_user(self):
        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('│New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select User
        self.assertSeen('│User')
        for _ in range(0, 6):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('New Object - User')

        # Username, etc
        fname = '00000000%s' % randomName(5)
        ini = randomName(1)
        lname = randomName(8)
        self.press(fname)
        self.press('Tab')
        self.press(ini)
        self.press('Tab')
        self.press(lname)
        self.press('Tab')
        self.press(' '.join([fname, ini, lname]))
        uname = ('%s%s' % (fname[0], lname)).lower()
        self.press('Tab')
        self.press(uname)
        self.press('Tab')
        self.press(uname)
        self.press('Tab')
        self.press('Enter') # Next

        self.assertSeen('UID number:')

        # Enter a GID
        self.press('Tab')
        self.press('1000')
        for _ in range(0, 5):
            self.press('Tab')
        self.press('Enter') # Next

        self.assertSeen('User must change password at next logon')

        # Enter password, etc
        self.press('locDCpass1')
        self.press('Tab')
        self.press('locDCpass1')
        self.press('Tab')
        self.press('Space') # Uncheck User must change password
        self.press('Tab')
        self.press('Space') # Check Password never expires
        self.press('Tab')
        # Do not disable the account
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Click finish

        self.assertSeen(' '.join([fname, ini, lname]), 'User not found')

        # Delete the user
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % ' '.join([fname, ini, lname]))
        self.press('Enter') # Yes
        self.assertNotSeen(' '.join([fname, ini, lname]), 'User found after deletion!')

    def test_create_delete_ou(self):
        # Highlight the domain
        for _ in range(0, 50):
            self.press('Up')
        self.press('Tab')
        self.press('Tab')

        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('│New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Organizational Unit
        self.assertSeen('│Organizational Unit')
        for _ in range(0, 5):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('New Object - Organizationalunit')

        # Provide an OU name
        name = '00000000%s' % randomName(10)
        self.press(name)
        self.press('Tab')
        self.press('Enter')

        self.assertSeen(name, 'OU not found')

        # Delete the OU
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up')
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % name)
        self.press('Enter') # Yes
        self.assertNotSeen(name, 'OU found after deletion!')

    def test_move_group(self):
        ### Create a test OU ###
        # Highlight the domain
        for _ in range(0, 50):
            self.press('Up')
        self.press('Tab')
        self.press('Tab')

        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('│New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Organizational Unit
        self.assertSeen('│Organizational Unit')
        for _ in range(0, 5):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('New Object - Organizationalunit')

        # Provide an OU name
        name = '00000000%s' % randomName(10)
        self.press(name)
        self.press('Tab')
        self.press('Enter')

        self.assertSeen(name, 'OU not found')

        ### Create a test Group ###
        self.press('Tab')
        for _ in range(0, 50): # Select Users
            self.press('Down')

        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('│New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Group
        self.assertSeen('│Group')
        for _ in range(0, 2):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('New Object - Group')

        # Group name, etc
        gname = '00000000%s' % randomName(5)
        self.press(gname)
        self.press('Tab')
        self.press(gname)
        self.press('BTab')
        self.press('BTab')
        self.press('BTab')
        self.press('Enter')

        self.assertSeen(gname, 'Group not found')

        ### Move the test group to the test OU ###
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Move...')
        self.press('Enter') # Move
        self.assertSeen('Move object into container:')
        self.press('Down') # Select the test OU
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Are you sure you want to move this object?')
        self.press('Enter') # Yes
        # Select the test OU
        self.press('Tab')
        for _ in range(0, 50):
            self.press('Up')
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Tab')

        self.assertSeen(gname, 'Group not found after object move')

        ### Delete the test group ###
        # No easy way to hightlight the test group when there is only one object
        self.press('Enter') # Open the properties window
        self.assertSeen('%s Properties' % gname)
        self.press('BTab')
        self.press('BTab')
        self.press('Enter') # Cancel (now the object is selected)
        self.assertNotSeen('%s Properties' % gname)
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % gname)
        self.press('Enter') # Yes
        self.assertNotSeen(gname, 'Group found after deletion!')

        ### Delete the test OU ###
        self.press('Tab')
        self.press('Up') # For some reason selecting the domain moves the cursor to the file menu
        self.press('Tab')
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up')
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('│Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % name)
        self.press('Enter') # Yes
        self.assertNotSeen(name, 'OU found after deletion!')

    def tearDown(self):
        self.at.shutdown()

if __name__ == "__main__":
    unittest.main()
