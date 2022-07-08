from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('webapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',TemplateView.as_view(template_name='index.html')),
    path('login/',TemplateView.as_view(template_name='index.html')),
    path('details/<str:finn_code>',TemplateView.as_view(template_name='index.html')),
    path('api/',include('api.urls'))
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
