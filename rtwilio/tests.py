import random

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from rapidsms.router.test import TestRouter
from rapidsms.tests.harness.base import CreateDataTest
from rapidsms.messages.outgoing import OutgoingMessage

from rtwilio import views
from rtwilio.outgoing import TwilioBackend


### this should live in rapidsms.tests.harness ###
UNICODE_CHARS = [unichr(x) for x in xrange(1, 0xD7FF)]

def random_unicode_string(max_length=255):
    output = u''
    for x in xrange(random.randint(1, max_length/2)):
        c = UNICODE_CHARS[random.randint(0, len(UNICODE_CHARS)-1)]
        output += c + u' '
    return output


class ReceiveTest(CreateDataTest, TestCase):

    urls = 'rtwilio.urls'

    def setUp(self):
        self.rf = RequestFactory()
        name = 'twilio-backend'
        self.url = reverse('twilio-backend', args=[name])
        self.view = views.TwilioBackendView.as_view(backend_name=name)

    def _post(self, data={}):
        request = self.rf.post(self.url, data)
        return self.view(request)

    def test_valid_form(self):
        """Form should be valid if GET keys match configuration."""
        data = {"From": "transport",
                "To": "+14155554345",
                "Body": "+14155554345",
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        view = views.TwilioBackendView()
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Form is invalid if POST keys don't match configuration."""
        view = views.TwilioBackendView()
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertFalse(form.is_valid())

    def test_invalid_response(self):
        """HTTP 400 should return if form is invalid."""
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self._post(data)
        self.assertEqual(response.status_code, 400)

    # TODO: test for incoming message encoding
    # def test_incoming_unicode_characters():
    #     basic_conf['config']['encoding'] = 'UTF-8'
    #     backend = TwilioBackend(name="twilio", router=None, **basic_conf)
    #     text = random_unicode_string(20).encode(basic_conf['config']['encoding'])
    #     data = {'From': '1112229999', 'Body': text}
    #     message = backend.message(data)
    #     assert_equals(text.decode(basic_conf['config']['encoding']), message.text)


class SendTest(CreateDataTest, TestCase):

    def test_required_fields(self):
        """Twilio backend requires Gateway URL and credentials."""
        router = TestRouter()
        self.assertRaises(TypeError, TwilioBackend, router, "twilio")

    def test_outgoing_keys(self):
        """Outgoing POST data should contain the proper keys."""
        connection = self.create_connection()
        message = OutgoingMessage(connection, 'hello!')
        router = TestRouter()
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34)}
        backend = TwilioBackend(router, "twilio", config=config)
        data = backend.prepare_message(message)
        self.assertTrue('from_' in data)
        self.assertTrue('to' in data)
        self.assertTrue('body' in data)

    def test_outgoing_unicode_characters(self):
        """Ensure outgoing messages are encoded properly."""
        connection = self.create_connection()
        message = OutgoingMessage(connection, random_unicode_string(20))
        router = TestRouter()
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34),
                  'encoding': 'UTF-8'}
        backend = TwilioBackend(router, "twilio", config=config)
        data = backend.prepare_message(message)
        self.assertEqual(data['body'].decode('UTF-8'), message.text)
