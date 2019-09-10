import unittest
import hecate
import random
import string
from time import sleep
from adcommon.creds import kinit_for_gssapi
from samba.credentials import Credentials, MUST_USE_KERBEROS
from getpass import getpass
from subprocess import Popen, PIPE
import re, six

def randomName(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length)).title()

class TestADUC(unittest.TestCase):
    def assertSeen(self, what, msg=None, timeout=10):
        try:
            self.at.await_text(what, timeout=timeout)
        except hecate.hecate.Timeout:
            pass
        self.assertIn(what, self.at.screenshot(), msg)

    def __validate_kinit(self):
        return Popen(['klist', '-s'], stdout=PIPE, stderr=PIPE).wait() == 0

    def __validate_kinit(self):
        out, _ = Popen(['klist'], stdout=PIPE, stderr=PIPE).communicate()
        m = re.findall(six.b('Default principal:\s*(\w+)@([\w\.]+)'), out)
        if len(m) == 0:
            return False
        user, realm = m[0]
        if Popen(['klist', '-s'], stdout=PIPE, stderr=PIPE).wait() != 0:
            return False
        self.creds.set_username(user.decode())
        self.creds.set_domain(realm.decode())
        self.creds.set_kerberos_state(MUST_USE_KERBEROS)
        return True

    def kinit(self):
        while not self.__validate_kinit():
            print('Domain administrator credentials are required to run the test.')
            self.creds.set_username(input('Domain user principal name: '))
            self.creds.set_password(getpass('Password for %s' % self.creds.get_username()))
            kinit_for_gssapi(self.creds, None)

    def setUp(self):
        self.creds = Credentials()
        self.kinit()
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
        sleep(1)

        # Enter a GID
        self.at.press('Tab')
        self.at.press('1000')
        for _ in range(0, 5):
            self.at.press('Tab')
        self.at.press('Enter') # Next
        sleep(1)

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
        sleep(1)

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
        sleep(3)
        self.assertNotIn(' '.join([fname, ini, lname]), self.at.screenshot(), 'User found after deletion!')

    def tearDown(self):
        self.at.shutdown()

if __name__ == "__main__":
    unittest.main()
