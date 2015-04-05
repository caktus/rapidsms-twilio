Release History
===============

Release and change history for rapidsms-twilio


v0.3.1 (Released 2015-04-05)
----------------------------

Fixes a regression from the v0.3 release where the view was not marked as CSRF
except.


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
