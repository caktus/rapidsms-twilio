import functools
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import available_attrs, method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rapidsms.backends.http.views import GenericHttpBackendView
from twilio.util import RequestValidator

from rtwilio.models import TwilioResponse
from rtwilio.forms import StatusCallbackForm, TwilioForm


logger = logging.getLogger(__name__)


def validate_twilio_signature(func=None, backend_name='twilio-backend'):
    """View decorator to validate requests from Twilio per http://www.twilio.com/docs/security."""

    def _dec(view_func):
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            backend = kwargs.get('backend_name', backend_name)
            config = settings.INSTALLED_BACKENDS[backend]['config']
            validator = RequestValidator(config['auth_token'])
            signature = request.META.get('HTTP_X_TWILIO_SIGNATURE', '')
            url = request.build_absolute_uri()
            body = {}
            if request.method == 'POST':
                body = request.POST
            require_validation = config.get('validate', True)
            if validator.validate(url, body, signature) or not require_validation:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseBadRequest()
        return _wrapped_view

    if func is None:
        return _dec
    else:
        return _dec(func)


class TwilioBackendView(GenericHttpBackendView):
    """
    Backend view for processing incoming messages from Twilio.
    https://www.twilio.com/docs/api/twiml/sms/twilio_request
    """

    http_method_names = ['post']
    form_class = TwilioForm

    @method_decorator(validate_twilio_signature)
    def dispatch(self, *args, **kwargs):
        return super(TwilioBackendView, self).dispatch(*args, **kwargs)


@require_POST
@csrf_exempt
@validate_twilio_signature
def status_callback(request):
    form = StatusCallbackForm(request.POST or None)
    if form.is_valid():
        try:
            TwilioResponse.objects.create(
                pk=form.cleaned_data['SmsSid'],
                account=form.cleaned_data['AccountSid'],
                sender=form.cleaned_data['From'],
                recipient=form.cleaned_data['To'],
                status=form.cleaned_data['SmsStatus'],
            )
        except:
            logger.debug("callback data")
            logger.debug(form.cleaned_data)
            raise
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest()
