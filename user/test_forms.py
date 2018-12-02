from .forms import IoniaUserCreationForm
import pytest


@pytest.mark.django_db
class TestUserForm:
    def test_maps_password_to_password_1_and_2(self):
        # data = {"password": "test_password"}
        password_one = IoniaUserCreationForm().add_prefix("password1")
        password_two = IoniaUserCreationForm().add_prefix("password2")
        assert password_one and password_two == "password"

    def test_form_field_mapping(self):
        data = {"username": "test_field", "password": "test_password"}
        form = IoniaUserCreationForm(data=data)
        assert form.is_valid()

