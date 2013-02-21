# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelReference'
        db.create_table('model_databank_modelreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_type', self.gf('django.db.models.fields.IntegerField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(u'id',), max_length=50, populate_from=u'identifier')),
        ))
        db.send_create_signal('model_databank', ['ModelReference'])


    def backwards(self, orm):
        # Deleting model 'ModelReference'
        db.delete_table('model_databank_modelreference')


    models = {
        'model_databank.modelreference': {
            'Meta': {'object_name': 'ModelReference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'model_type': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "(u'id',)", 'max_length': '50', 'populate_from': "u'identifier'"})
        }
    }

    complete_apps = ['model_databank']