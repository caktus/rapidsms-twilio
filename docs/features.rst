Status Callback
---------------

RapidSMS can take advantage of Twilio's `status callback
<http://www.twilio.com/docs/api/rest/sending-sms#post-parameters-optional>`_.
This is useful if you'd like to track the status of a message after it's been
passed to Twilio for processing. Twilio will use a callback URL to notify us.
Enabling this feature will allow you to view delivery reports, for each
message, in the Django admin.

1. Make sure ``rtwilio`` is in ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # other apps
        'rtwilio',
    )

2. Add the callback view to your urlconf. If you are including all of the urls this
is already handled for you::

    urlpatterns = [
        # ...
        url(r'^backend/twilio/', include('rtwilio.urls')),
    ]

3. Add the necessary database tables::

    python manage.py migrate rtwilio

4. Add the full callback URL to your settings::

    INSTALLED_BACKENDS = {
        # ...
        # other backends, if any
        "twilio-backend": {
            "ENGINE": "rtwilio.outgoing.TwilioBackend",
            'config': {
                # same as before..
                'callback': 'http://<public-django-instance>/backend/twilio/status-callback/',
            }
        },
    }

You can view delivery reports in the Django admin.
