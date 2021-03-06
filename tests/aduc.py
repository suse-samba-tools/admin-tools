#!/usr/bin/python3
import unittest
import hecate
from time import sleep
from common import AdminToolsTestCase, randomName
from adcommon.yldap import *

class TestADUC(AdminToolsTestCase):
    def __open_aduc(self):
        self.assertSeen('Administrative Tools')
        self.press('Enter')
        self.assertSeen('To continue, type an Active Directory administrator password')
        for _ in range(0, 3):
            self.press('BTab')
        self.press('Enter')
        self.assertSeen('Active Directory Users and Computers', timeout=30)
        for _ in range(0, 50): # Select Users
            self.press('Down')
        # Make sure we see the Administrator in the Users list
        self.assertSeen('Domain Users')
        self.assertNotSeen('00000000', 'You need to cleanup a previous failed run!')

    def test_create_delete_group(self):
        self.__open_aduc()
        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Group
        self.assertSeen('Group')
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
        self.assertSeen('Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % gname)
        self.press('Enter') # Yes
        self.assertNotSeen(gname, 'Group found after deletion!')

    def test_create_delete_user(self):
        self.__open_aduc()
        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select User
        self.assertSeen('User')
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
        self.assertSeen('Delete')
        for _ in range(0, 3):
            self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % ' '.join([fname, ini, lname]))
        self.press('Enter') # Yes
        self.assertNotSeen(' '.join([fname, ini, lname]), 'User found after deletion!')

    def test_create_delete_ou(self):
        self.__open_aduc()
        # Highlight the domain
        for _ in range(0, 50):
            self.press('Up')
        self.press('Tab')
        self.press('Tab')

        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Organizational Unit
        self.assertSeen('Organizational Unit')
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
        self.assertSeen('Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % name)
        self.press('Enter') # Yes
        self.assertNotSeen(name, 'OU found after deletion!')

    def test_move_group(self):
        self.__open_aduc()
        ### Create a test OU ###
        # Highlight the domain
        for _ in range(0, 50):
            self.press('Up')
        self.press('Tab')
        self.press('Tab')

        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Organizational Unit
        self.assertSeen('Organizational Unit')
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
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select Group
        self.assertSeen('Group')
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
        self.assertSeen('Move...')
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
        self.assertSeen('Delete')
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
        self.assertSeen('Delete')
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % name)
        self.press('Enter') # Yes
        self.assertNotSeen(name, 'OU found after deletion!')

    def test_modify_user(self):
        self.__open_aduc()
        # Open the Action Menu
        self.press('BTab')
        self.press('Enter')
        self.assertSeen('New')
        # Select New
        self.press('Down')
        self.press('Enter')
        # Select User
        self.assertSeen('User')
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

        ### Disable the user ###
        self.press('Tab')
        self.press('Tab')
        self.press('Enter')
        self.assertSeen('%s Properties' % ' '.join([fname, ini, lname]), 'Properties dialog not found')
        self.press('Right')
        self.assertSeen('Street:') # Address Tab
        self.press('Right') # Account Tab
        self.assertSeen('\[ \] Account is disabled', 'Account should not be disabled!')
        for _ in range(0, 5):
            self.press('Tab')
        self.press('Space') # Check 'Account is disabled'
        self.press('Tab')
        self.press('Enter') # OK

        ### Verify account is disabled ###
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Enter')
        self.assertSeen('%s Properties' % ' '.join([fname, ini, lname]), 'Properties dialog not found')
        self.press('Right')
        self.assertSeen('Street:') # Address Tab
        self.press('Right') # Account Tab
        self.assertSeen('\[x\] Account is disabled', 'Account should be disabled!')

        ### Modify user shell ###
        self.press('Right') # Unix Attributes tab
        self.assertSeen('/bin/sh', 'Should have seen the default shell for test user')
        for _ in range(0, 5):
            self.press('Tab')
        self.press('BSpace')
        self.press('BSpace')
        self.press('bash')
        self.assertSeen('/bin/bash')
        self.press('Tab')
        self.press('Enter') # OK

        ### Verify user shell has changed ###
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Enter')
        self.assertSeen('%s Properties' % ' '.join([fname, ini, lname]), 'Properties dialog not found')
        for _ in range(0, 3):
            self.press('Right')
        self.assertSeen('/bin/bash', 'Should have seen the modified shell for test user')
        self.press('BTab')
        self.press('BTab')
        self.press('Enter') # Cancel

        # Delete the user
        self.press('Tab')
        self.press('Tab')
        self.press('Tab')
        self.press('Down')
        self.press('Up') # ADUC automatically selects the object, but does not update the menu
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Action menu
        self.assertSeen('Delete')
        for _ in range(0, 3):
            self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen("Are you sure you want to delete '%s'?" % ' '.join([fname, ini, lname]))
        self.press('Enter') # Yes
        self.assertNotSeen(' '.join([fname, ini, lname]), 'User found after deletion!')

    def __select_obj(self, name):
        timeout = 0
        while timeout < 50:
            self.press('Enter')
            self.assertSeen('Properties')
            if ('%s Properties' % name) in self.at.screenshot():
                break
            self.press('BTab')
            self.press('BTab')
            self.press('Enter') # Cancel
            self.press('Down')
            timeout+=1
        self.press('BTab')
        self.press('BTab')
        self.press('Enter') # Cancel

    def __testuser(self):
        uname = '00000000%s' % randomName(5)
        self.users.append(uname)
        try:
            self.conn.newuser(uname, randomName(20))
        except ldb.LdbError:
            pass # Ignore password issues
        return uname

    def __testgroup(self):
        gname = '00000000%s' % randomName(5)
        self.groups.append(gname)
        self.conn.newgroup(gname)
        return gname

    def test_group_assignment(self):
        self.__open_aduc()
        uname = self.__testuser()
        gname = self.__testgroup()
        self.press('Up')
        self.press('Down') # Refresh the page
        self.assertSeen(uname)
        self.assertSeen(gname)

        self.press('Tab')
        self.__select_obj(gname)
        self.press('Enter')
        self.assertSeen('%s Properties' % gname)
        self.press('Right')
        self.assertSeen('Members:')
        self.press('Tab')
        self.press('Tab')
        self.press('Enter') # Add
        self.press('Tab')
        self.press(uname)
        self.press('Tab')
        self.press('Enter') # Check Name
        self.press('Tab')
        self.press('Enter') # OK
        sleep(2)
        for _ in range(0, 6):
            self.press('Tab')
        self.press('Enter') # Apply
        result = self.conn.search(None, SCOPE_SUBTREE, '(samaccountname=%s)' % uname, ['memberOf'])[0]
        self.assertIn('memberOf', result)
        self.assertIn(gname, str(result['memberOf']))
        sleep(2)
        for _ in range(0, 4):
            self.press('Tab')
        self.press('Enter') # Remove
        for _ in range(0, 3):
            self.press('Tab')
        self.press('Enter') # OK
        result = self.conn.search(None, SCOPE_SUBTREE, '(samaccountname=%s)' % uname, ['memberOf'])[0]
        self.assertNotIn('memberOf', result)

    def test_object_search(self):
        self.__open_aduc()
        uname = self.__testuser()
        self.press('BTab')
        self.press('Enter') # Action
        self.assertSeen('Find...')
        self.press('Enter') # Find
        self.assertSeen('Find Users, Contacts, and Groups')
        for _ in range(0, 2):
            self.press('Tab')
        self.press(uname)
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Find Now
        self.assertSeen('%s\s*│User' % uname)
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # User Properties
        self.assertSeen('%s Properties' % uname)
        for _ in range(0, 2):
            self.press('BTab')
        self.press('Enter') # Cancel
        self.press('BTab')
        self.press('Enter') # Cancel
        self.assertSeen('Active Directory Users and Computers') # Make sure the dialog closed ok

    def test_password_reset(self):
        self.__open_aduc()
        uname = self.__testuser()
        self.press('Up')
        self.press('Down') # Refresh the page
        self.assertSeen(uname)

        ### Reset the password ###
        self.press('Tab')
        self.__select_obj(uname)
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # Action
        self.assertSeen('Reset Password...')
        self.press('Down')
        self.press('Enter') # Reset Password...
        self.assertSeen('New password:')
        self.press('locDCpass1')
        self.press('Tab')
        self.press('locDCpass1')
        self.press('Tab')
        self.assertSeen('\[x\] User must change password at next logon')
        self.press('Space')
        self.assertSeen('\[ \] User must change password at next logon')
        self.press('Tab')
        self.assertSeen('\[ \] Unlock the user\'s account')
        self.press('Space')
        self.assertSeen('\[x\] Unlock the user\'s account')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('The password for %s has been changed.' % uname)
        self.press('Enter') # OK
        self.assertNotSeen('The password for %s has been changed.' % uname)
        self.press('Enter') # Action
        for _ in range(0, 4):
            self.press('Down')
        self.press('Enter') # Properties
        self.assertSeen('%s Properties' % uname)
        self.press('Right')
        self.assertSeen('Street:') # Address tab
        self.press('Right')
        self.assertSeen('\[ \] User must change password at next logon') # Account Tab
        for _ in range(0, 2):
            self.press('BTab')
        self.press('Enter') # Cancel

    def setUp(self):
        super(TestADUC, self).setUp()
        self.conn = Ldap(self.lp, self.creds)
        self.users = []
        self.groups = []

    def tearDown(self):
        for user in self.users:
            try:
                self.conn.deleteuser(user)
            except Exception:
                pass # Ignore deletion failures
        for group in self.groups:
            try:
                self.conn.deletegroup(group)
            except Exception:
                pass # Ignore deletion failures
        super(TestADUC, self).tearDown()

if __name__ == "__main__":
    unittest.main()
