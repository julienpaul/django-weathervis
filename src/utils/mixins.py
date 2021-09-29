# Stdlib imports
# Core Django import
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

# Third-party app imports
# Imports from my app

# TODO LogoutIfNotStaffMixin
# see https://stackoverflow.com/questions/44341391/django-class-based-view-logout-user-if-not-staff


class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}


class CrispyMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # init crispy helper
        self.helper = FormHelper()
        self._init_helper_layout()
        # customize it
        self._custom_helper()

    def _init_helper_layout(self):
        """initialise crispy layout"""
        self.helper.layout = Layout()

    def _custom_helper(self):
        """customize crispy form"""
        pass
