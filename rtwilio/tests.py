import unittest
import urllib
import logging

from rapidsms.tests.harness import MockRouter
from rtwilio.backend import TwilioBackend, TwilioHandler

from rapidsms.tests.scripted import TestScript
from django.test.client import Client

router = MockRouter()
backend = TwilioBackend(name="twilio", router=router)
logging.basicConfig(level=logging.DEBUG)


class TestBackendTwilio(unittest.TestCase):

    def test_Router(self):
        data = {'Body': 'now', 'From': '9191111111', 'blah': 'foo'}
        message = backend.message(data)
        backend.route(message)
        
