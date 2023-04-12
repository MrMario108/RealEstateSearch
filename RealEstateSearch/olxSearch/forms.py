from django import forms
from django.contrib.auth.models import User
from .models import Profile, SearchingSettings, City
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    #email = forms.CharField(widget=forms.EmailInput())


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Hasła nie są identyczne.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class SearchingSettingsForm(forms.ModelForm):
    """ Form for create and edit searching settings """
    class Meta:
        model = SearchingSettings
        #fields = '__all__'

        fields = ('title','category', 'city', 'rooms', 'price', 'area' )
                
        labels = {
            'title': _('Tytuł'),
            'category': _('Rodzaj nieruchomości'),
            'city': _('Miasto'),
            'rooms': _('Ilość pokoi'),
            'price': _('Maks. cena za m2:'),
            'area': _('Powierzchnia do:'),
            
        }
        help_texts = {
            'title': _('Musisz wpisać jakąś nazwę.'),
        }
        error_messages = {
            'title': {
                'max_length': _("Tytuł jest za długi."),
            },
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__' #('cityName')
        labels = {
            'cityName': _('Miasto'),
        }
        widgets = {
            'cityName': forms.Select()
        }
