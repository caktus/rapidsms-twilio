Release History
===============

Release and change history for rapidsms-twilio


v1.0.0 (Released TBD)
----------------------------

This is a clean up and stablizing release for rapidsms-twilio. This removes support for old
versions of Django and RapidSMS. The setup has been streamlined by changing some of the defaults.


Backwards Incompatible Changes
______________________________

* Support for Django < 1.7 has been dropped.
* Support for RapidSMS < 0.18 has been dropped.
* The default url patterns have been renamed. ``status-callback`` is now ``twilio-status-callback`` to be consistent internally
and with the package naming.
* The default backend name is now ``twilio-backend`` if using the default views and url patterns.
* The url setup in the quick start now uses an include and defaults to using ``/backend/twilio/`` and
``/backend/twilio/status-callback/`` for the urls. If you were including the urls manually you are
not affected by this change. Otherwise you need to ensure the setup is changed in the Twilio configuration
as well.


v0.3.0 (Released 2015-03-27)
----------------------------

This is a minor release following up on the previous security release to turn the
request validation on by default.


Backwards Incompatible Changes
______________________________

* Twilio validation is now enforced by default. To turn this off you can set ``validate`` to ``False`` in your backend configuration. This is not recommended.


v0.2.1 (Released 2015-03-27)
----------------------------

Security release to add support for validating incoming requests from Twilio. For
backwards compatibility this is not enabled by default. You should update your backend
configuration to include the new ``validate`` configuration. See the quick-start for
an example configuration.

* Improved ``tox`` testing support for RapidSMS and Django version combinations.
* Relaxed ``twilio`` requirement.
* Added Twilio request signature validation.


v0.2.0 (Released 2013-06-21)
----------------------------

Improved callback functionality and added needed tests:

* Remove callback URL field. It's not needed.
* Require POST on callback view.
* Add tests to callback view.


Bug Fixes
_________

- Fixed issue where using a port with the callback URL caused an error.


v0.1.0 (Released 2013-06-10)
----------------------------

Update for RapidSMS 0.13+.


v0.0.1 (Released 2010-07-26)
----------------------------

- Initial public release.
