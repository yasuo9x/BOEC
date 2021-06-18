from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django import forms
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from boec_core.views.signup import SignUpForm
from boec_core.views.edit_profile import EditProfileForm

from ..models import *


class RoleRequiredView(View):
    user_role = None
    form = None
    template_path = ""

    error_messages = {
        "anon_user": "This view can't be access by Anonymous user",
        "wrong_role_user": "This view can't be access by this user",
    }

    direct_url = {}
    post_redirect = None
    """
        View for Role Required
    """
    def role_required_decorator(func):
        def _wrapped_view(self, request, *args, **kwargs):
            try:
                if self.user_role is None:
                    return JsonResponse({
                        "status": "Error",
                        "msg": self.error_messages.get("anon_user"),
                    })
                else:
                    if request.user.role == 4:
                        return func(self, request, *args, **kwargs)
                    if request.user.role != self.user_role:
                        return JsonResponse({
                            "status": "Error",
                            "msg": self.error_messages.get("wrong_role_user")
                        })

                    return func(self, request, *args, **kwargs)
            except Exception as e:
                return JsonResponse({
                    "status": "Error",
                    "msg": str(e),
                })
        return _wrapped_view

    def update_get_context(self, request, *args, **kwargs):
        """
            main content define here
        """
        return None

    def update_post_context(self, request, *args, **kwargs):
        """
            main content define here
        """
        return None

    def prepare_context(self, request, *args, **kwargs):
        """
            prepare context for all request type
        """
        self.context = {}
        self.context["user"] = request.user
        self.context["direct_url"] = self.direct_url
        self.context["request"] = self.request

    @method_decorator(login_required)
    @role_required_decorator
    def get(self, request, *args, **kwargs):
        """
            Default get processing
        """
        self.prepare_context(request)
        if self.form is None:
            self.update_get_context(request, *args, **kwargs)
            return render(request, self.template_path, self.context)
        form = self.form()
        self.context["form"] = form
        self.update_get_context(request, *args, **kwargs)

        return render(request, self.template_path, self.context)

    @method_decorator(login_required)
    @role_required_decorator
    def post(self, request, *args, **kwargs):
        """
            Default post processing
        """
        self.prepare_context(request)

        form = self.form(request.POST)
        self.context["form"] = form

        if form.is_valid():
            self.cleaned_data = form.cleaned_data
            self.update_post_context(request, *args, **kwargs)
        return render(request, self.template_path, self.context)


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main_customer')
    else:
        form = SignUpForm()
    return render(request, "boec_core/user_base/signup.html", {'form': form})


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('main_customer')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'boec_core/user_base/edit_profile.html', args)


def get_user_role_root_path(user):
    if user.role == 2:
        return "/boec/admin/oders/"
    if user.role == 3:
        return "/boec_admin/productlist/"   
    return "/boec/customer"
