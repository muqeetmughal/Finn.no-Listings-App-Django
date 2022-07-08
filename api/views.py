from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from webapp.models import Listing, Price_History
from .serializers import ListingSerializer, PriceSerializer
from webapp.filters import ListingFilter
from webapp.finn_v3 import FinnScraper
from rest_framework import generics
import csv
from rest_framework.authentication import SessionAuthentication
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        "listings" : '/api/listings/',
        "listing detail" : '/api/listing/<str:pk>',
        "create listing" : '/api/listing-create/',
        "delete listing" : '/api/listing-delete/<str:pk>',
    }
    return Response(api_urls)
    
@api_view(['GET'])
def start_scraper(request):
    scrape = FinnScraper()
    scrape.new_data_today()
    return Response("Today Scrape Completed")


@api_view(['GET'])
def old_scraper(request):
    scrape = FinnScraper()
    scrape.old_data()
    return Response("Old Scrape Completed")

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,code):
    Details = Listing.objects.get(finn_code=code)
    Details.delete()
    PriceHistory = Price_History.objects.filter(finn_code=code)
    PriceHistory.delete()
    return Response("Deleted")


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def listings(request):
    listing = Listing.objects.all().order_by("last_updated")
    
    myfilter = ListingFilter(request.GET,queryset=listing)
    listing = myfilter.qs


    page_num = request.GET.get('page')
    length_of_data = request.GET.get('length')
    if length_of_data is None:
        length_of_data = 10
    else:
        length_of_data = length_of_data
    data_paginator = Paginator(listing, length_of_data)
    try:
        listing = data_paginator.page(page_num)
    except PageNotAnInteger:
        listing = data_paginator.page(1)
    except EmptyPage:
        listing = data_paginator.page(data_paginator.num_pages)


    
    page = data_paginator.get_page(page_num)
    list_serializer = ListingSerializer(listing, many=True)


    total_records = page.paginator.count
    num_pages = page.paginator.num_pages

    if page.has_next():
        next_page = page.next_page_number()
    else:
        next_page = page.paginator.num_pages


    if page.has_previous():
        previous_page = page.previous_page_number()
    else:
        previous_page = 1

    output = {
        'previous_page' : previous_page,
        'current_page' : page.number,
        'next_page' : next_page,
        'total_pages' : num_pages,
        'total_records' : total_records,
        'records' : list_serializer.data,  
    }
    return Response(output)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def detail(request,code):
    try:
        scrape = FinnScraper()
        scrape.scrape_single_listing("https://www.finn.no/boat/forsale/ad.html?finnkode={}".format(str(code)))
    except:
        pass
    Details = Listing.objects.get(finn_code=code)
    PriceHistory = Price_History.objects.filter(finn_code=code)
    print("Price Length",len(PriceHistory))
    detail_serializer = ListingSerializer(Details, many=False).data
    price_serializer = PriceSerializer(PriceHistory, many=True).data

    detail_serializer['prices'] = price_serializer

    return Response(detail_serializer)



@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['finn_code', 'title', 'Boat_location','State','Type','Brand','Model','Model_Year','Length_feet','Length_cm','Width','Depth','Engine_Included','Engine_Manufacturer','Engine_Type','Motorstr','Max_Speed','Fuel','Weight','Material','Color','Seating','Sleeps','orignal_price','last_changed','contact_name','phone_number','address','last_updated','url','status'])

    for item in Listing.objects.all().values_list('finn_code', 'title', 'Boat_location','State','Type','Brand','Model','Model_Year','Length_feet','Length_cm','Width','Depth','Engine_Included','Engine_Manufacturer','Engine_Type','Motorstr','Max_Speed','Fuel','Weight','Material','Color','Seating','Sleeps','orignal_price','last_changed','contact_name','phone_number','address','last_updated','url','status'):
        writer.writerow(item)

    response['Content-Disposition'] = 'attachment; filename="table_data.csv"'

    return response

