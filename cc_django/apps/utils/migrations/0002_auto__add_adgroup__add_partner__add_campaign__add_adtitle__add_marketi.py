# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdGroup'
        db.create_table('utils_adgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['AdGroup'])

        # Adding model 'Partner'
        db.create_table('utils_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Partner'])

        # Adding model 'Campaign'
        db.create_table('utils_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Campaign'])

        # Adding model 'AdTitle'
        db.create_table('utils_adtitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['AdTitle'])

        # Adding model 'MarketingCost'
        db.create_table('utils_marketingcost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Channel'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Partner'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Campaign'])),
            ('ad_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.AdGroup'])),
            ('ad_title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.AdTitle'])),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Keyword'])),
            ('match_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.MatchType'])),
            ('cost', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('utils', ['MarketingCost'])

        # Adding model 'Keyword'
        db.create_table('utils_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Keyword'])

        # Adding model 'MatchType'
        db.create_table('utils_matchtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['MatchType'])

        # Adding model 'Channel'
        db.create_table('utils_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Channel'])


    def backwards(self, orm):
        # Deleting model 'AdGroup'
        db.delete_table('utils_adgroup')

        # Deleting model 'Partner'
        db.delete_table('utils_partner')

        # Deleting model 'Campaign'
        db.delete_table('utils_campaign')

        # Deleting model 'AdTitle'
        db.delete_table('utils_adtitle')

        # Deleting model 'MarketingCost'
        db.delete_table('utils_marketingcost')

        # Deleting model 'Keyword'
        db.delete_table('utils_keyword')

        # Deleting model 'MatchType'
        db.delete_table('utils_matchtype')

        # Deleting model 'Channel'
        db.delete_table('utils_channel')


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
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviewed_images'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'}),
            'reviewer_comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        'utils.adgroup': {
            'Meta': {'object_name': 'AdGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.adtitle': {
            'Meta': {'object_name': 'AdTitle'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.channel': {
            'Meta': {'object_name': 'Channel'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.marketingcost': {
            'Meta': {'object_name': 'MarketingCost'},
            'ad_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.AdGroup']"}),
            'ad_title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.AdTitle']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']"}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Keyword']"}),
            'match_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.MatchType']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']"}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.matchtype': {
            'Meta': {'object_name': 'MatchType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'utils.partner': {
            'Meta': {'object_name': 'Partner'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
        'websites.website': {
            'Meta': {'object_name': 'Website'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'website_admins'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'website_logos'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['profiles.Image']", 'blank': 'True', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'website_owners'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['utils']