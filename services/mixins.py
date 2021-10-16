from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserIsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class UserIsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_if_patient(self):
        return redirect('login-redirect')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        # if request.user.type == 'patient':
        #     return self.handle_no_permission()

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)


class UserIsPatientMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.type == 'patient'
