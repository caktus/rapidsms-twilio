Getting Started and Setup
=========================

Below are the basic steps need to get rapidsms-twilio integrated into your
RapidSMS project.

Install ``rapidsms-twilio``::

    pip install rapidsms-twilio

Add ``rtwilio`` to your ``INSTALLED_APPS`` in your ``settings.py`` file::

    INSTALLED_APPS = (
        # other apps
        'rtwilio',
    )

Add the following to your existing ``INSTALLED_BACKENDS`` configuration in your
``settings.py`` file::

    INSTALLED_BACKENDS = {
        # ...
        # other backends, if any
        "twilio-backend": {
            "ENGINE": "rtwilio.outgoing.TwilioBackend",
            'config': {
                'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',  # (required)
                'auth_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',  # (required)
                'number': '(###) ###-####',  # your Twilio phone number (required)
                # 'callback': 'http://<public-django-instance>/twilio/status-callback/',  # optional callback URL
            }
        },
    }

Next, you need to add an endpoint to your ``urls.py`` for the newly created
backend.  You can do this like so::

    from django.conf.urls import patterns, include, url
    from rtwilio.views import TwilioBackendView

    urlpatterns = patterns('',
        # ...
        url(r"^backend/twilio/$",
            TwilioBackendView.as_view(backend_name="twilio-backend")),
    )

Now inbound Twilio messages can be received at ``<your-server>/backend/twilio/``
and outbound messages will be sent via the Twilio backend.
