import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rapidsms.backends.http.views import GenericHttpBackendView

from rtwilio.models import TwilioResponse
from rtwilio.forms import StatusCallbackForm, TwilioForm


logger = logging.getLogger(__name__)


class TwilioBackendView(GenericHttpBackendView):
    """
    Backend view for processing incoming messages from Twilio.
    https://www.twilio.com/docs/api/twiml/sms/twilio_request
    """

    http_method_names = ['post']
    form_class = TwilioForm


@require_POST
@csrf_exempt
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
