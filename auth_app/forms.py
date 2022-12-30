from django.forms import Form,CharField,PasswordInput,EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(Form):
    username=CharField(max_length=50)
    password=CharField(widget=PasswordInput())

class PasswordResetForm(Form):
    email=EmailField(max_length=100)

class NewUserCreationForm(UserCreationForm):
    email=EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def save(self,commit=True):
        # commit=False creates an instance 
        user=super(NewUserCreationForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user