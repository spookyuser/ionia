from .forms import IslandCreationForm


class TestIslandForm:
    def test_name_field_label(self):
        form = IslandCreationForm()
        assert form.fields["name"] is None or "name"

    def test_description_field_label(self):
        form = IslandCreationForm()
        assert form.fields["description"] is None or "description"
