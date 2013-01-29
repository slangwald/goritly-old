# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ConfirmationKey'
        db.create_table('profiles_confirmationkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('unique_key', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('function', self.gf('django.db.models.fields.CharField')(default='undefined', max_length=200)),
            ('key', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=100)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_been_opened', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_been_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('failed_to_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['ConfirmationKey'])

        # Adding model 'Image'
        db.create_table('profiles_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('unique_key', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='images', null=True, blank=True, to=orm['auth.User'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rejected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('base_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='derived_images', null=True, to=orm['profiles.Image'])),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='reviewed_images', null=True, blank=True, to=orm['auth.User'])),
            ('reviewer_comment', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('profiles', ['Image'])

        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('unique_key', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('profile_image', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='profile_photos', null=True, blank=True, to=orm['profiles.Image'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('has_verified_name', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_verified_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_beta_key', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('appearance_on_platform', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('notification_policy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notification_weekday', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notification_time', self.gf('django.db.models.fields.TimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Profile'])


    def backwards(self, orm):
        
        # Deleting model 'ConfirmationKey'
        db.delete_table('profiles_confirmationkey')

        # Deleting model 'Image'
        db.delete_table('profiles_image')

        # Deleting model 'Profile'
        db.delete_table('profiles_profile')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 26, 11, 13, 9, 589668)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 26, 11, 13, 9, 589597)'}),
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
        'profiles.confirmationkey': {
            'Meta': {'object_name': 'ConfirmationKey'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'failed_to_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'function': ('django.db.models.fields.CharField', [], {'default': "'undefined'", 'max_length': '200'}),
            'has_been_opened': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_been_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'profiles.image': {
            'Meta': {'object_name': 'Image'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'base_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'derived_images'", 'null': 'True', 'to': "orm['profiles.Image']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'reviewed_images'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'reviewer_comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'images'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'appearance_on_platform': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'has_beta_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_verified_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_verified_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'notification_policy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'notification_time': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notification_weekday': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile_image': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'profile_photos'", 'null': 'True', 'blank': 'True', 'to': "orm['profiles.Image']"}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['profiles']
