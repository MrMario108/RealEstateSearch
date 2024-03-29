from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import viewsets
from datetime import datetime
from .forms import (LoginForm, ProfileEditForm, SearchingSettingsForm,
                    UserEditForm, UserRegistrationForm)
from .models import Apartment, City, Profile, SearchingSettings, Category
from .serializer import ApartmentSerializer, SearchingSettingsSerializer
#from scrapingApp.utils.worker import Starter
from scrapingApp.tasks import startScraperTasks
import logging

logger = logging.getLogger('django')

@login_required
def olxSearch(request):
    """ Main site """
  
    # query the db to return all project objects
    advaresments = Apartment.objects.all()
    
    # w plikac template mamy dostęp do danych poprzez zadeklarowaną wartość 'allRealEstates'
    return render(request, 'olxSearch/index.html', {'allRealEstates': advaresments})

@login_required
def change_pass(request):
    return render(request, 'olxSearch/registration/password_change_form.html', {'allRealEstates': 0})


@login_required
def realEstateList(request):
    """ Real Estate list of loged user"""

    searchingSettingsList = SearchingSettings.objects.filter(user__pk = request.user.id)
    
    if len(searchingSettingsList) > 0:
    
        first = searchingSettingsList[0]
        advaresments = Apartment.objects.filter(city = first.city, rooms = first.rooms, category = first.category, price__lte = first.price)
        
        return render(request, 'olxSearch/index.html', {'allRealEstates': advaresments, 'searchingSettingsList': searchingSettingsList})

    else:

        return render(request, 'olxSearch/index.html', {'allRealEstates': 0})

@login_required
def realEstateListFiltered(request, pk):
    """ Real Estate list of loged user"""

    
    searchingSettingsList = SearchingSettings.objects.filter(pk = pk)
    
    if len(searchingSettingsList) > 0:
    
        first = searchingSettingsList[0]
        advaresments = Apartment.objects.filter(city = first.city, rooms = first.rooms, category = first.category) #, price__lte = first.price

        return render(request, 'olxSearch/index.html', {'allRealEstates': advaresments, 'searchingSettingsList': searchingSettingsList})

    else:
        return render(request, 'olxSearch/index.html', {'allRealEstates': 0})



class ApartmentViewSet(viewsets.ModelViewSet):
    """ Viewsets for serialization """

    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

class SearchingSettingsViewSet(viewsets.ModelViewSet):
    """ Viewsets for serialization """

    queryset = SearchingSettings.objects.all()
    serializer_class = SearchingSettingsSerializer


# for edit - not all done yet - edit data_publish 
class SaveApartment():
    """ Save the new advs in the database """

    def saveNewAdvs(request, data):
        """Save the new advs in the database"""

        forSave = Apartment()

        forSave.advId = data['advId']
        forSave.link = data['link']
        forSave.pic = data['pic']
        forSave.title = data['title']
        forSave.price = data['price']
        # date_published = models.DateTimeField('date published')
        forSave.date_published = data['date_published']
        forSave.area = data['area']
        forSave.type = data['type']
        forSave.rooms = data['rooms']

        forSave.save()


# for edit - not all done yet
def user_login(request):
    """ Login user """

    if request.method == 'POST':
        form = LoginForm(request.POST)
    
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],    # zwaraca dane o użytkowniku który ma username ==username
            password=cd['password'])
    
            if user is not None:
    
                if user.is_active:
                    login(request, user)                    # umieszcza usera w sesji :)
    
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
    
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()

    return render(request, 'olxSearch/login.html', {'form': form})


def register(request):
    """ Create a new user account and his profile. """

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
    
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika; jednak jeszcze nie zapisujemy go w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(user_form.cleaned_data['password'])
            # Zapisanie obiektu User.
            new_user.save()
            # Utworzenie profilu użytkownika.
            profile = Profile.objects.create(user=new_user)
    
            return render(request, 'olxSearch/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'olxSearch/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """ Edit user and its profile."""

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return render(request, 'olxSearch/dashboard.html', {'section': 'dashboard'})

    else:
        try:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        except:
            return render(request, 'olxSearch/dashboard.html', {'section': 'dashboard', 'info': 'You have to fill your profile first! Please contact with admin!'})

    return render(request,'olxSearch/edit.html',{'user_form': user_form,'profile_form': profile_form})


# for edit - not all done yet
@login_required
def searchingSettingsEditView(request, pk):
    """ Edit one searching settings """
    
    instance = SearchingSettings.objects.get(id=pk)

    if request.method == 'POST':
        
        searchSet_form = SearchingSettingsForm(instance=instance, data=request.POST)

        if searchSet_form.is_valid():
            searchSet_form.save()

            return searchingSettingsListView(request)
    else:
        searchSet_form = SearchingSettingsForm(instance=instance)
        
    return render(request, 'olxSearch/searchingSettingsEdit.html', {'searchSet_form': searchSet_form})

# for edit - not all done yet
@login_required
def searchingSettingsDeleteView(request, pk):
    """ Delete chosen searching setting """

    instance = SearchingSettings.objects.get(id=pk)
    instance.delete()

    return searchingSettingsListView(request)


@login_required
def searchingSettingsNewView(request):
    """ Save a new searching settings and go to list of searching settings """

    if request.method == 'POST':
        searchSet_form = SearchingSettingsForm(request.POST)

        if searchSet_form.is_valid():
            searchSet = searchSet_form.save(commit=False)
            searchSet.user = request.user
            searchSet.data_created = timezone.now()
            searchSet.save()
        
        
        return searchingSettingsListView(request)

    else:
        searchSet_form = SearchingSettingsForm()
       
    return render(request,'olxSearch/searchingSettingsNew.html',{'searchSet_form': searchSet_form})


@login_required
def searchingSettingsListView(request):
    """  Return a list of search settings for loged user"""

    searchingSettingsList = SearchingSettings.objects.filter(user__pk = request.user.id)

    return render(request,'olxSearch/searchingSettingsList.html',{'searchingSettingsList': searchingSettingsList})

def default(request):
    """ Default view """

    return render(request, 'olxSearch/index.html')

def testScrapy(request):
    """ Test scrapy """

    logger.info(str(datetime.now()) + "\t testScrap was runed")
    startScraperTasks()

    return render(request, 'olxSearch/index.html', {'testScrap': ['test',], 'allRealEstates':'', 'searchingSettingsList':[]})