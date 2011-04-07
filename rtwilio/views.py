from django.http import HttpResponse

from rtwilio.models import TwilioResponse
from rtwilio.forms import StatusCallbackForm

from threadless_router.backends.http.froms import HttpForm
from threadless_router.backends.http.views import BaseHttpBackendView


class TwilioBackendView(BaseHttpBackendView):

    form_class = HttpForm

    def get_form_kwargs(self):
        kwargs = super(SimpleHttpBackendView, self).get_form_kwargs()
        kwargs.update({'identity': 'From', 'text': 'Body'})
        return kwargs


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
