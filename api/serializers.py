from rest_framework import serializers
from webapp.models import Listing, Price_History

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price_History
        fields = '__all__'
