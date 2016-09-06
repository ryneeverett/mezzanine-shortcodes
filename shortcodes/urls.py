from django.conf.urls import url

from . import views

urlpatterns = [
    url('^metadata.js$', views.metadata, name='shortcodes_metadata'),
    url('^dialog/(?P<name>\w+)',  views.dialog, name='shortcodes_dialog'),
]
