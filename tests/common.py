import unittest
import hecate
from adcommon.creds import kinit_for_gssapi
from samba.credentials import Credentials, MUST_USE_KERBEROS
from getpass import getpass
from subprocess import Popen, PIPE
import re, six

class AdminToolsTestCase(unittest.TestCase):
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
        self.creds.set_username(user.decode())
        self.creds.set_domain(realm.decode())
        with Popen(['klist', '-s'], stdout=PIPE, stderr=PIPE) as p:
            if p.wait() != 0:
                return False
        self.creds.set_kerberos_state(MUST_USE_KERBEROS)
        return True

    def kinit(self):
        while not self.__validate_kinit():
            print('Domain administrator credentials are required to run the test.')
            username = input('Domain user principal name%s: ' % (' (%s)' % self.creds.get_username() if self.creds.get_username() else ''))
            if username:
                self.creds.set_username(username)
            self.creds.set_password(getpass('Password for %s: ' % self.creds.get_username()))
            kinit_for_gssapi(self.creds, None)

    def setUp(self):
        self.creds = Credentials()
        self.kinit()
