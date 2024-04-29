from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path("register/", user_register_view, name="user_register_view"),
    path("login/", user_login_view, name="user_login_view"),
    path("logout/", user_logout_view, name="user_logout_view"),
    path("verify_email/<str:token>/", verify_email_view, name="verify_email"),
    path("profile/", user_profile_detail_view, name="user_profile_detail_view"),
    path("profile/edit/", user_profile_edit_view, name="user_profile_edit_view"),
]
