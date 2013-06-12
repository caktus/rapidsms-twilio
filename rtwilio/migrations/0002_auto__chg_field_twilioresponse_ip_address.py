# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TwilioResponse.ip_address'
        db.alter_column(u'rtwilio_twilioresponse', 'ip_address', self.gf('django.db.models.fields.CharField')(max_length=64))

    def backwards(self, orm):

        # Changing field 'TwilioResponse.ip_address'
        db.alter_column(u'rtwilio_twilioresponse', 'ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15))

    models = {
        u'rtwilio.twilioresponse': {
            'Meta': {'object_name': 'TwilioResponse'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['rtwilio']