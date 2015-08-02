rapidsms-twilio
===============

`Twilio`_ backend for the `RapidSMS`_ project. Uses `python-twilio`_ to communicate with Twilio.

.. image::
    https://api.travis-ci.org/caktus/rapidsms-twilio.png?branch=develop
    :alt: Build Status
    :target: http://travis-ci.org/caktus/rapidsms-twilio

Features
--------

* Incoming (MO) and Outgoing (MT) SMS support.
* Support for Twilio's `status callback <http://www.twilio.com/docs/api/rest/sending-sms#post-parameters-optional>`_


Requirements
------------

* Python 2.7 or Python 3.3+
* Django 1.7+
* RapidSMS v0.18.0+

Future versions: We currently support Django 1.8 with no pending deprecation warnings in our 1.0
release. We expect each future point release to similarly support the next version of Django, so our
1.1 release would support Django 1.9 with no pending deprecation warnings. Support for older Django
versions may be dropped when the period of 'mainstream support' expires. See Django's `supported
versions <https://www.djangoproject.com/download/>`_ documentation for those timelines.

Installation
-------------

rapidsms-twilio requires Django >= 1.7 and Python >= 2.7.

To install from PyPi::

    pip install rapidsms-twilio

Documentation
-------------

Documentation on using rapidsms-twilio is available on
`Read The Docs <http://readthedocs.org/docs/rapidsms-twilio/>`_.


License
-------

rapidsms-twilio is released under the BSD License. See the  `LICENSE
<https://github.com/caktus/rapidsms-twilio/blob/master/LICENSE.txt>`_ file for
more details.

Contributing
------------

If you think you've found a bug or are interested in contributing to this
project check out `rapidsms-twilio on Github <https://github.com/caktus
/rapidsms-twilio>`_.

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.

.. _RapidSMS: http://www.rapidsms.org/
.. _Twilio: http://www.twilio.com
.. _python-twilio: http://pypi.python.org/pypi/twilio
