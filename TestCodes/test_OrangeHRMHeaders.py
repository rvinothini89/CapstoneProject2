import pytest
from selenium.common import TimeoutException
from TestData.OrangeHrm_DataHeader import OrangeHRMHeader
from Utilities.excel_functions import excelFunction
from Utilities.yaml_functions import YAMLReader


class Test_OrangeHRMHeader:
    """
    Class to test OrangeHRM header functionalities using pytest.
    The driver is initialized per class using a fixture in conftest.py to avoid multiple instantiations.
    """

    @pytest.fixture(autouse=True)
    # Fixture to initialize the OrangeHRMHeader object and data readers
    def setup_class(self, driver):
        self.driver = driver
        """
        Initializes the OrangeHRMHeader object and data readers for each test case.
        Uses pytest's type keyword to create class-level instances to avoid initialization issues.
        """
        type(self).obj1 = OrangeHRMHeader(OrangeHRMHeader.url, driver)
        self.obj1.WebPageAccess()
        type(self).eobj1 = excelFunction(OrangeHRMHeader.excel_file, OrangeHRMHeader.sheet_number)
        type(self).yobj1 = YAMLReader(OrangeHRMHeader.yaml_file)

    def login_helper(self, username, password):
        """
        Helper function to perform login and check if the login was successful.
        Returns True if the login was successful, otherwise False.
        """
        try:
            current_url = self.obj1.login(username, password)
            if current_url == OrangeHRMHeader.dashboard_url:
                print(f"Successfully logged in using {username}, {password}")
                return True
            else:
                print(f"Login failed due to incorrect credentials: {username}, {password}")
                return False
        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False

    @pytest.mark.parametrize("username,password,row", OrangeHRMHeader.read_login_data_empOperations(2))
    def test_ResetPasswordLink(self, username, password, row):
        """
        Test the 'Forgot Password' link functionality.
        Asserts that the reset message is as expected and updates the test status in Excel.
        """
        try:
            # Read expected reset message from YAML
            reset_message = self.yobj1.reader()['reset_message']
            actual_message = self.obj1.ResetPasswordTest()
            if self.obj1.WebPageAccess():
                assert actual_message == reset_message, f"Expected {reset_message}, but got {actual_message}"
                print("Forgot password link validated successfully")
                self.eobj1.write_data(row, 8, OrangeHRMHeader.pass_data)

        except TimeoutException as e:
            # Handle timeout exceptions and update Excel status
            print(f"TimeoutException occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed

        except AssertionError as e:
            # Handle assertion errors and update Excel status
            print(f"AssertionError occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed

    @pytest.mark.parametrize("username,password,row", OrangeHRMHeader.read_login_data_empOperations(3))
    def test_checkAdminHeaders(self, username, password, row):
        """
        Test the headers present in the Admin section.
        Asserts that the actual headers match the expected headers and updates the test status in Excel.
        """
        try:
            # Read expected headers and title from YAML
            expected_headers = self.yobj1.reader()['expected_headers']
            title = self.yobj1.reader()['title']
            # Perform login and check if successful
            login_status = self.login_helper(username, password)
            assert login_status, "Login was not successful"
            actual_title = self.obj1.AdminAccess()
            # Verify the title of the page
            assert actual_title == title, f"Expected title '{title}', but got {actual_title}"
            print("Web page title validated successfully")
            # Verify the headers
            actual_headers = self.obj1.CheckAdminHeaders()
            assert actual_headers == expected_headers, f"Expected {expected_headers}, but got {actual_headers}"
            self.eobj1.write_data(row, 8, OrangeHRMHeader.pass_data)
            print("Headers in the Admin section validated successfully")

        except AssertionError as e:
            # Handle assertion errors and update Excel status
            print(f"AssertionError occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed

        except TimeoutException as e:
            # Handle timeout exceptions and update Excel status
            print(f"TimeoutException occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed

    @pytest.mark.parametrize("username,password,row", OrangeHRMHeader.read_login_data_empOperations(4))
    def test_checkAdminTabs(self, username, password, row):
        """
        Test the tabs present in the Admin section.
        Asserts that the actual tabs match the expected tabs and updates the test status in Excel.
        """
        try:
            # Read expected tabs from YAML
            expected_tabs = self.yobj1.reader()['expected_tabs']
            # Perform login and check if successful
            login_status = self.login_helper(username, password)
            assert login_status, "Login was not successful"
            actual_tabs = self.obj1.CheckAdminTabs()
            self.obj1.AdminAccess()
            # Verify the tabs
            assert actual_tabs == expected_tabs, f"Expected {expected_tabs}, but got {actual_tabs}"
            self.eobj1.write_data(row, 8, OrangeHRMHeader.pass_data)
            print("Tabs in the Admin section validated successfully")

        except AssertionError as e:
            # Handle assertion errors and update Excel status
            print(f"AssertionError occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed

        except TimeoutException as e:
            # Handle timeout exceptions and update Excel status
            print(f"TimeoutException occurred: {e}")
            self.eobj1.write_data(row, 8, OrangeHRMHeader.fail_data, str(e))
            pytest.fail(str(e))  # Mark the test as failed
