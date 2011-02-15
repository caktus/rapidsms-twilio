-*- restructuredtext -*-

rtwilio
=======

Basic `Twilio <http://www.twilio.com>`_ backend for the `RapidSMS <http://www.rapidsms.org/>`_ project.

Requirements
------------

 * `python-twilio <http://pypi.python.org/pypi/twilio>`_ (pip install twilio)

Usage
-----

Add rtwilio to your Python path and setup the Twilio backend in your Django settings file. For example::

    INSTALLED_BACKENDS = {
        "twilio": {
            "ENGINE": "rtwilio.backend",
            'host': 'localhost', 'port': '8081', # used for spawned backend WSGI server
            'config': {
                'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                'auth_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
                'number': '(###) ###-####',
                'callback': 'http://<public-django-instance>/twilio/status-callback/', # optional callback URL
            }
        },
    }

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
