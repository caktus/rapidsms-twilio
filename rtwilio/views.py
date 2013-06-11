from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rapidsms.backends.http.views import GenericHttpBackendView

from rtwilio.models import TwilioResponse
from rtwilio.forms import StatusCallbackForm, TwilioForm


class TwilioBackendView(GenericHttpBackendView):
    """
    Backend view for processing incoming messages from Twilio.
    https://www.twilio.com/docs/api/twiml/sms/twilio_request
    """

    http_method_names = ['post']
    form_class = TwilioForm


@csrf_exempt
def status_callback(request):
    form = StatusCallbackForm(request.POST or None)
    if form.is_valid():
        TwilioResponse.objects.create(
            pk=form.cleaned_data['SmsSid'],
            ip_address=request.get_host(),
            account=form.cleaned_data['AccountSid'],
            sender=form.cleaned_data['From'],
            recipient=form.cleaned_data['To'],
            status=form.cleaned_data['SmsStatus'],
        )
    return HttpResponse('OK')
