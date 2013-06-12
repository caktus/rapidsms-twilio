# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TwilioResponse.ip_address'
        db.delete_column(u'rtwilio_twilioresponse', 'ip_address')


    def backwards(self, orm):
        # Adding field 'TwilioResponse.ip_address'
        db.add_column(u'rtwilio_twilioresponse', 'ip_address',
                      self.gf('django.db.models.fields.IPAddressField')(default='', max_length=15),
                      keep_default=False)


    models = {
        u'rtwilio.twilioresponse': {
            'Meta': {'object_name': 'TwilioResponse'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['rtwilio']