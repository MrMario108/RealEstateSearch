from django.contrib import admin
from .models import Apartment, Profile, SearchingSettings

# Register your models here.

admin.site.register(Apartment)
admin.site.register(SearchingSettings)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']