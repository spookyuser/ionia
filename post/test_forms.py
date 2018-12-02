from .forms import PostForm


class TestPostForm:
    def test_post_field_label(self):
        """From: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing"""
        form = PostForm()
        assert form.fields["post"] is None or "post"

    def test_island_field_label(self):
        form = PostForm()
        assert form.fields["island"] is None or "island"
