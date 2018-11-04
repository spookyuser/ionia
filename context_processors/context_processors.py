"""Project wide context processors

From https://stackoverflow.com/a/24383565/1649917
"""

from django.urls import reverse

from island.models import Island
from post.models import Post
from post.sorts import Hot, New


class Link:
    """Represents a link href and display text

    Each method contains a category of links
    """
    href = ""
    title = ""

    def __init__(self, href, title):
        self.href = href
        self.title = title

    @staticmethod
    def authenticated_links():
        links = [
            Link(reverse("avatar_change"), "Change avatar"),
            Link(reverse("user:email_change"), "Add/Update email"),
            Link(reverse("password_change"), "Change password"),
        ]
        return links

    @staticmethod
    def unauthenticated_links():
        links = [Link(reverse("password_reset"), "Reset password")]
        return links

    @staticmethod
    def global_links():
        links = [
            Link(reverse("island:list"), "Explore islands"),
            Link(reverse("island:create"), "Create an island"),
        ]
        return links


def template_links(request):
    """Adds sidebar links to context"""
    links = Link.global_links()
    if request.user.is_authenticated:
        links += Link.authenticated_links()
        links.append(Link(reverse("logout") + "?next=" + request.path, "Logout"))
    else:
        links += Link.unauthenticated_links()

    return {"template_links": links}


def common_contexts(request):
    """Adds arbitrary data common to one or more view"""
    common_context = {
        "top_islands": Island.get_top_islands(),
        "sorts": [Hot.name, New.name],
    }
    if request.user.is_authenticated:
        common_context.update(
            {
                "my_islands": Island.get_my_islands(request.user),
                "list_types": Post.list_types(),
            }
        )
    return common_context
