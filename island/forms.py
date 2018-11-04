from django.forms import ModelForm, TextInput, Textarea

from island.models import Island


class IslandCreationForm(ModelForm):
    """Description + name"""
    class Meta:
        model = Island
        fields = ("name", "description")
        widgets = {
            "name": TextInput(attrs={"placeholder": "Island name"}),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your island (optional)",
                    "class": "mv1 h3 w-100",
                }
            ),
        }
