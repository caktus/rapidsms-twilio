from django.conf.urls.defaults import *

from rtwilio import views


urlpatterns = patterns('',
    url(r"^(?P<backend_name>[\w-]+)/$", views.TwilioBackendView.as_view(),
        name='twilio-backend'),
    url(r'^twilio/status-callback/$', views.status_callback,
        name='status-callback'),
)
