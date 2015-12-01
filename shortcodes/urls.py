from django.conf.urls import url

from . import views

urlpatterns = [
    url('^metadata.js$', views.metadata, name='metadata'),
    url('^dialog/(?P<name>\w+)',  views.new, name='new'),
]
