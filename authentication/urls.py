from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
] + static(settings.STATIC_URL, documents_root = settings.STATIC_ROOT)