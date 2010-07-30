from django import forms


class StatusCallbackForm(forms.Form):
    AccountSid = forms.CharField()
    From = forms.CharField()
    SmsSid = forms.CharField()
    SmsStatus = forms.CharField()
    To = forms.CharField()
