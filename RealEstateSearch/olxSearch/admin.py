from django.contrib import admin
from .models import Category, City, Apartment, Profile, SearchingSettings, BuildingType

# Register your models here.

admin.site.register(Apartment)
admin.site.register(SearchingSettings)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(BuildingType)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']