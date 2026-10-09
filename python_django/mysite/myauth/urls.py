from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (set_cookie_view, get_cookie_view, set_session_view,
                    get_session_view, my_logout_view, AboutmeView,
                    RegisterView, UserListView, UserDetailView,
                    UpdateUserView)

app_name = 'myauth'

urlpatterns = [
    path("",
         LoginView.as_view(
             redirect_authenticated_user=True,
             template_name='myauth/login.html'),
         name="login"),
    path("logout/", my_logout_view, name="logout"),
    path("about-me/", AboutmeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("set/", set_cookie_view, name="set-cookie"),
    path("get/", get_cookie_view, name="get-cookie"),
    path("set-s/", set_session_view, name="set-session"),
    path("get-s/", get_session_view, name="get-session"),
    path("users-list/", UserListView.as_view(), name="users-list"),
    path("users-detail/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("user-update/<int:pk>/", UpdateUserView.as_view(), name="user-update"),
]