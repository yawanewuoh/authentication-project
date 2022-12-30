from django.urls import path
from .views import  Homepage,LoginView,LogoutView,RegisterView,PasswordResetView

urlpatterns=[
    path('',Homepage,name='home'),
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('register/',RegisterView,name='register'),
    path('password_reset/',PasswordResetView,name='password-reset'),
]