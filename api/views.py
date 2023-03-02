from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from webapp.models import Listing, Price_History
from .serializers import ListingSerializer, PriceSerializer
from webapp.filters import ListingFilter
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication



class ListingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]



class PriceHistoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Price_History.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [AllowAny]