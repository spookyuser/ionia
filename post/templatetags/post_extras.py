from django import template

from post.forms import PostForm

register = template.Library()


@register.simple_tag
def post_form():
    """Add post form to page context"""
    return PostForm()
