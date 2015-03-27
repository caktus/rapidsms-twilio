from mock import Mock, patch

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from rapidsms.tests.harness import RapidTest, CreateDataMixin

from ..views import validate_twilio_signature


EXAMPLE_CONFIG = {
    'ENGINE': 'rtwilio.outgoing.TwilioBackend',
    'config': {
        'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'auth_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYY',
        'number': '(###) ###-####',
        'validate': False,
    }
}


class TwilioViewTest(RapidTest):

    urls = 'rtwilio.tests.urls'
    disable_phases = True
    backends = {
        'twilio-backend': EXAMPLE_CONFIG,
    }

    def test_invalid_response(self):
        """HTTP 400 should return if data is invalid."""
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self.client.post(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 400)

    def test_get_disabled(self):
        """HTTP 405 should return if GET is used."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        response = self.client.get(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 405)

    def test_valid_post_message(self):
        """Valid POSTs should pass message object to router."""
        data = {"From": "transport",
                "To": "+14155554345",
                "Body": "foo",
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        response = self.client.post(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 200)
        message = self.inbound[0]
        self.assertEqual(data['Body'], message.text)
        self.assertEqual(message.fields['external_id'], data['SmsSid'])
        self.assertEqual('rtwilio-backend', message.connection.backend.name)


@override_settings(INSTALLED_BACKENDS={'twilio-backend': EXAMPLE_CONFIG})
class CallbackTest(CreateDataMixin, TestCase):

    urls = 'rtwilio.tests.urls'

    def setUp(self):
        self.valid_data = {
            'To': '+1112223333',
            'AccountSid': self.random_string(34),
            'SmsSid': self.random_string(34),
            'From': '+9998887777',
            'SmsStatus': 'sent',
        }

    def test_get_forbidden(self):
        """GET is not allowed."""
        url = reverse("twilio-status-callback")
        response = self.client.get(url)
        self.assertEqual(405, response.status_code)

    def test_valid_data_callback(self):
        """Valid POSTs should return 200."""
        url = reverse("twilio-status-callback")
        response = self.client.post(url, self.valid_data)
        self.assertEqual(200, response.status_code)

    def test_invalid_callback(self):
        """Invalid POSTs should return a 400."""
        url = reverse("twilio-status-callback")
        del self.valid_data['To']
        response = self.client.post(url, self.valid_data)
        self.assertEqual(400, response.status_code)


class SignatureValidationTestCase(TestCase):
    """Validate request signature from Twilio."""

    def setUp(self):
        self.factory = RequestFactory()
        # From http://www.twilio.com/docs/security example
        self.request = self.factory.post(
            '/myapp.php?foo=1&bar=2',
            {
                'CallSid': 'CA1234567890ABCDE',
                'Caller': '+14158675309',
                'Digits': '1234',
                'From': '+14158675309',
                'To': '+18005551212'
            },
            HTTP_X_TWILIO_SIGNATURE='RSOYDt4T1cUTdK1PDd93/VVr8B8=',
            SERVER_NAME='mycompany.com',
            SERVER_PORT='443',
            **{'wsgi.url_scheme': 'https'}
        )
        self.config = {
            'ENGINE': 'rtwilio.outgoing.TwilioBackend',
            'config': {
                'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                'auth_token': '12345',
                'number': '(###) ###-####',
                'validate': True,
            }
        }
        self.view = Mock()
        self.view.return_value = HttpResponse('OK')

    def test_valid_signature(self):
        """Valid signature should pass request onto the view."""
        wrapped = validate_twilio_signature(self.view)
        with self.settings(INSTALLED_BACKENDS={'twilio-backend': self.config}):
            result = wrapped(self.request)
            self.assertEqual(result.status_code, 200)
            self.view.assert_called_with(self.request)

    def test_invalid_signature(self):
        """Invalid signatures will return a 400 reponse."""
        wrapped = validate_twilio_signature(self.view)
        self.config['config']['auth_token'] = 'XXXX'
        with self.settings(INSTALLED_BACKENDS={'twilio-backend': self.config}):
            result = wrapped(self.request)
            self.assertEqual(result.status_code, 400)
            self.assertFalse(self.view.called)

    def test_missing_signature(self):
        """Signature will be validated (and fail) if missing."""
        wrapped = validate_twilio_signature(self.view)
        self.config['config']['auth_token'] = 'XXXX'
        del self.request.META['HTTP_X_TWILIO_SIGNATURE']
        with self.settings(INSTALLED_BACKENDS={'twilio-backend': self.config}):
            result = wrapped(self.request)
            self.assertEqual(result.status_code, 400)
            self.assertFalse(self.view.called)

    def test_non_default_backend(self):
        """Allow using a non-default backend name with the decorator."""
        wrapped = validate_twilio_signature(self.view, backend_name='other')
        with self.settings(INSTALLED_BACKENDS={'other': self.config}):
            result = wrapped(self.request)
            self.assertEqual(result.status_code, 200)
            self.view.assert_called_with(self.request)
