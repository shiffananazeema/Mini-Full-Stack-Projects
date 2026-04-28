from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_expense, name="add_expense"),
    path("edit/<int:expense_id>/", views.edit_expense, name="edit_expense"),
    path("delete/<int:expense_id>/", views.delete_expense, name="delete_expense"),
    path(
        "login/",
        LoginView.as_view(
            template_name="expenses/auth_form.html",
            authentication_form=LoginForm,
            extra_context={"title": "Login", "button_text": "Login"},
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
