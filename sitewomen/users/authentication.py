from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email = username)
            if user.check_password(password)
                return user
            else:
                None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

