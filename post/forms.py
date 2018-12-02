from django import forms
from django.conf import settings


class PostForm(forms.Form):
    """Form describing Post (Post+Island)
    TODO: Draw from model https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms#ModelForms
    """

    post = forms.CharField(widget=forms.Textarea, max_length=240)
    island = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": settings.DEFAULT_ISLAND}),
    )
