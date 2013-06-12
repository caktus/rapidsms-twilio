from django.contrib import admin

from rtwilio.models import TwilioResponse


class TwilioResponseAdmin(admin.ModelAdmin):
    list_display = ('message', 'date', 'sender', 'recipient',
                    'sent')
    ordering = ('-date',)
    list_filter = ('date',)

    def sent(self, response):
        return response.status == 'sent'
    sent.boolean = True

admin.site.register(TwilioResponse, TwilioResponseAdmin)
