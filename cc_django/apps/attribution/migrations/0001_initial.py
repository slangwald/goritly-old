# -*- coding: utf-8 -*-
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

        # Adding model 'SummaryCLV'
        db.create_table('attribution_summaryclv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['websites.Website'])),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_click', self.gf('django.db.models.fields.DateTimeField')()),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('partner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('campaign', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('adgroup', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('adtitle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('match_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('date_order', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_customer', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_clv', self.gf('django.db.models.fields.DateTimeField')()),
            ('counter', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('customer_age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('contribution_to_clv', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('marketing_cost', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('revenue_order', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('profit_order', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('profit_order_after_returns', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('revenue', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('revenue_click', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('profit', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('profit_click', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('clv', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('clv_click', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('marketing_cost_click', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('roi', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('attribution', ['SummaryCLV'])


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

        # Deleting model 'SummaryCLV'
        db.delete_table('attribution_summaryclv')


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
        },
        'attribution.summaryclv': {
            'Meta': {'object_name': 'SummaryCLV'},
            'adgroup': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'adtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'clv': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'contribution_to_clv': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer_age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_click': ('django.db.models.fields.DateTimeField', [], {}),
            'date_clv': ('django.db.models.fields.DateTimeField', [], {}),
            'date_customer': ('django.db.models.fields.DateTimeField', [], {}),
            'date_order': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'marketing_cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'marketing_cost_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'match_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'partner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'profit': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'profit_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'profit_order': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'profit_order_after_returns': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'revenue': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'revenue_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'revenue_order': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'roi': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['websites.Website']"})
        },
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

    complete_apps = ['attribution']