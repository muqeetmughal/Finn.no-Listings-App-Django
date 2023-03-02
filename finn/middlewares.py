from .script import FinnScraper
from webapp.models import Listing
from django.db import close_old_connections
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.scraper = FinnScraper()
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        path = str(request.path)

        if "/admin/webapp/listing" in path and  "change" in path:
            listing_id = int(path.split("/")[-3])
            print(listing_id)
            listing = Listing.objects.get(pk=listing_id)
            print(listing.url)

            self.scraper.scrape_single_listing(listing.url)
            close_old_connections()
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response