from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainDocs, name='mainDocs'),
    url(r'^examples/$', views.exampleDocs, name='exampleDocs')
]
