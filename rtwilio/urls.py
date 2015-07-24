from django.conf.urls import url

from rtwilio import views


urlpatterns = [
    url(r'^status-callback/$', views.status_callback, name='twilio-status-callback'),
    url(r'^$',
        views.validate_twilio_signature(views.TwilioBackendView.as_view()), name='twilio-backend'),
]
