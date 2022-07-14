from django.contrib.auth.mixins import UserPassesTestMixin

class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.profile.role == "President":
            return True
        else:
            return False

    