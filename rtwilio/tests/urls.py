from django.conf.urls import patterns, url

from rtwilio.views import TwilioBackendView, status_callback


urlpatterns = patterns('',  # nopep8
    url(r"^backend/twilio/$",
        TwilioBackendView.as_view(backend_name='rtwilio-backend'),
        name='rtwilio-backend'),
    url(r'^backend/twilio/status-callback/$', status_callback,
        name='twilio-status-callback'),
)
