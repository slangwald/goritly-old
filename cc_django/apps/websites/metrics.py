from utils.models import *
from dateutil import rrule
from datetime import datetime

from django.core import serializers


"""
------------------------
METRICS
------------------------
"""

class BasicMetric():

    table = None

    dimensions = ['channel', 'partner', 'campaign']

    seperation_field = {
        'channel' : 'channel_id', 
        'partner' : 'partner_id', 
        'campaign': 'campaign_id'
    }
    
    seperation_objects = {
        'channel' : Channel ,
        'partner' : Partner ,
        'campaign': Campaign, 
    }
    
    seperation_aggregated = 'aggregated'

    def __init__(self, model, filter, seperation, options = {}):
        self.filter     = filter
        print filter
        self.options    = options
        self.model      = model
        
        if 'timerange' in self.options and not 'disable_days' in self.options:
            self.timerange = self.options['timerange']
        else:
            self.timerange = ''
        
        self.kpi_view = False
        if 'kpi_view' in self.options:
            if self.options['kpi_view'] == True:
                self.kpi_view = True
        
        self.apply_seperation(seperation)
        self.apply_filter()
    
    def apply_seperation(self, seperation):
        self.seperation = False
        if seperation != self.seperation_aggregated:
            self.seperation        = self.seperation_field[seperation]
            self.seperation_object = self.seperation_objects[seperation]
            
    def apply_filter(self):
        self.filter_date_set  = False
        if 'date' in self.filter:
            if 'from' in self.filter['date'] and 'to' in self.filter['date']:
                self.filter_date_from = self.filter['date']['from']
                self.filter_date_to   = self.filter['date']['to']
                self.filter_date_set  = True
    
    def get_dimension_filter(self):
        dim_filter = []
        print self.filter
        for dimension in self.dimensions:
            if dimension in self.filter:
                if self.filter[dimension] != None:
                    sql = dimension + '_id IN(%s)' % (', '.join(str(int(d)) for d in self.filter[dimension]))
                    dim_filter.append(sql)
        
        return dim_filter
    
    def get_filter_sql(self):
        
        dim_filter = self.get_dimension_filter()
        dim_filter.append(self.get_filter_date())
        
        print "hellllloooooo2123"
        if self.timerange != '':
            print "hellllloooooo"
            dim_filter.append('((days = {0} AND days_distance!=0) OR (days+days_distance > {0} AND days < {0}))'.format(self.timerange))
        
        sql = ' AND '.join(part for part in dim_filter)
        
        if sql != "":
            sql = ' WHERE ' + sql
        
        return sql
    
    def get_date_range(self):
        """
        Builds a date range from the given date filter
        """

        start = datetime.strptime(self.filter_date_from, '%Y-%m-%d')
        stop  = datetime.strptime(self.filter_date_to, '%Y-%m-%d')

        difference = stop - start
        rangelist = list(rrule.rrule(rrule.DAILY, count=difference.days + 1, dtstart=start))
        
        rangelist = map(lambda d: d.strftime('%Y-%m-%d'), rangelist)
        
        return rangelist 
    
    def get_json(self):
        data = self.get_data()
        if self.seperation:
            data_view = []
            for d in data:
                data_view.append({
                    "key"    : d,
                    "values" : data[d]
                })
            _json = json.dumps(data_view)
        else:
            _json = json.dumps(data)
        return _json
    
    def get_filter_date(self):
        filter = ""
        if(self.filter_date_set):
            filter = ' (`' + self.date_column + '` BETWEEN "%s" AND "%s") ' % (self.filter_date_from, self.filter_date_to)
        return filter
    
    def get_group_by(self):
        group_items = []
        if not self.kpi_view:
            group_items.append(self.date_column)
        if self.seperation:
            group_items.append(self.seperation)
        
        group_by = False
        if len(group_items) > 0:
            group_by = ', '.join(group_items) 
        
        return group_by 
        
    def get_order_by(self):
        return self.get_group_by()
    
    def get_data_kpi(self):
        filter   = self.get_filter_sql()
        model    = self.model
        group_by = self.get_group_by()
        if group_by:
            group_by = " GROUP BY " + group_by
        else:
            group_by = ""
            
        order_by = self.get_order_by()
        if order_by:
            order_by = " ORDER BY " + order_by
        else:
            order_by = ""
            
        seperation = ', ' + self.seperation if self.seperation else ''
        
        per_unit = ''
        if 'per_unit' in self.options:
            per_unit = self.per_unit_divider
        
        raw_data = self.hydration.objects.raw("""
            SELECT 
                id, 
                """ + self.get_value_field() + per_unit + """ as `value`
                """ + seperation + """
            FROM 
                """ + self.table + """
            """ + filter + """
            """ + group_by + """
            """ + order_by + """
        """)
        print raw_data
        return raw_data
    
    def get_data_bubble(self):
        filter   = self.get_filter_sql()
        model    = self.model

        group_by = self.get_group_by()
        if group_by:
            group_by = " GROUP BY " + group_by
        else:
            group_by = ""
        
        per_unit = ''
        if 'per_unit' in self.options:
            per_unit = self.per_unit_divider
        
        seperation = ', ' + self.seperation if self.seperation else ''
        
        raw_data = self.hydration.objects.raw("""
            SELECT 
                id, 
                """ + self.get_value_field() + per_unit + """ as `value`
                """ + seperation + """
            FROM 
                """ + self.table + """
            """ + filter + """ 
            """ + group_by + """
        """)
        return raw_data
    
    def get_data(self):
        filter   = self.get_filter_sql()
        model    = self.model
        group_by = self.get_group_by()
        if group_by:
            group_by = " GROUP BY " + group_by
        else:
            group_by = ""
            
        order_by = self.get_order_by()
        if order_by:
            order_by = " ORDER BY " + order_by
        else:
            order_by = ""
        seperation = ', ' + self.seperation if self.seperation else ''
        
        per_unit = ''
        if 'per_unit' in self.options:
            per_unit = self.per_unit_divider
        
        raw_data = self.hydration.objects.raw("""
            SELECT 
                id, 
                `""" + self.date_column + """`, 
                """ + self.get_value_field() + per_unit + """ as `value`
                """ + seperation + """
            FROM 
                """ + self.table + """
            """ + filter + """ 
            """ + group_by + """
            """ + order_by + """
        """)
        print raw_data
        return self.transform(raw_data)
    
    def transform_seperated(self, raw_data):
        reduced = {}
        date_range = self.get_date_range()
        
        for line in raw_data:
            sep_id = getattr(line, self.seperation)
            sep_obj = self.seperation_object.objects.get(pk=sep_id)
            line_date = str(getattr(line, self.date_column).strftime('%Y-%m-%d'))
            if not sep_obj.name in reduced:
                reduced[sep_obj.name] = {}
            reduced[sep_obj.name][line_date] = {'value': line.value, 'date': int(getattr(line, self.date_column).strftime('%s000'))}
        
        sorted = {}
        
        for campaign in reduced:
            sorted[campaign] = []
            for date in date_range:
                if date in reduced[campaign]:
                    val = reduced[campaign][date]['value'] if reduced[campaign][date]['value'] else 0
                    tmp = [reduced[campaign][date]['date'], val]
                    sorted[campaign].append(tmp)
                else:
                    placeholder = int(datetime.strptime(date, '%Y-%m-%d').strftime('%s000'))
                    sorted[campaign].append([placeholder, 0])
        
        return sorted
        
    def transform_unseperated(self, raw_data):
        date_range = self.get_date_range()
        data = []
        date_counter = 0
        for d in raw_data:
            date_attr = getattr(d, self.date_column)
            if date_attr.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(date_attr.strftime('%s000')), d.value])
            else:
                placeholder = int(datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000'))
                data.append([placeholder, 0])
            date_counter += 1
        return data
    
    def transform(self, raw_data):
        if self.seperation:
            return self.transform_seperated(raw_data)
        return self.transform_unseperated(raw_data)

class RoiMetric(BasicMetric):
    
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = CustomerCLV
    
    def get_value_field(self):
        if self.timerange == '':
            return "SUM(`clv_" + self.model + "_added`)/SUM(cost_added)*100"
        return "SUM(`clv_" + self.model + "_total`)/SUM(cost_total)*100"


class CustomerCountMetric(BasicMetric):
    
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = CustomerCLV
    
    def get_value_field(self):
        return "COUNT(DISTINCT customer_id)"
   
    
class ProfitMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT customer_id)"
    
    def get_value_field(self):
        if self.timerange == '':
            return "SUM(`clv_" + self.model + "_added` - cost_added)"
        return "SUM(`clv_" + self.model + "_total` - cost_total)"

    
    
class ClvMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT customer_id)"
    
    def get_value_field(self):
        if self.timerange == '':
            return "SUM(`clv_" + self.model + "_added`)"
        return "SUM(`clv_" + self.model + "_total`)"
    
    
   

    
class RevenueMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = Attributions
    per_unit_divider = "/count(DISTINCT customer_id)"
    
    def get_value_field(self):
        if self.timerange == '':
            return "SUM(`revenue_" + self.model + "_added`)"
        return "SUM(`revenue_" + self.model + "_total`)"
        
    
class CostMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT customer_id)"
    
    def get_value_field(self):
        if self.timerange == '':
            return "SUM(cost_added)"
        return "SUM(cost_total)"

class OrderRoiMetric(BasicMetric):
    
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    
    def get_value_field(self):
        return "SUM(`clv_" + self.model + "_added`)/SUM(cost_added)*100"


class OrderCountMetric(BasicMetric):
    
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    
    def get_value_field(self):
        return "COUNT(DISTINCT order_id)"
   
    
class OrderProfitMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT order_id)"
    
    def get_value_field(self):
        return "SUM(`clv_" + self.model + "_added` - cost_added)"
    
class OrderValueMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT order_id)"
    
    def get_value_field(self):
        return "SUM(`clv_" + self.model + "_added`)"
    
class OrderRevenueMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT order_id)"
    
    def get_value_field(self):
        return "SUM(`revenue_" + self.model + "_added`)"
        
    
class OrderCostMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'date'
    hydration   = CustomerCLV
    per_unit_divider = "/count(DISTINCT order_id)"
    
    def get_value_field(self):
        return "SUM(cost_added)"


METRICS = {
    'roi': {
        'label': 'Return on Investment', 
        'class': RoiMetric, 
        'options': {}
    },
    'profit_per_customer':  {
        'label': 'Profit (per Customer)', 
        'class': ProfitMetric, 
        'options': {
            'per_unit': True
        }
    },
    'clv': {
        'label': 'Customer Lifetime Value', 
        'class': ClvMetric, 
        'options': {
            'per_unit': True
        }
    },                 
    'cac': {
        'label': 'Customer Acquisition Cost', 
        'class': CostMetric, 
        'options': {
            'per_unit': True
        }
    },                 
    'revenue_per_customer': {
        'label': 'Revenue (per Customer)', 
        'class': RevenueMetric, 
        'options': {
            'per_unit': True
        }
    },  
    'profit_total': {
        'label': 'Profit (total)', 
        'class': ProfitMetric, 
        'options': {
        }
    },        
    'customer_equity': {
        'label': 'Customer Equity', 
        'class': ClvMetric, 
        'options': {
        }
    },     
    'marketingspend': {
        'label': 'Marketing Spend', 
        'class': CostMetric, 
        'options': {}
    },      
    'revenue_total': {
        'label': 'Revenue (total)', 
        'class': RevenueMetric, 
        'options': {}
    },
    'customer_count': {
        'label': 'No. of Customers', 
        'class': CustomerCountMetric, 
        'options': {
            'disable_days': True
        }
    }
}

METRICS_ORDER = {
    'order_roi': {
        'label': 'Order ROI', 
        'class': OrderRoiMetric, 
        'options': {
            'per_order': True
        }
    },
    'profit_per_order':  {
        'label': 'Profit (per Order)', 
        'class': OrderProfitMetric, 
        'options': {
            'per_unit' : True,
            'per_order': True
        }
    },
    'order_value': {
        'label': 'Value (per Order)', 
        'class': OrderValueMetric, 
        'options': {
            'per_unit' : True,
            'per_order': True
        }
    },                 
    'cost_per_order': {
        'label': 'Cost (per Order)', 
        'class': OrderCostMetric, 
        'options': {
            'per_unit' : True,
            'per_order': True
        }
    },                 
    'revenue_per_order': {
        'label': 'Revenue (per Order)', 
        'class': OrderRevenueMetric, 
        'options': {
            'per_unit' : True,
            'per_order': True
        }
    },  
    'order_profit_total': {
        'label': 'Profit (total)', 
        'class': OrderProfitMetric, 
        'options': {
            'per_order': True
        }
    },        
    'order_value': {
        'label': 'Order Value', 
        'class': OrderValueMetric, 
        'options': {
            'per_order': True
        }
    },     
    'value_per_order': {
        'label': 'Value (per order)', 
        'class': OrderValueMetric, 
        'options': {
            'per_order': True,
            'per_unit' : True
        }
    },     
    'order_count': {
        'label': 'Number of Orders', 
        'class': OrderCountMetric, 
        'options': {
            'disable_days': True
        }
    }
}

SEPERATIONS = {
    'channel'   : 'by channel' ,
    'partner'   : 'by partner' ,
    'campaign'  : 'by campaign',
    'aggregated': 'aggregated' ,
}
