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
        timeout = 0
        while '┌%s─' % name not in self.at.screenshot() and timeout < 50:
            self.press('Down')
            timeout+=1
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

    def test_modify_account_policy_gpo(self):
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

        ### Modify Password Policy ###
        self.press('BTab')
        self.press('Enter') # Action menu
        self.assertSeen('Edit...')
        self.press('Enter') # Edit
        self.assertSeen('Group Policy Management Editor')
        self.press('Down') # Policies
        self.press('Space')
        self.press('Down') # OS Settings
        self.press('Space')
        self.press('Down') # Security Settings
        self.press('Space')
        self.press('Down') # Account Policy
        self.press('Space')
        self.press('Down') # Password Policy
        self.assertSeen('Minimum password age\s*│Not Defined')
        self.press('Tab')
        self.press('Enter') # Minimum password age
        self.assertSeen('MinimumPasswordAge Properties')
        self.press('1')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Minimum password age\s*│1 days')
        self.press('Down')
        self.assertSeen('Maximum password age\s*│Not Defined')
        self.press('Enter') # Maximum password age
        self.assertSeen('MaximumPasswordAge Properties')
        self.press('99')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Maximum password age\s*│99 days')
        for _ in range(0, 2):
            self.press('Down')
        self.assertSeen('Minimum password length\s*│Not Defined')
        self.press('Enter') # Minimum password length
        self.assertSeen('MinimumPasswordLength Properties')
        self.press('10')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Minimum password length\s*│10 characters')
        for _ in range(0, 3):
            self.press('Down')
        self.assertSeen('Password must meet complexity requirements\s*│Not Defined')
        self.press('Enter') # Password must meet complexity requirements
        self.assertSeen('PasswordComplexity Properties')
        self.press('Down')
        self.press('Enter')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Password must meet complexity requirements\s*│Enabled')
        for _ in range(0, 4):
            self.press('Down')
        self.assertSeen('Enforce password history\s*│Not Defined')
        self.press('Enter') # Enforce password history
        self.assertSeen('PasswordHistorySize Properties')
        self.press('10')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Enforce password history\s*│10 passwords remembered')
        for _ in range(0, 5):
            self.press('Down')
        self.assertSeen('Store passwords using reversible encryption\s*│Not Defined')
        self.press('Enter') # Store passwords using reversible encryption
        self.assertSeen('ClearTextPassword Properties')
        self.press('Down')
        self.press('Enter')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Store passwords using reversible encryption\s*│Enabled')

        ### Modify Account Lockout Policy ###
        self.press('BTab')
        self.press('Down')
        self.press('Tab')
        self.assertSeen('Account lockout duration\s*│Not Defined')
        self.press('Enter') # Account lockout duration
        self.assertSeen('LockoutDuration Properties')
        self.press('10')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Account lockout duration\s*│10 minutes')
        self.press('Down')
        self.assertSeen('Account lockout threshold\s*│Not Defined')
        self.press('Enter') # Account lockout threshold
        self.assertSeen('LockoutBadCount Properties')
        self.press('3')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Account lockout threshold\s*│3 invalid logon attempts')
        for _ in range(0, 2):
            self.press('Down')
        self.assertSeen('Reset account lockout counter after\s*│Not Defined')
        self.press('Enter') # Reset account lockout counter after
        self.assertSeen('ResetLockoutCount Properties')
        self.press('10')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Reset account lockout counter after\s*│10 minutes')

        ### Modify Kerberos Policy ###
        self.press('BTab')
        self.press('Down')
        self.press('Tab')
        self.assertSeen('Maximum lifetime for user ticket\s*│Not Defined')
        self.press('Enter') # Maximum lifetime for user ticket
        self.assertSeen('MaxTicketAge Properties')
        self.press('10')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Maximum lifetime for user ticket\s*│10 hours')
        self.press('Down')
        self.assertSeen('Maximum lifetime for user ticket renewal\s*│Not Defined')
        self.press('Enter') # Maximum lifetime for user ticket renewal
        self.assertSeen('MaxRenewAge Properties')
        self.press('600')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Maximum lifetime for user ticket renewal\s*│600 minutes')
        for _ in range(0, 2):
            self.press('Down')
        self.assertSeen('Maximum lifetime for service ticket\s*│Not Defined')
        self.press('Enter') # Maximum lifetime for service ticket
        self.assertSeen('MaxServiceAge Properties')
        self.press('600')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Maximum lifetime for service ticket\s*│600 minutes')
        for _ in range(0, 3):
            self.press('Down')
        self.assertSeen('Maximum tolerance for computer clock synchronization\s*│Not Defined')
        self.press('Enter') # Maximum tolerance for computer clock synchronization
        self.assertSeen('MaxClockSkew Properties')
        self.press('5')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Maximum tolerance for computer clock synchronization\s*│5 minutes')
        for _ in range(0, 4):
            self.press('Down')
        self.assertSeen('Enforce user logon restrictions\s*│Not Defined')
        self.press('Enter') # Enforce user logon restrictions
        self.assertSeen('TicketValidateClient Properties')
        self.press('Down')
        self.press('Enter')
        self.press('Tab')
        self.press('Enter') # OK
        self.assertSeen('Enforce user logon restrictions\s*│Enabled')

        ### Close the Group Policy Management Editor ###
        self.press('Tab')
        self.press('Enter') # File
        self.press('Enter') # Exit
        self.__select_gpo_by_name(gpo_name)

        ### Delete the GPO ###
        self.press('BTab')
        self.press('Enter') # Action menu
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete this GPO and all links')
        self.press('Enter') # Yes
        self.assertNotSeen(gpo_name)

    def test_modify_browser_maintenance_gpo(self):
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

        ### Modify Browser Proxy Settings Policy ###
        self.press('BTab')
        self.press('Enter') # Action menu
        self.assertSeen('Edit...')
        self.press('Enter') # Edit
        self.assertSeen('Group Policy Management Editor')
        for _ in range(0, 3):
            self.press('Down')
        self.press('Space') # Policies
        self.press('Down')
        self.press('Space') # OS Settings
        self.press('Down')
        self.press('Space') # Internet Browser Maintenance
        self.press('Down') # Connection
        self.press('Tab')
        self.assertSeen('Proxy Settings\s*│Settings for proxy')
        self.press('Enter') # Proxy Settings
        self.assertSeen('Proxy Settings Properties')
        self.press('Down')
        self.press('Up')
        self.press('Enter') # Enable proxy settings
        self.press('Tab')
        self.press('example.com') # Address of HTTP proxy
        for _ in range(0, 5):
            self.press('Tab')
        self.press('Down')
        self.press('Up')
        self.press('Enter') # Use the same proxy server for all addresses
        for _ in range(0, 2):
            self.press('Tab')
        self.press('Enter') # OK
        ### Reopen the dialog and ensure the settings were saved ###
        self.press('Enter') # Proxy Settings
        self.assertSeen('Enable proxy settings\s*│\s*│\s*│\s*│\s*Enabled')
        self.assertSeen('Address of HTTP proxy\s*│\s*│\s*│\s*│\s*example.com')
        self.assertSeen('Use the same proxy server for all addresses\s*│\s*│\s*│\s*│\s*Enabled')
        for _ in range(0, 2):
            self.press('BTab')
        self.press('Enter') # Cancel

        ### Modify Browser User Agent String Policy ###
        self.press('Down')
        self.assertSeen('User Agent String\s*│Settings for user agent string')
        self.press('Enter')
        self.assertSeen('User Agent String Properties')
        self.press('AppleTV6,2/11.1')
        self.press('Tab')
        self.press('Enter') # OK
        ### Reopen the dialog and ensure the settings were saved ###
        self.press('Down')
        self.press('Enter')
        self.assertSeen('AppleTV6,2/11.1')
        for _ in range(0, 2):
            self.press('BTab')
        self.press('Enter') # Cancel

        ### Close the Group Policy Management Editor ###
        self.press('Tab')
        self.press('Enter') # File
        self.press('Enter') # Exit
        self.__select_gpo_by_name(gpo_name)

        ### Delete the GPO ###
        self.press('BTab')
        self.press('Enter') # Action menu
        self.press('Down')
        self.press('Enter') # Delete
        self.assertSeen('Do you want to delete this GPO and all links')
        self.press('Enter') # Yes
        self.assertNotSeen(gpo_name)
