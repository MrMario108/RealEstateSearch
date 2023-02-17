from django.urls import path, include
from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'olxSearch', views.ApartmentViewSet)
router.register(r'searchingSettingsApi', views.SearchingSettingsViewSet)

#app_name = 'olxSearch'

urlpatterns = [
    path('api/', include(router.urls), name='search'),
    #path('api2/', include(router.urls), name='searchingSettingsApi'),
    
    path('',views.realEstateList, name='dashboard'),
    path('<int:pk>/',views.realEstateListFiltered, name='realEstateListFiltered'),
    path('', include('django.contrib.auth.urls')),

    # path for Users edit, register
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('change/', views.change_pass, name='change_pass'),

    # path for searching settings
    path('searchingSettingsNew/', views.searchingSettingsNewView, name='searchingSettingsNew'),
    path('searchingSettingsList/', views.searchingSettingsListView, name='searchingSettingsList'),
    path('searchingSettingsDelete/<int:pk>/', views.searchingSettingsDeleteView, name='searchingSettingsDelete'),
    path('searchingSettingsEdit/<int:pk>/', views.searchingSettingsEditView, name='searchingSettingsEdit'),
]

    #path('<int:pk>', views.realEstatesDetails, name='realEstatesDetails'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

