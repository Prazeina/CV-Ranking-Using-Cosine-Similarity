from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm #inherits from usercreation form
from .models import Profile


class UserRegisterForm(UserCreationForm): #call userregister form inherit from user creation form
    email = forms.EmailField()
    # address = forms.CharField(max_length=200)
    # phone = PhoneField(blank=True, help_text='Contact phone number')

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phone', 'password1', 'type']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phone']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile     #model that we wanna work with is model
        fields = ['image']   #fields we wanna work with






