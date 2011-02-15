import unittest
import urllib
import logging
import datetime

from nose.tools import assert_equals, assert_raises, assert_true, assert_false

from rapidsms.router import Router
from rapidsms.messages.incoming import IncomingMessage
from rapidsms.models import Connection, Contact, Backend
from rapidsms.messages.outgoing import OutgoingMessage

from rtwilio.backend import TwilioBackend


logging.basicConfig(level=logging.DEBUG)

basic_conf = {
    'config': {
        'account_sid': 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'auth_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
        'number': '(###) ###-####',
    }
}


class MockRouter(Router):
    def start(self):
        self.running = True
        self.accepting = True
        self._start_all_backends()
        self._start_all_apps()

    def stop(self):
        self.running = False
        self.accepting = False
        self._stop_all_backends()


def test_good_message():
    """ Make sure backend creates IncomingMessage properly """
    backend = TwilioBackend(name="twilio", router=None, **basic_conf)
    data = {'From': '1112229999', 'Body': 'Hi'}
    message = backend.message(data)
    assert_true(isinstance(message, IncomingMessage))
    assert_true(isinstance(message.connection, Connection))
    assert_equals(message.connection.identity, data['From'])
    assert_equals(message.text, data['Body'])
    

def test_bad_message():
    """ Don't die if POSTed data doesn't contain the necessary items """
    backend = TwilioBackend(name="twilio", router=None, **basic_conf)
    data = {'foo': 'moo'}
    message = backend.message(data)
    assert_equals(message, None)


def test_backend_route():
    router = MockRouter()
    backend = TwilioBackend(name="twilio", router=router, **basic_conf)
    router.start()
    Connection.objects.all().delete()
    conn = Connection.objects.create(backend=backend.model,
                                     identity='1112229999')
    message = IncomingMessage(conn, 'Hi', datetime.datetime.now())
    assert_true(backend.route(message), True)

