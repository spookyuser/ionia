from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from island.forms import IslandCreationForm
from post.models import Post
from post.sorts import Hot
from .models import Island


class DetailView(generic.DetailView):
    """Island Detail View"""
    model = Island
    context_object_name = "island"

    # noinspection PyAttributeOutsideInit
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch method

        Get sort type before get context data
        If Island doesn't exist, send user to Island creation page
        """
        self.sort = kwargs.get("sort", Hot.name)
        try:
            Island.get_island(self.kwargs["pk"])
        except ObjectDoesNotExist:
            create_form = IslandCreationForm()
            return render(
                request,
                "island/island_not_created.html",
                {"form": create_form, "submitted_island": self.kwargs["pk"]},
            )
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self, **kwargs):
        """Use iexact search"""
        return Island.get_island(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Paginate and sort posts"""
        context = super(DetailView, self).get_context_data(**kwargs)
        paginator = Paginator(
            Post.get_island_posts(self.sort, context["island"]), settings.MAX_POSTS_PAGE
        )
        page = self.request.GET.get("page")
        context["post_list"] = paginator.get_page(page)
        context["selected_sort"] = self.sort
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    """Create Island View

    Add `created_by` on `form_valid`, from
    https://stackoverflow.com/a/33001010/1649917
    """
    model = Island
    template_name = "island/create_island.html"
    form_class = IslandCreationForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        response = super().form_valid(form)
        user.subscribes.add(self.object)
        return response


class ListView(generic.ListView):
    model = Island

    def get_queryset(self):
        return Island.get_top_islands(1000)


@login_required
def change_subscribe(request, island, action):
    """Subscribe or unsubscribe a user to an Island given an action"""
    selected_island = get_object_or_404(Island, name=island)
    if action == "unsubscribe":
        request.user.subscribes.remove(selected_island)
    else:
        request.user.subscribes.add(selected_island)
    return HttpResponseRedirect(reverse("island:detail", args=[island]))
