from django.contrib.auth.backends import BaseBackend

from accounts.models import Token, User

class PasswordlessAuthenticationBackend(BaseBackend):
    def authenticate(self, request, uuid):
        try:
            token = Token.objects.get(uuid=uuid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
