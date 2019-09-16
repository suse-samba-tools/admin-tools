import unittest
import hecate
from adcommon.creds import kinit_for_gssapi
from samba.credentials import Credentials, MUST_USE_KERBEROS
from getpass import getpass
from subprocess import Popen, PIPE
import re, six
from time import sleep
import random, string
from configparser import ConfigParser

def randomName(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length)).title()

class AdminToolsTestCase(unittest.TestCase):
    def assertSeen(self, what, msg=None, timeout=10):
        try:
            self.at.await_text(what, timeout=timeout)
        except hecate.hecate.Timeout:
            pass
        self.assertRegex(self.at.screenshot(), what, msg)

    def assertNotSeen(self, what, msg=None, timeout=10):
        sleep(.5)
        slept = 0
        while slept < timeout:
            slept += .1
            if not re.search(what, self.at.screenshot()):
                break
            sleep(.1)
        self.assertNotRegex(self.at.screenshot(), what, msg)

    def press(self, msg):
        self.at.press(msg)
        sleep(.1)

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

    def get_password(self):
        if not self.creds.get_password():
            self.creds.set_password(getpass('Password for %s: ' % self.creds.get_username()))
        return self.creds.get_password()

    def kinit(self):
        while not self.__validate_kinit():
            print('Domain administrator credentials are required to run the test.')
            upn = '%s@%s' % (self.creds.get_username(), self.creds.get_domain()) if self.creds.get_username() and self.creds.get_domain() else None
            username = input('Domain user principal name%s: ' % (' (%s)' % upn if upn else ''))
            if username:
                self.creds.set_username(username)
            else:
                self.creds.set_username(upn)
            self.creds.set_password(getpass('Password for %s: ' % self.creds.get_username()))
            kinit_for_gssapi(self.creds, None)

    def setUp(self):
        self.creds = Credentials()
        self.config = ConfigParser()
        self.config.read('.tcreds')
        if self.config.has_section('creds'):
            self.creds.set_username('%s@%s' % (self.config.get('creds', 'username'), self.config.get('creds', 'domain')))
            self.creds.set_domain(self.config.get('creds', 'domain'))
            self.creds.set_password(self.config.get('creds', 'password'))
            kinit_for_gssapi(self.creds, None)
        self.kinit()
        self.at = hecate.Runner("admin-tools", width=120, height=50)

    def tearDown(self):
        self.at.shutdown()
        if self.creds.get_password():
            if not self.config.has_section('creds'):
                self.config.add_section('creds')
            self.config.set('creds', 'username', self.creds.get_username())
            self.config.set('creds', 'domain', self.creds.get_domain())
            self.config.set('creds', 'password', self.creds.get_password())
            self.config.write(open('.tcreds', 'w'))
