"""Forms for User

FIELD_NAME_MAPPING:
    Map password1 and password2 to password so we
    can continue using the django user creation form
    and not have a password confirmation input
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()
FIELD_NAME_MAPPING = {"password1": "password", "password2": "password"}


class IoniaUserCreationForm(UserCreationForm):
    """User creation form"""
    class Meta(UserCreationForm.Meta):
        model = User

    def add_prefix(self, field_name):
        """Look up field name (password1/2), return original if not found"""
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(UserCreationForm, self).add_prefix(field_name)
