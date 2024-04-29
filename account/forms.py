from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs = {"class":"form-control"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))

class UserSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs = {"class":"form-control"}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs = {"class":"form-control"}))
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput(attrs = {"class":"form-control"}))
    
    class Meta:
        model = User
        fields = ('first_name' , 'last_name', 'username' , 'email' , 'registration_no' , 'password1' , 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = "__all__"
