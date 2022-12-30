
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('auth_app.urls')),
    # path('accounts',include('django.contrib.auth.urls')),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name='auth_app/passwords/password_reset_done.html'),name='password-reset-done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetCompleteView.as_view(template_name='auth_app/passwords/password_reset_confirm.html'),name='password-reset-confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='auth_app/passwords/password_reset_complete.html'),name='password-reset-complete'),
]
