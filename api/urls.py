
from django.urls import path,include
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'listings', ListingViewSet)
router.register(r'history', PriceHistoryViewSet)
urlpatterns = router.urls