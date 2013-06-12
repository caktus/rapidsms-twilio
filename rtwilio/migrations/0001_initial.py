# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwilioResponse'
        db.create_table(u'rtwilio_twilioresponse', (
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'rtwilio', ['TwilioResponse'])


    def backwards(self, orm):
        # Deleting model 'TwilioResponse'
        db.delete_table(u'rtwilio_twilioresponse')


    models = {
        u'rtwilio.twilioresponse': {
            'Meta': {'object_name': 'TwilioResponse'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['rtwilio']