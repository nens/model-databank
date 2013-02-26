# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelVersion'
        db.create_table('model_databank_modelversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'original', to=orm['model_databank.ModelReference'])),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'version', to=orm['model_databank.ModelReference'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=u'name')),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('model_databank', ['ModelVersion'])

        # Adding model 'Project'
        db.create_table('model_databank_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=u'name')),
        ))
        db.send_create_signal('model_databank', ['Project'])

        # Adding M2M table for field model_references on 'Project'
        db.create_table('model_databank_project_model_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['model_databank.project'], null=False)),
            ('modelreference', models.ForeignKey(orm['model_databank.modelreference'], null=False))
        ))
        db.create_unique('model_databank_project_model_references', ['project_id', 'modelreference_id'])

        # Adding field 'ModelReference.comment'
        db.add_column('model_databank_modelreference', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'ModelReference.created'
        db.add_column('model_databank_modelreference', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 2, 26, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'ModelReference.slug'
        db.alter_column('model_databank_modelreference', 'slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=u'identifier'))

    def backwards(self, orm):
        # Deleting model 'ModelVersion'
        db.delete_table('model_databank_modelversion')

        # Deleting model 'Project'
        db.delete_table('model_databank_project')

        # Removing M2M table for field model_references on 'Project'
        db.delete_table('model_databank_project_model_references')

        # Deleting field 'ModelReference.comment'
        db.delete_column('model_databank_modelreference', 'comment')

        # Deleting field 'ModelReference.created'
        db.delete_column('model_databank_modelreference', 'created')


        # Changing field 'ModelReference.slug'
        db.alter_column('model_databank_modelreference', 'slug', self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique_with=(u'id',), populate_from=u'identifier'))

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
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'identifier'"}),
            'versions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['model_databank.ModelReference']", 'through': "orm['model_databank.ModelVersion']", 'symmetrical': 'False'})
        },
        'model_databank.modelversion': {
            'Meta': {'object_name': 'ModelVersion'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'original'", 'to': "orm['model_databank.ModelReference']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'name'"}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'version'", 'to': "orm['model_databank.ModelReference']"})
        },
        'model_databank.project': {
            'Meta': {'object_name': 'Project'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_references': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'provider'", 'symmetrical': 'False', 'to': "orm['model_databank.ModelReference']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'name'"})
        }
    }

    complete_apps = ['model_databank']