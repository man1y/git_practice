from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def wait(func):
        def modified_func(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return func(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > FunctionalTest.MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_func

    def setUp(self) -> None:
        # Set up webdriver
        geckodriver_path = '/snap/bin/geckodriver'
        driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

        self.browser = webdriver.Firefox(service=driver_service)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text) -> None:
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, func):
        return func()

    def get_item_input_box(self):
        return self.browser.find_element(by=By.ID, value='id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(by=By.LINK_TEXT, value='Log out')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(by=By.NAME, value='email')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertNotIn(email, navbar.text)
