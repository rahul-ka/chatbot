from django.conf.urls import url
from .views import response

urlpatterns = [
 	url(r'^message/$', response, name='response'),
 ]