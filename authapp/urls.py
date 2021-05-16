from django.urls import path
import authapp.views

urlpatterns = [
    path("login/", authapp.views.login),
    path("login/", authapp.views.logout),
]