from django.conf.urls import url

from . import views

urlpatterns = [
    url('^metadata.js$', views.metadata, name='shortcodes_metadata'),
    url('^dialog/(?P<name>\w+)',  views.dialog, name='shortcodes_dialog'),
    url('^insert/(?P<name>\w+)/(?P<pending_id>\w+)', views.insert_shortcode,
        name='insert_shortcode'),
]
