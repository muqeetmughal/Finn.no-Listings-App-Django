
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',apiOverview),
    path('listings/',listings),
    path('detail/<int:code>/', detail),
    path('delete/<int:code>/', delete),
    path('today/', start_scraper),
	path('old/', old_scraper),
    path('export/', export_to_csv),
]
