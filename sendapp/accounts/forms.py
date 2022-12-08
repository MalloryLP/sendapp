from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
  
class CustomUserRegisterForm(UserCreationForm):  
    username = forms.CharField(label='Username', min_length=5, max_length=150, widget=forms.TextInput(attrs={   'class': "input-form",
                                                                                                                'placeholder': 'Username',
                                                                                                                'style': "--top_level: 1vh;"}))  
    
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={  'class': "input-form",
                                                                            'placeholder': 'Email',
                                                                            'style': "--top_level: 16vh;"}))

    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={ 'class': "input-form",
                                                                                    'placeholder': 'Prénom',
                                                                                    'style': "--top_level: 6vh;"}))

    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={   'class': "input-form",
                                                                                    'placeholder': 'Nom',
                                                                                    'style': "--top_level: 11vh;"}))

    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={  'class': "input-form",
                                                                                            'placeholder': 'Mot de passe',
                                                                                            'style': "--top_level: 21vh;"})) 

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': "input-form",
                                                                                            'placeholder': 'Confirmation du mot de passe',
                                                                                            'style': "--top_level: 26vh;"}))  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email
    
    def first_name_clean(self):  
        first_name = self.cleaned_data['first_name'].lower()
        return first_name 

    def last_name_clean(self):  
        last_name = self.cleaned_data['last_name'].lower()
        return last_name 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            username = self.cleaned_data['username'],  
            email = self.cleaned_data['email'],  
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']
        )  
        return user  