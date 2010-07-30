from django.conf.urls.defaults import *

from rtwilio import views


urlpatterns = patterns('',
    url(r'^twilio/status-callback/$', views.status_callback,
        name='status-callback'),
)
