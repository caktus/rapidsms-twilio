from django.conf.urls import patterns, url

from rtwilio.views import TwilioBackendView


urlpatterns = patterns('',  # nopep8
    url(r"^backend/twilio/$",
        TwilioBackendView.as_view(backend_name='rtwilio-backend'),
        name='rtwilio-backend'),
)
