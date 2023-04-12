from .models import Apartment, SearchingSettings, Category, City
from rest_framework import serializers

class ApartmentSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(slug_field='categoryName', queryset=Category.objects.all())
    city = serializers.SlugRelatedField(slug_field='slug', queryset=City.objects.all())

    class Meta:
        model = Apartment
        #fields = '__all__'
        fields = ['advId', 'title', 'link', 'pic', 'price', 'date_published', 'rooms', 'area', 'city', 'category']


class SearchingSettingsSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.SlugRelatedField(slug_field='slug', queryset=City.objects.all())
    category = serializers.SlugRelatedField(slug_field='categoryName', queryset=Category.objects.all())

    class Meta:
        model = SearchingSettings
        fields = ('category', 'price', 'rooms', 'area', 'city')


#  examples
# SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='title'
# 
# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
# 
#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']

# class AlbumSerializer(serializers.HyperlinkedModelSerializer):
#    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')
#
#    class Meta:
#        model = Album
#        fields = ['album_name', 'artist', 'track_listing']
#
#class AlbumSerializer(serializers.ModelSerializer):
#    tracks = serializers.StringRelatedField(many=True)
#
#    class Meta:
#        model = Album
#        fields = ['album_name', 'artist', 'tracks']