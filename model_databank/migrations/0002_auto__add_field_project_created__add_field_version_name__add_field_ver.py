# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.created'
        db.add_column('model_databank_project', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Version.name'
        db.add_column('model_databank_version', 'name',
                      self.gf('django.db.models.fields.CharField')(default='TODO_change', max_length=100),
                      keep_default=False)

        # Adding field 'Version.comment'
        db.add_column('model_databank_version', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Version.created'
        db.add_column('model_databank_version', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Version.model'
        db.alter_column('model_databank_version', 'model_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['model_databank.ModelReference']))
        # Deleting field 'Variant.model'
        db.delete_column('model_databank_variant', 'model_id')

        # Adding field 'Variant.name'
        db.add_column('model_databank_variant', 'name',
                      self.gf('django.db.models.fields.CharField')(default='TODO_change', max_length=100),
                      keep_default=False)

        # Adding field 'Variant.comment'
        db.add_column('model_databank_variant', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Variant.created'
        db.add_column('model_databank_variant', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 27, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.created'
        db.delete_column('model_databank_project', 'created')

        # Deleting field 'Version.name'
        db.delete_column('model_databank_version', 'name')

        # Deleting field 'Version.comment'
        db.delete_column('model_databank_version', 'comment')

        # Deleting field 'Version.created'
        db.delete_column('model_databank_version', 'created')


        # User chose to not deal with backwards NULL issues for 'Version.model'
        raise RuntimeError("Cannot reverse this migration. 'Version.model' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Variant.model'
        raise RuntimeError("Cannot reverse this migration. 'Variant.model' and its values cannot be restored.")
        # Deleting field 'Variant.name'
        db.delete_column('model_databank_variant', 'name')

        # Deleting field 'Variant.comment'
        db.delete_column('model_databank_variant', 'comment')

        # Deleting field 'Variant.created'
        db.delete_column('model_databank_variant', 'created')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'model_databank.modelreference': {
            'Meta': {'object_name': 'ModelReference'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'model_type': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'identifier'"})
        },
        'model_databank.project': {
            'Meta': {'object_name': 'Project'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_references': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'provider'", 'symmetrical': 'False', 'to': "orm['model_databank.ModelReference']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'name'"})
        },
        'model_databank.variant': {
            'Meta': {'object_name': 'Variant'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'variants'", 'to': "orm['model_databank.Version']"})
        },
        'model_databank.version': {
            'Meta': {'object_name': 'Version'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'versions'", 'null': 'True', 'to': "orm['model_databank.ModelReference']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['model_databank.Version']", 'null': 'True'})
        }
    }

    complete_apps = ['model_databank']