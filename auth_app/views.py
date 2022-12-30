from django.shortcuts import render,HttpResponse,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from .forms import NewUserCreationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError

# Create your views here.
@login_required
def Homepage(request):
    template='auth_app/home.html'
    return render(request,template)

def LoginView(request):
    if request.method=='POST':
        # data entry
        form=LoginForm(request.POST)
        # data matches form widget
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            # looks for a user with such credentials
            user=authenticate(
                request,
                username=username,
                password=password
            )
         # logs a user in
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse('User not found')
    else:
        form=LoginForm()
    template='auth_app/login.html'
    context={'form':form}
    return render(request,template,context)

def LogoutView(request):
    logout(request)
    return redirect('login')

def RegisterView(request):
    if request.method=='POST':
        form=NewUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse('form is invalid')
    else:
        form=NewUserCreationForm()
    template='auth_app/register.html'
    context={'form':form}
    return render(request,template,context)

def PasswordResetView(request):
    if request.method=='POST':
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth_app/passwords/password_reset_email.txt"
                    info = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, info)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password-reset-done")
            else:
                return HttpResponse('user not found')        
    else:    
        form=PasswordResetForm()
    template='auth_app/passwords/password_reset.html'
    context={'form':form}
    return render(request,template,context)
