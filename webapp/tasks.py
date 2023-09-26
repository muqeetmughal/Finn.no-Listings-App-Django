from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from webapp.models import Listing, Price_History
from webapp.scraper_latest import FinnScraper
from django.utils.timezone import now
from datetime import timedelta


@shared_task
def scrape_single_listing_task(url):
    scraper = FinnScraper()
    scraper.scrape_single_listing(url)


@shared_task()
def update_old_data():
    last_month = now().date() - timedelta(days=90)

    listings = Listing.objects.filter(
        last_changed_datetime__gte=last_month
    ).prefetch_related("history")

    for listing in listings:
        print("Sending Task for: ", listing.url)
        scrape_single_listing_task.delay(listing.url)
        sleep(2)


@shared_task()
def start_scrape_new_data():
    scraper = FinnScraper()
    scraper.scrape_data(old=False)


@shared_task()
def start_scrape_old_data():
    scraper = FinnScraper()
    scraper.scrape_data(old=True)
