rapidsms-twilio
===============

.. image::
    https://api.travis-ci.org/caktus/rapidsms-twilio.png?branch=develop
    :alt: Build Status
    :target: http://travis-ci.org/caktus/rapidsms-twilio

`Twilio <http://www.twilio.com>`_ backend for the `RapidSMS
<http://www.rapidsms.org/>`_ project.


Requirements
------------

 * `python-twilio <http://pypi.python.org/pypi/twilio>`_

Usage
-----

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

2. Add the callback view to your urlconf::

    urlpatterns = patterns('',
        # ...
        url(r'^backend/twilio/status-callback/$', status_callback,
            name='twilio-status-callback'),
    )

3. Add the necessary database tables (omit ``--migrate`` if you're not using South)::

    python manage.py syncdb --migrate

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

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
