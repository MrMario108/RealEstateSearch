from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'olxSearch', views.ApartmentViewSet)
router.register(r'searchingSettingsApi', views.SearchingSettingsViewSet)

#app_name = 'olxSearch'

urlpatterns = [
    path('api/', include(router.urls), name='search'),
    #path('api2/', include(router.urls), name='searchingSettingsApi'),
    
    path('home/',views.realEstateList, name='dashboard'),
    path('',views.realEstateList, name='dashboard'),
    path('<int:pk>/',views.realEstateListFiltered, name='realEstateListFiltered'),
    path('', include('django.contrib.auth.urls')),

    # path for Users edit, register
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('change/', views.change_pass, name='change_pass'),
    path('default/', views.default, name='default'),
    #path('contact/', views.contact, name='contact'),
    path('contact/', TemplateView.as_view(template_name="olxSearch/contact.html"), name='contact'),
    path('testScrap/', views.testScrapy, name='testScrap'),

    # path for searching settings
    path('searchingSettingsNew/', views.searchingSettingsNewView, name='searchingSettingsNew'),
    path('searchingSettingsList/', views.searchingSettingsListView, name='searchingSettingsList'),
    path('searchingSettingsDelete/<int:pk>/', views.searchingSettingsDeleteView, name='searchingSettingsDelete'),
    path('searchingSettingsEdit/<int:pk>/', views.searchingSettingsEditView, name='searchingSettingsEdit'),
]
