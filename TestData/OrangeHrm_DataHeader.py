from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestLocators.OrangeHrm_Locators import locators
from Utilities.excel_functions import excelFunction
from Utilities.yaml_functions import YAMLReader


class OrangeHRMHeader:
    # Class to handle OrangeHRM operations with test data and interactions

    # Paths to test data files
    excel_file = "D:\\VinoLEarning\\Capstone_Vino\\TestData\\OrangeHRM_Header.xlsx"
    yaml_file = "D:\\VinoLEarning\\Capstone_Vino\\TestData\\config.yaml"
    sheet_number = "Sheet1"

    # Initialize data readers for Excel and YAML
    excel_obj = excelFunction(excel_file, sheet_number)
    yaml_obj = YAMLReader(yaml_file)

    # Read configuration and test data from YAML
    url = yaml_obj.reader()['url']
    dashboard_url = yaml_obj.reader()['dashboard_url']
    title = yaml_obj.reader()['title']
    actual_headers = []
    actual_tabs = []
    error_text = yaml_obj.reader()['error_text']
    pass_data = yaml_obj.reader()['pass_data']
    fail_data = yaml_obj.reader()['fail_data']

    def __init__(self, url, driver):
        """
        Initialize with URL and WebDriver instance.
        """
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 30)
        self.excel_obj = excelFunction(self.excel_file, self.sheet_number)

    @classmethod
    def read_login_data_empOperations(cls, start_row, end_row=None):
        """
        Read login data for employee operations from the Excel file.
        If end_row is not provided, use start_row as the only row.
        """
        data = []
        end_row = end_row or start_row
        for row in range(start_row, end_row + 1):
            username = cls.excel_obj.read_data(row, 6)
            password = cls.excel_obj.read_data(row, 7)
            data.append((username, password, row))
        return data

    def WebPageAccess(self):
        """
        Access the specified URL and maximize the browser window.
        Returns the title of the current page.
        """
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            print(self.driver.title)  # Print the title of the current page
            return self.driver.title
        except TimeoutException as e:
            print(e)  # Print the exception if a timeout occurs

    def login(self, username, password):
        """
        Perform login with provided username and password.
        Handles both successful and failed login attempts.
        """
        try:
            # Locate and interact with the username field
            username_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_username)))
            username_element.send_keys(username)
            print(username)  # Print the username used for login

            # Locate and interact with the password field
            pswd_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_password)))
            pswd_element.send_keys(password)
            print(password)  # Print the password used for login

            # Locate and click the login button
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, locators.loc_login)))
            login_button.click()

            # Check for error message indicating a failed login
            try:
                error_message_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_error)))
                print(error_message_element.text)  # Print the error message
                error_text = error_message_element.text
            except TimeoutException:
                current_url = self.driver.current_url  # Return the current URL on successful login
                return current_url
        except TimeoutException as e:
            print(e)  # Print the exception if a timeout occurs

    def ResetPasswordTest(self):
        """
        Perform a password reset test.
        Clicks on the 'Forgot Password' link, enters a username, and clicks the reset button.
        Returns the reset message.
        """
        try:
            # Locate and click the 'Forgot Password' link
            forgot_pswd_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_forgotpswd)))
            forgot_pswd_element.click()

            # Enter the username for password reset
            reset_user_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, locators.loc_reset_username)))
            reset_user_element.send_keys(self.yaml_obj.reader()['reset_username'])

            # Locate and click the reset button
            reset_button_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, locators.loc_reset_button)))
            reset_button_element.click()

            # Wait for URL to change to indicate password reset process
            self.wait.until(EC.url_contains('sendPasswordReset'))

            # Locate and print the reset message
            reset_msg_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_reset_msg)))
            reset_msg_text = reset_msg_element.text
            print(reset_msg_text)
            return reset_msg_text

        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException occurred: {e}")
            return False

    def AdminAccess(self):
        """
        Access the Admin section of the application.
        Waits for the URL to contain '/viewSystemUsers' to confirm successful navigation.
        Returns the title of the current page.
        """
        try:
            # Locate and click the Admin section link
            Admin_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_Admin)))
            Admin_element.click()

            # Wait for the URL to contain '/viewSystemUsers'
            self.wait.until(EC.url_contains("/viewSystemUsers"))
            return self.driver.title

        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException occurred: {e}")
            return False

    def CheckAdminHeaders(self):
        """
        Check the headers in the Admin section.
        Captures the text of each header and appends it to the list of actual headers.
        """
        try:
            # Locate and capture the text of each header element
            usermgmt_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_usermgmt)))
            usermgmt_text = usermgmt_element.text
            self.actual_headers.append(usermgmt_text)

            job_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_job)))
            job_text = job_element.text
            self.actual_headers.append(job_text)

            org_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_org)))
            org_text = org_element.text
            self.actual_headers.append(org_text)

            qual_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_qual)))
            qual_text = qual_element.text
            self.actual_headers.append(qual_text)

            nation_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_nation)))
            nation_text = nation_element.text
            self.actual_headers.append(nation_text)

            corpbank_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_corp_bank)))
            corpbank_text = corpbank_element.text
            self.actual_headers.append(corpbank_text)

            config_element = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_config)))
            config_text = config_element.text
            self.actual_headers.append(config_text)

            print(self.actual_headers)  # Print the captured headers
            return self.actual_headers

        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException occurred: {e}")
            return False

    def CheckAdminTabs(self):
        """
        Check the tabs in the Admin section.
        Captures the text of each tab and appends it to the list of actual tabs.
        """
        try:
            # Locate and capture the text of each tab element
            Admin_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_Admintab)))
            Admin_tab_text = Admin_tabelement.text
            self.actual_tabs.append(Admin_tab_text)

            PIM_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_PIM)))
            PIM_tab_text = PIM_tabelement.text
            self.actual_tabs.append(PIM_tab_text)

            Leave_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_Leavetab)))
            Leave_tab_text = Leave_tabelement.text
            self.actual_tabs.append(Leave_tab_text)

            Time_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_Timetab)))
            Time_tab_text = Time_tabelement.text
            self.actual_tabs.append(Time_tab_text)

            Recruit_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_Recruittab)))
            Recruit_tab_text = Recruit_tabelement.text
            self.actual_tabs.append(Recruit_tab_text)

            Info_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_infotab)))
            Info_tab_text = Info_tabelement.text
            self.actual_tabs.append(Info_tab_text)

            Perf_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_perftab)))
            Perf_tab_text = Perf_tabelement.text
            self.actual_tabs.append(Perf_tab_text)

            Dash_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_dashtab)))
            Dash_tab_text = Dash_tabelement.text
            self.actual_tabs.append(Dash_tab_text)

            Direct_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_directtab)))
            Direct_tab_text = Direct_tabelement.text
            self.actual_tabs.append(Direct_tab_text)

            Main_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_maintab)))
            Main_tab_text = Main_tabelement.text
            self.actual_tabs.append(Main_tab_text)

            Claim_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_claimtab)))
            Claim_tab_text = Claim_tabelement.text
            self.actual_tabs.append(Claim_tab_text)

            Buzz_tabelement = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.loc_buzztab)))
            Buzz_tab_text = Buzz_tabelement.text
            self.actual_tabs.append(Buzz_tab_text)

            print(self.actual_tabs)  # Print the captured tabs
            return self.actual_tabs

        except TimeoutException as e:
            print(f"TimeoutException occurred: {e}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException occurred: {e}")
            return False
