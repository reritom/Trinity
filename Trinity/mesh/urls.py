from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'go/', views.gogo, name='gogo'),
    url(r'examples/', views.examples, name='examples'),
]
