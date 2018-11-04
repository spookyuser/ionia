from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from island.forms import IslandCreationForm
from post.forms import PostForm
from .models import Island, Post
from .sorts import Hot


class IndexView(generic.ListView):
    """Ionia index view

    The index sends users to a post list depending on
    whether they are anonymous or logged in and what
    kind of sort, list type is selected
    """

    template_name = "ionia/index.html"
    model = Post
    context_object_name = "post_list"

    # noinspection PyAttributeOutsideInit
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch method

        Get sort and list type before get context data
        """
        self.list_type = kwargs.get("list", "subscribed")
        self.sort = kwargs.get("sort", Hot.name)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Override get queryset  method

        Get a different queryset depending on whether the user
        is logged in and what list, sort type is selected

        If the user isn't logged, get posts by the anonymous user filter
        """
        if self.request.user.is_authenticated:
            return Post.get_user_posts(self.list_type, self.sort, self.request.user)
        else:
            return Post.get_anonymous_posts(self.sort)

    def get_context_data(self, **kwargs):
        """Override get context data

        Add sort and list variables to context
        """
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = Paginator(context["post_list"], settings.MAX_POSTS_PAGE)
        page = self.request.GET.get("page")
        context["post_list"] = paginator.get_page(page)
        context["selected_sort"] = self.sort
        context["selected_list_type"] = self.list_type
        return context


class DetailView(generic.DetailView):
    """Post Detail View"""

    model = Post


@login_required
def save_post(request):
    """Saves a Post

    Check if the post's island exists
    If not redirect the user to Island creation page
    If no island was included, use the default island.
    Add post to user's likes then save the post and
    return the user to a page specified with the next variable
    """
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.cleaned_data["post"]
            island_name = form.cleaned_data["island"]

            if island_name:
                try:
                    island = Island.get_island(island_name)
                except ObjectDoesNotExist:
                    create_form = IslandCreationForm()
                    return render(
                        request,
                        "island/island_not_created.html",
                        {"form": create_form, "submitted_island": island_name},
                    )
            else:
                island = Island.get_island(settings.DEFAULT_ISLAND)
            post = Post(post=post, user=request.user, island=island)
            post.save()
            request.user.likes.add(post)
            return HttpResponseRedirect(request.GET.get("next", ""))


@login_required
def change_like(request, pk, action):
    post = Post.objects.get(pk=pk)
    user = request.user
    next_url = request.GET.get("next")

    if action == "add":
        user.likes.add(post)
    elif action == "remove":
        user.likes.remove(post)
    if next_url:
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect(reverse("post:index"))
