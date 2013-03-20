# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GACampaign'
        db.create_table('attribution_gacampaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('attribution', ['GACampaign'])

        # Adding model 'GASource'
        db.create_table('attribution_gasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('attribution', ['GASource'])

        # Adding model 'GAMedium'
        db.create_table('attribution_gamedium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('attribution', ['GAMedium'])

        # Adding model 'GAKeyword'
        db.create_table('attribution_gakeyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('attribution', ['GAKeyword'])

        # Adding model 'GAClick'
        db.create_table('attribution_gaclick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GACampaign'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GASource'], null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GAMedium'], null=True, blank=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GAKeyword'], null=True, blank=True)),
            ('custom_var_1', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('custom_var_2', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('clicked_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('new_visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_1_completions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goal_2_completions', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('attribution', ['GAClick'])

        # Adding model 'GACustomer'
        db.create_table('attribution_gacustomer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('attribution', ['GACustomer'])

        # Adding model 'GASession'
        db.create_table('attribution_gasession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('attribution', ['GASession'])

        # Adding model 'GACustomerSession'
        db.create_table('attribution_gacustomersession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('matched_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GASession'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GACustomer'])),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('attribution', ['GACustomerSession'])

        # Adding model 'MarketingCost'
        db.create_table('attribution_marketingcost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GASource'], null=True, blank=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GACampaign'], null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GAMedium'], null=True, blank=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GAKeyword'], null=True, blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GASession'], null=True, blank=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('currency', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('attribution', ['MarketingCost'])

        # Adding model 'Order'
        db.create_table('attribution_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GACustomer'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attribution.GASession'], null=True, blank=True)),
            ('ordered_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('order_value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('promotion_code', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('promotion_value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('currency', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('attribution', ['Order'])


    def backwards(self, orm):
        
        # Deleting model 'GACampaign'
        db.delete_table('attribution_gacampaign')

        # Deleting model 'GASource'
        db.delete_table('attribution_gasource')

        # Deleting model 'GAMedium'
        db.delete_table('attribution_gamedium')

        # Deleting model 'GAKeyword'
        db.delete_table('attribution_gakeyword')

        # Deleting model 'GAClick'
        db.delete_table('attribution_gaclick')

        # Deleting model 'GACustomer'
        db.delete_table('attribution_gacustomer')

        # Deleting model 'GASession'
        db.delete_table('attribution_gasession')

        # Deleting model 'GACustomerSession'
        db.delete_table('attribution_gacustomersession')

        # Deleting model 'MarketingCost'
        db.delete_table('attribution_marketingcost')

        # Deleting model 'Order'
        db.delete_table('attribution_order')


    models = {
        'attribution.gacampaign': {
            'Meta': {'object_name': 'GACampaign'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'attribution.gaclick': {
            'Meta': {'object_name': 'GAClick'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GACampaign']", 'null': 'True', 'blank': 'True'}),
            'clicked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'custom_var_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'custom_var_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'goal_1_completions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goal_2_completions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GAKeyword']", 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GAMedium']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'new_visits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GASource']", 'null': 'True', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'attribution.gacustomer': {
            'Meta': {'object_name': 'GACustomer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        },
        'attribution.gacustomersession': {
            'Meta': {'object_name': 'GACustomerSession'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GACustomer']"}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matched_at': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GASession']"}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'attribution.gakeyword': {
            'Meta': {'object_name': 'GAKeyword'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'attribution.gamedium': {
            'Meta': {'object_name': 'GAMedium'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'attribution.gasession': {
            'Meta': {'object_name': 'GASession'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        },
        'attribution.gasource': {
            'Meta': {'object_name': 'GASource'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'attribution.marketingcost': {
            'Meta': {'object_name': 'MarketingCost'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GACampaign']", 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GAKeyword']", 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GAMedium']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GASession']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GASource']", 'null': 'True', 'blank': 'True'})
        },
        'attribution.order': {
            'Meta': {'object_name': 'Order'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GACustomer']"}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'ordered_at': ('django.db.models.fields.DateTimeField', [], {}),
            'promotion_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'promotion_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attribution.GASession']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['attribution']
