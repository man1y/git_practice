from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

# Create your tests here.

User = auth.get_user_model()

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='edith@example.com')
        user.full_clean() # should not raise

    def test_email_is_primary_key(self):
        user = User(email='edith@example.com')
        self.assertEqual(user.pk, 'edith@example.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='edith@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)    # should not raise

class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uuid(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uuid, token2.uuid)
