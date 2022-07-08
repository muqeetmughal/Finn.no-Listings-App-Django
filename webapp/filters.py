import django_filters
from django_filters import *
from .models import Listing


class ListingFilter(django_filters.FilterSet):
    finn_code = CharFilter(field_name='finn_code',lookup_expr='icontains',label="Finncode")
    title = CharFilter(field_name='title',lookup_expr='icontains',label="title")
    description = CharFilter(field_name='description',lookup_expr='icontains',label="description")
    State = CharFilter(field_name='State',lookup_expr='icontains',label="State")
    Type = CharFilter(field_name='Type',lookup_expr='icontains',label="Type")
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['definitions_html','last_changed','url','phone_number','address','contact_name']
        