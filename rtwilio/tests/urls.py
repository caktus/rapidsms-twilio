from django.conf.urls import include, url


urlpatterns = [
    url(r'^backend/twilio/', include('rtwilio.urls')),
]
