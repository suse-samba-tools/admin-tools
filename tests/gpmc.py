import unittest
import hecate
from time import sleep
from common import AdminToolsTestCase, randomName

class TestGPMC(AdminToolsTestCase):
    def __open_gpmc(self):
        self.assertSeen('Administrative Tools')
        for _ in range(0, 3):
            self.press('Down')
        self.press('Enter')
        self.assertSeen('To continue, type an Active Directory administrator password')
        self.press('Tab')
        self.press('Tab')
        self.press('Enter')
        self.assertSeen('Group Policy Management Console')
        # Make sure we see the Administrator in the Users list
        self.assertSeen('Default Domain Policy')
        self.assertNotSeen('00000000', 'You need to cleanup a previous failed run!')

    def __select_gpo_by_name(self, name):
        for _ in range(0, 50):
            self.press('Up')
        while '┌%s─' % name not in self.at.screenshot():
            self.press('Down')
        self.assertSeen('┌%s─' % name)

    def test_create_delete_gpo(self):
        self.__open_gpmc()

        ### Create a GPO ###
        self.press('Down')
        self.press('BTab')
        self.press('Enter') # Action menu
        self.assertSeen('Create a GPO in this domain, and Link it here...')
        self.press('Enter')
        self.assertSeen('New GPO')
        gpo_name = '00000000%s' % randomName(10)
        self.press(gpo_name)
        self.press('Tab')
        self.press('Enter') # OK

        ### Verify creation ###
        self.assertSeen(gpo_name)
        sleep(3)
        self.press('Tab')
        self.__select_gpo_by_name(gpo_name)

        ### Delete the GPO ###
        self.press('BTab')
        self.press('Enter') # Action menu
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete this GPO and all links')
        self.press('Enter') # Yes
        self.assertNotSeen(gpo_name)
