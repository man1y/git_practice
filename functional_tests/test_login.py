from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time
import ssl

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.staging_server:
            test_email = 'mly40@socal.rr.com'
        else:
            test_email = TEST_EMAIL

        self.browser.get(self.live_server_url)

        self.browser.find_element(by=By.NAME, value='email').send_keys(test_email)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        ))

        # She checks her email and find a message
        body = self.wait_for_mail(test_email, SUBJECT)

        # It has a URL link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)
        # she is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_mail(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('mail.twc.com', context=ssl.create_default_context())
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['EMAIL_PASSWORD'])
            while time.time() - start < 30:
                # get 1 newest message
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count-1), count+1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    # print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.quit()
