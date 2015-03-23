from django.conf.urls import url

from rtwilio import views


urlpatterns = [
    url(r'^status-callback/$', views.status_callback,
        name='rtwilio-status-callback'),
    url(r'^$',
        views.TwilioBackendView.as_view(backend_name='rtwilio-backend'),
        name='rtwilio-backend'),
]
