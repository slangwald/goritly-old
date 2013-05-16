# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CustomerCLV.linear'
        db.delete_column('utils_customerclv', 'linear')

        # Deleting field 'CustomerCLV.decay'
        db.delete_column('utils_customerclv', 'decay')

        # Deleting field 'CustomerCLV.last_click'
        db.delete_column('utils_customerclv', 'last_click')

        # Deleting field 'CustomerCLV.u_shape'
        db.delete_column('utils_customerclv', 'u_shape')

        # Deleting field 'CustomerCLV.clv'
        db.delete_column('utils_customerclv', 'clv')

        # Deleting field 'CustomerCLV.first_click'
        db.delete_column('utils_customerclv', 'first_click')

        # Adding field 'CustomerCLV.clv_total'
        db.add_column('utils_customerclv', 'clv_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_added'
        db.add_column('utils_customerclv', 'clv_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.partner'
        db.add_column('utils_customerclv', 'partner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['utils.Partner']),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_u_shape_total'
        db.add_column('utils_customerclv', 'clv_u_shape_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_linear_total'
        db.add_column('utils_customerclv', 'clv_linear_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_first_click_total'
        db.add_column('utils_customerclv', 'clv_first_click_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_last_click_total'
        db.add_column('utils_customerclv', 'clv_last_click_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_decay_total'
        db.add_column('utils_customerclv', 'clv_decay_total',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_u_shape_added'
        db.add_column('utils_customerclv', 'clv_u_shape_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_linear_added'
        db.add_column('utils_customerclv', 'clv_linear_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_first_click_added'
        db.add_column('utils_customerclv', 'clv_first_click_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_last_click_added'
        db.add_column('utils_customerclv', 'clv_last_click_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv_decay_added'
        db.add_column('utils_customerclv', 'clv_decay_added',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'CustomerCLV.linear'
        db.add_column('utils_customerclv', 'linear',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.decay'
        db.add_column('utils_customerclv', 'decay',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.last_click'
        db.add_column('utils_customerclv', 'last_click',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.u_shape'
        db.add_column('utils_customerclv', 'u_shape',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.clv'
        db.add_column('utils_customerclv', 'clv',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'CustomerCLV.first_click'
        db.add_column('utils_customerclv', 'first_click',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Deleting field 'CustomerCLV.clv_total'
        db.delete_column('utils_customerclv', 'clv_total')

        # Deleting field 'CustomerCLV.clv_added'
        db.delete_column('utils_customerclv', 'clv_added')

        # Deleting field 'CustomerCLV.partner'
        db.delete_column('utils_customerclv', 'partner_id')

        # Deleting field 'CustomerCLV.clv_u_shape_total'
        db.delete_column('utils_customerclv', 'clv_u_shape_total')

        # Deleting field 'CustomerCLV.clv_linear_total'
        db.delete_column('utils_customerclv', 'clv_linear_total')

        # Deleting field 'CustomerCLV.clv_first_click_total'
        db.delete_column('utils_customerclv', 'clv_first_click_total')

        # Deleting field 'CustomerCLV.clv_last_click_total'
        db.delete_column('utils_customerclv', 'clv_last_click_total')

        # Deleting field 'CustomerCLV.clv_decay_total'
        db.delete_column('utils_customerclv', 'clv_decay_total')

        # Deleting field 'CustomerCLV.clv_u_shape_added'
        db.delete_column('utils_customerclv', 'clv_u_shape_added')

        # Deleting field 'CustomerCLV.clv_linear_added'
        db.delete_column('utils_customerclv', 'clv_linear_added')

        # Deleting field 'CustomerCLV.clv_first_click_added'
        db.delete_column('utils_customerclv', 'clv_first_click_added')

        # Deleting field 'CustomerCLV.clv_last_click_added'
        db.delete_column('utils_customerclv', 'clv_last_click_added')

        # Deleting field 'CustomerCLV.clv_decay_added'
        db.delete_column('utils_customerclv', 'clv_decay_added')


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
        'utils.attributions': {
            'Meta': {'object_name': 'Attributions'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']"}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'decay': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'first_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_click': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'linear': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'orders': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'u_shape': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
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
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Order']", 'null': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']", 'null': 'True', 'blank': 'True'}),
            'position_in_chain': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
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
        'utils.customerclv': {
            'Meta': {'object_name': 'CustomerCLV'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']"}),
            'clv_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_decay_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_decay_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_first_click_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_first_click_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_last_click_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_last_click_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_linear_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_linear_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_u_shape_added': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'clv_u_shape_total': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'first_ordered_at': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'orders': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']"})
        },
        'utils.customeridmap': {
            'Meta': {'object_name': 'CustomerIdMap'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Visitor']"})
        },
        'utils.customerroimarks': {
            'Meta': {'object_name': 'CustomerRoiMarks'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Partner']"}),
            'roi_decay_100': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_125': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_150': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_175': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_200': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_25': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_300': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_400': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_50': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_500': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_decay_75': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_100': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_125': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_150': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_175': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_200': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_25': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_300': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_400': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_50': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_500': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_first_click_75': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_100': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_125': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_150': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_175': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_200': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_25': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_300': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_400': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_50': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_500': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_last_click_75': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_100': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_125': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_150': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_175': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_200': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_25': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_300': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_400': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_50': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_500': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_linear_75': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_100': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_125': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_150': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_175': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_200': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_25': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_300': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_400': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_50': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_500': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'roi_u_shape_75': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
            'ad_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.AdGroup']", 'null': 'True'}),
            'ad_title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.AdTitle']", 'null': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Campaign']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Channel']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
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
        'utils.order': {
            'Meta': {'object_name': 'Order'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordered_at': ('django.db.models.fields.DateTimeField', [], {}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'revenue': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'shipping': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'tax': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Visitor']", 'null': 'True'})
        },
        'utils.orderproducts': {
            'Meta': {'object_name': 'OrderProducts'},
            'cost_per_unit': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Order']"}),
            'price_per_unit': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Product']"}),
            'qty': ('django.db.models.fields.FloatField', [], {'default': '1'})
        },
        'utils.orderproductsreturns': {
            'Meta': {'object_name': 'OrderProductsReturns'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Product']"}),
            'qty': ('django.db.models.fields.FloatField', [], {'default': '1'})
        },
        'utils.partner': {
            'Meta': {'object_name': 'Partner'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.ProductCategory']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'utils.productcategory': {
            'Meta': {'object_name': 'ProductCategory'},
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