from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from django.http import HttpRequest, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import UserUpdateForm

from .models import Profile

# Create your views here.
class AboutmeView(UpdateView):
    template_name = "myauth/about-me.html"
    fields = ("avatar",)
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        return self.request.user.profile

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        Profile.objects.create(user=self.object)
        user = authenticate(
            username=username
            ,password=password
        )
        login(request=self.request, user=user)
        return response


def set_cookie_view(request: HttpRequest):
    response = HttpResponse("Cookie set")
    response.set_cookie('one', 'two', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest):
    value = request.COOKIES.get('one', 'without number')
    return HttpResponse(f'Cookie value: {value!r}')

def set_session_view(request: HttpRequest):
    request.session["number"] = "one"
    return HttpResponse("Session set")

def get_session_view(request: HttpRequest):
    return HttpResponse(f'Session value: '
                        f'{request.session.get(
                            'number',
                            'without number')!r}')

def my_logout_view(request):
    logout(request)
    return redirect(reverse_lazy("myauth:login"))

class UserDetailView(DetailView):
    template_name = "myauth/user-detail.html"
    queryset = (
        User.objects
        .select_related("profile")
    )
    context_object_name = "user"

class UserListView(ListView):
    template_name = "myauth/user-list.html"
    queryset = (
        User.objects
        .select_related("profile")
    )
    context_object_name = "users"

class UpdateUserView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff or User.pk == self.request.user.pk

    template_name = "myauth/update-user.html"
    queryset = User.objects.select_related("profile")
    form_class = UserUpdateForm
    success_url = reverse_lazy("myauth:users-list")
