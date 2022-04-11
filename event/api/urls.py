
from django.conf.urls import url, include
from rest_framework import routers
from event.api import views as api_views



router = routers.DefaultRouter()

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^api/customer_add/',api_views.CustomerAddAPIView.as_view()),

    url(r'^api/login_api/',api_views.LoginAPIView.as_view()),

]