from django import forms

from rapidsms.backends.http.forms import BaseHttpForm


class TwilioForm(BaseHttpForm):
    From = forms.CharField()
    To = forms.CharField()
    Body = forms.CharField()
    AccountSid = forms.CharField()
    SmsSid = forms.CharField()

    def get_incoming_data(self):
        fields = self.cleaned_data.copy()
        # save SmsSid as external_id so RapidSMS will handle it properly
        fields['external_id'] = self.cleaned_data['SmsSid']
        connections = self.lookup_connections([self.cleaned_data['From']])
        return {'connection': connections[0],
                'text': self.cleaned_data['Body'],
                'fields': fields}


class StatusCallbackForm(forms.Form):
    AccountSid = forms.CharField()
    From = forms.CharField()
    SmsSid = forms.CharField()
    SmsStatus = forms.CharField()
    To = forms.CharField()
