
from django.conf.urls import url, include
from rest_framework import routers
from event.api import views as api_views
from django.views.decorators.csrf import csrf_exempt




router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/customer_add/',csrf_exempt(api_views.CustomerAddAPIView.as_view())),
    url(r'^api/login_api/',api_views.LoginAPIView.as_view()),
    url(r'^api/event_type/',api_views.EventAPIView.as_view()),
    url(r'^api/venue/',api_views.VenueAPIView.as_view()),
    url(r'^api/price/',api_views.EstimatedPriceAPIView.as_view()),
    url(r'^api/event/',api_views.EventsAPIView.as_view()),


    
]