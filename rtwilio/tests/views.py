from django.core.urlresolvers import reverse

from rapidsms.tests.harness import RapidTest


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
