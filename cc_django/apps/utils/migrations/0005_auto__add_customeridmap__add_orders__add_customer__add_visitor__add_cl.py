# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomerIdMap'
        db.create_table('utils_customeridmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Visitor'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Customer'])),
        ))
        db.send_create_signal('utils', ['CustomerIdMap'])

        # Adding model 'Orders'
        db.create_table('utils_orders', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Orders'])

        # Adding model 'Customer'
        db.create_table('utils_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Customer'])

        # Adding model 'Visitor'
        db.create_table('utils_visitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('utils', ['Visitor'])

        # Adding model 'Click'
        db.create_table('utils_click', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Campaign'], null=True, blank=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Partner'], null=True, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Channel'], null=True, blank=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Keyword'], null=True, blank=True)),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Visitor'], null=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Customer'], null=True)),
            ('clicked_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('new_visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_1_completions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_2_completions', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('utils', ['Click'])


    def backwards(self, orm):
        # Deleting model 'CustomerIdMap'
        db.delete_table('utils_customeridmap')

        # Deleting model 'Orders'
        db.delete_table('utils_orders')

        # Deleting model 'Customer'
        db.delete_table('utils_customer')

        # Deleting model 'Visitor'
        db.delete_table('utils_visitor')

        # Deleting model 'Click'
        db.delete_table('utils_click')


    models = {
        'utils.adgroup': {
            'Meta': {'object_name': 'AdGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.adtitle': {
            'Meta': {'object_name': 'AdTitle'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.brandkeywords': {
            'Meta': {'object_name': 'BrandKeywords'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.channel': {
            'Meta': {'object_name': 'Channel'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.click': {
            'Meta': {'object_name': 'Click'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']", 'null': 'True', 'blank': 'True'}),
            'clicked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']", 'null': 'True'}),
            'goal_1_completions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goal_2_completions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Keyword']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'new_visits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']", 'null': 'True', 'blank': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Visitor']", 'null': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'utils.customer': {
            'Meta': {'object_name': 'Customer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        },
        'utils.customeridmap': {
            'Meta': {'object_name': 'CustomerIdMap'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Visitor']"})
        },
        'utils.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']"})
        },
        'utils.matchtype': {
            'Meta': {'object_name': 'MatchType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.orders': {
            'Meta': {'object_name': 'Orders'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.partner': {
            'Meta': {'object_name': 'Partner'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['utils']