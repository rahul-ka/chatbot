from django.conf.urls import url
from .views import index, response

urlpatterns = [
    
 	url(r'^index/$', index, name='index'),
 ]