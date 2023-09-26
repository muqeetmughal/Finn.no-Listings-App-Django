from django import forms
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import Listing, Price_History
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from time import sleep
# from .finn_v3 import FinnScraper
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ListingFilter
# Create your views here.
from django.db.models import Prefetch


@login_required(login_url='login')
def home(request):
    # listing = Listing.objects.prefetch_related('history').order_by("last_updated")
    listing = Listing.objects.prefetch_related(
        Prefetch('history', queryset=Price_History.objects.order_by('-id'))
    ).order_by("-id")
    myfilter = ListingFilter(request.GET,queryset=listing)
    listing = myfilter.qs

    page_num = request.GET.get('page')
    data_paginator = Paginator(listing, 10)

    try:
        listing = data_paginator.page(page_num)
    except PageNotAnInteger:
        listing = data_paginator.page(1)
    except EmptyPage:
        listing = data_paginator.page(data_paginator.num_pages)


    page = data_paginator.get_page(page_num)
    context = {
        "page": page,
        "count": data_paginator.count,
        "myfilter":myfilter,
        }
    return render(request, "home.html", context)


@login_required(login_url='login')
def details_redirect(request):

    return redirect("home")


# @login_required(login_url='login')
# def start_scraper(request):
#     scrape = FinnScraper()
#     scrape.new_data_today()
#     return HttpResponse("<h1>New Data Scrape Completed</h1>")



# @login_required(login_url='login')
# def old_scraper(request):
#     scrape2 = FinnScraper()
#     scrape2.old_data()
#     # scrape.scrape_single_listing("https://www.finn.no/boat/forsale/ad.html?finnkode=207958480")
#     return HttpResponse("<h1>Old DataScrape Completed</h1>")


@login_required(login_url='login')
def details(request, code):
    # try:
    #     scrape = FinnScraper()
    #     scrape.scrape_single_listing(
    #     "https://www.finn.no/boat/forsale/ad.html?finnkode={}".format(str(code)))
    # except:
    #     pass

    Details = Listing.objects.prefetch_related('history').get(finn_code=code)
    # PriceHistory = Price_History.objects.filter(finn_code=code)
    # print(len(PriceHistory))
    print(Details)
    context = {
        "Details": Details,
        # "PriceHistory": PriceHistory,
    }
    return render(request, "details.html", context)

@login_required(login_url='login')
def delete_detail(request, code):

    Details = Listing.objects.get(finn_code=code)
    Details.delete()
    PriceHistory = Price_History.objects.get(finn_code=code)
    PriceHistory.delete()
    # print(len(PriceHistory))
    # print(Details)
    return redirect("home")


@login_required(login_url='login')
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['finn_code', 'title', 'Boat_location','State','Type','Brand','Model','Model_Year','Length_feet','Length_cm','Width','Depth','Engine_Included','Engine_Manufacturer','Engine_Type','Motorstr','Max_Speed','Fuel','Weight','Material','Color','Seating','Sleeps','orignal_price','last_changed','contact_name','phone_number','address','last_updated','url','status'])

    for item in Listing.objects.all().values_list('finn_code', 'title', 'Boat_location','State','Type','Brand','Model','Model_Year','Length_feet','Length_cm','Width','Depth','Engine_Included','Engine_Manufacturer','Engine_Type','Motorstr','Max_Speed','Fuel','Weight','Material','Color','Seating','Sleeps','orignal_price','last_changed','contact_name','phone_number','address','last_updated','url','status'):
        writer.writerow(item)

    response['Content-Disposition'] = 'attachment; filename="table_data.csv"'

    return response


def login_handler(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logout_handler(request):
    logout(request)
    return redirect("login")
