from django import template

from user.forms import IoniaUserCreationForm

register = template.Library()


@register.simple_tag
def authentication_form():
    """Add user creation form to context"""
    return IoniaUserCreationForm()
