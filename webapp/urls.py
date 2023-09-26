from pathlib import Path
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.details_redirect, name='detail_redirect'),
    path('detail/<int:code>/', views.details, name='detail'),
    # path('todayscrape', views.start_scraper, name="today_scrape"),
    # path('oldscrape', views.old_scraper, name="old_scrape"),
    path('login', views.login_handler, name="login"),
    path('logout', views.logout_handler, name="logout"),
    path('delete/<int:code>/', views.delete_detail, name="delete"),
    path('exportcsv', views.export_to_csv, name="csvExport")
]
