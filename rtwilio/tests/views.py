from django.test import TestCase

from django.core.urlresolvers import reverse

from rapidsms.tests.harness import RapidTest, CreateDataMixin


class TwilioViewTest(RapidTest):

    urls = 'rtwilio.tests.urls'
    disable_phases = True

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
