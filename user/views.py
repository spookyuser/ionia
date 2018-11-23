from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from island.models import Island
from user.forms import IoniaUserCreationForm

User = get_user_model()


class RegisterView(generic.CreateView):
    """User Register View.

    Used for both the embedded register form
    and the root register form

    Checks if the form is valid. If it is, the
    new user is subscribed to the default Island/s
    and then logged in

    See-Also:
        https://stackoverflow.com/a/31491942/1649917
        https://stackoverflow.com/a/48040136/1649917
    """

    template_name = "registration/register.html"
    model = User
    form_class = IoniaUserCreationForm

    def form_valid(self, form):
        """Override form valid.

        Validate form.
        Subscribe to default Island.
        Make the user follow itself.
        Log user in.

        See-Also:
            https://stackoverflow.com/a/31491942/1649917
        """
        valid = super(RegisterView, self).form_valid(form)
        username, password = (
            form.cleaned_data.get("username"),
            form.cleaned_data.get("password1"),
        )
        new_user = authenticate(
            request=self.request, username=username, password=password
        )
        self.add_defaults(new_user)
        login(self.request, new_user)
        return valid

    def form_invalid(self, form):
        """Redirect user if form is invalid.

        Sends user to the root register template if
        the password doesn't pass the validation tests
        set in settings.py.

        See-Also/From:
            https://stackoverflow.com/a/48040136/1649917
        """
        #
        try:
            validate_password(
                form.cleaned_data.get("password1"), form.cleaned_data.get("username")
            )
        except ValidationError as validation_error:
            form.add_error(
                "password1", validation_error
            )  # to be displayed with the field's errors
            return render(self.request, self.template_name, {"form": form})

    @staticmethod
    def add_defaults(user):
        """Default operations to perform when user is created

        Subscribe to default Island
        Make user follow themselves
        """
        default_subscribe = Island.get_island(settings.DEFAULT_ISLAND)
        user.subscribes.add(default_subscribe)
        user.follows.add(user)

    def get_success_url(self):
        return reverse("post:index")


class DetailView(generic.DetailView):
    """User Detail View"""

    model = User
    context_object_name = "user_object"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs["pk"])


def change_follow(request, username, action):
    """Change or add follow status"""
    selected_user = get_object_or_404(User, username=username)
    if action == "unfollow":
        request.user.follows.remove(selected_user)
    elif action == "follow":
        request.user.follows.add(selected_user)
    return HttpResponseRedirect(reverse("user:detail", args=[username]))


class ChangeEmail(generic.UpdateView):
    """Change or add user email."""

    model = User
    fields = ["email"]
    template_name = "user/email_change_form.html"

    def get_success_url(self):
        return reverse("user:email_change_done")

    def get_object(self, queryset=None):
        return self.request.user


class ChangeEmailDone(generic.TemplateView):
    """Redirect when email change is completed."""

    template_name = "user/email_change_done.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
