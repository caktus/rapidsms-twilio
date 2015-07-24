from django.test import TestCase

from rapidsms.tests.harness import CreateDataMixin

from rtwilio.forms import TwilioForm


class TwilioFormTest(CreateDataMixin, TestCase):

    def test_valid_form(self):
        """Form should be valid if GET keys match configuration."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Form is invalid if POST keys don't match configuration."""
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        self.assertFalse(form.is_valid())

    def test_get_incoming_data(self):
        """get_incoming_data should return matching text and connection."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(data['Body'], incoming_data['text'])
        self.assertEqual(data['From'],
                         incoming_data['connection'].identity)
        self.assertEqual(data['SmsSid'],
                         incoming_data['fields']['external_id'])
        self.assertEqual('rtwilio-backend',
                         incoming_data['connection'].backend.name)
