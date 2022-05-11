from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from .models import Tweet, Profile

class DateInput(forms.DateInput):
    input_type = 'date'

class Signupform(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1','password2']
        labels = {'first_name': "First Name",'last_name': "Last Name", "email": "Email-Id", "username": "Username", "password1":"Password", 'password2': "Confirm Password"}
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'auto-focus':False}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
class Loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'auto-focus':True, 'class':'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'auto-complete': 'current-password'}))

# class Loginform(forms.Form):
#     username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control', 'auto-focus':True}))
#     password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'auto-complete': 'current-password'}))

# class Loginform(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password1']
#         labels = {"username": "Username", "password1":"Password"}
#         widgets = {
#             'username': forms.TextInput(attrs={'class':'form-control', 'auto-focus':True}),
#             'password1': forms.PasswordInput(attrs={'class':'form-control', 'auto-complete': 'current-password'}),
#             }

    
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['post_text', 'post_image']
        widgets = {
            'post_text' : forms.Textarea(attrs={'placeholder':"Share Something Here...", 'class':'form-control text-class','id':'text-area-input', 'cols':100,'rows':4}),
            'post_image' : forms.FileInput(attrs={'class':'image-class', 'onchange':'donef(event)'}),
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'bio', 'location', 'profile_image']
        labels = {'dob':"Date of Birth", 'bio': 'Bio', 'location':'Location'}
        widgets = {
            'dob' : DateInput(attrs={'class':'form-control'}),
            'bio' : forms.Textarea(attrs={'placeholder':"Something About Your Self...", 'class':'form-control text-class', 'cols':60,'rows':3}),
            'location' : forms.TextInput(attrs={'class':'form-control', 'placeholder':"City - Country"}),
            'profile_image' : forms.FileInput(attrs={'class':'image-class', 'onchange':'pro_pic(event)'}),
        }
        
class PasswordChangeform(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'auto-complete': 'current-password'}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput( attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput( attrs={'class':'form-control'}))