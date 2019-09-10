import unittest
import hecate
from adcommon.creds import kinit_for_gssapi, pdc_dns_name
from samba.credentials import Credentials, MUST_USE_KERBEROS
from samba.param import LoadParm
from samba.auth import system_session
from samba.samdb import SamDB
from getpass import getpass
from subprocess import Popen, PIPE
import re, six
import ldapurl

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
        m = re.findall(six.b('Ticket cache:\s*(.*)'), out)
        if len(m) != 1:
            return None
        self.creds.set_named_ccache(m[0].decode())
        m = re.findall(six.b('Default principal:\s*(\w+)@([\w\.]+)'), out)
        if len(m) == 0:
            return False
        user, realm = m[0]
        if Popen(['klist', '-s'], stdout=PIPE, stderr=PIPE).wait() != 0:
            return False
        self.creds.set_kerberos_state(MUST_USE_KERBEROS)
        self.creds.set_username(user.decode())
        self.creds.set_domain(realm.decode())
        return True

    def kinit(self):
        while not self.__validate_kinit():
            print('Domain administrator credentials are required to run the test.')
            self.creds.set_username(input('Domain user principal name: '))
            self.creds.set_password(getpass('Password for %s: ' % self.creds.get_username()))
            kinit_for_gssapi(self.creds, None)

    def setUp(self):
        self.creds = Credentials()
        self.lp = LoadParm()
        self.lp.load_default()
        self.creds.guess(self.lp)
        self.kinit()
        self.lp.set('realm', self.creds.get_domain())
        ldap_url = ldapurl.LDAPUrl('ldap://%s' % pdc_dns_name(self.creds.get_domain()))
        self.samdb = SamDB(url=ldap_url.initializeUrl(), session_info=system_session(),
                           credentials=self.creds, lp=self.lp)
