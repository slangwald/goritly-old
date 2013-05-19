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

    def __init__(self, model, filter, options = {}):
        """
        options = {
            'model':
            (stuff used by specific metrics)
        }
        """
        print filter
        self.filter  = filter
        self.options = options
        self.model   = model
        
        self.apply_filter()
        
    def apply_filter(self):
        self.filter_date_set  = False
        if 'date' in self.filter:
            if 'from' in self.filter['date'] and 'to' in self.filter['date']:
                self.filter_date_from = self.filter['date']['from']
                self.filter_date_to   = self.filter['date']['to']
                self.filter_date_set  = True
    
    def get_dimension_filter(self):
        
        dim_filter = []
        for dimension in self.dimensions:
            if dimension in self.filter:
                if self.filter[dimension] != None:
                    sql = dimension + '_id IN(%s)' % (', '.join(str(int(d)) for d in self.filter[dimension]))
                    dim_filter.append(sql)
        
        return dim_filter
    
    def get_filter_sql(self):
        
        dim_filter = self.get_dimension_filter()
        dim_filter.append(self.get_filter_date())
        
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
    
    def get_data(self):
        pass
    
    def get_json(self):
        return json.dumps(self.get_data())
    
    def get_filter_date(self):
        filter = ""
        if(self.filter_date_set):
            filter = ' (`' + self.date_column + '` BETWEEN "%s" AND "%s") ' % (self.filter_date_from, self.filter_date_to)
        return filter

class RoiMetric(BasicMetric):
    
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    
    def get_data(self):
        
        filter = self.get_filter_sql()
        
        model = self.model
        raw_data = CustomerCLV.objects.raw("""
            SELECT 
                id, 
                `first_ordered_at`, 
                SUM(`clv_""" + model + """_added`)/SUM(cost)*100 as summed
            FROM 
                utils_customerclv 
            
            """ + filter + """ 
            
            GROUP BY 
                `first_ordered_at`
            ORDER BY 
                `first_ordered_at`
        """)
        date_range = self.get_date_range()
        
        data = []
        date_counter = 0
        for d in raw_data:
            print "%s==%s" % (d.first_ordered_at, date_range[date_counter])
            if d.first_ordered_at.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(d.first_ordered_at.strftime('%s000')), d.summed])
            else:
                print date_range[date_counter]
                placeholder = datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000')
                data.append([placeholder, 0])
            date_counter += 1
        
        return data
    
class ProfitMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    
    def get_data(self):
        
        filter = self.get_filter_sql()
        
        model = self.model
        raw_data = CustomerCLV.objects.raw("""
            SELECT 
                id, 
                `first_ordered_at`, 
                SUM(`clv_""" + model + """_added`)/SUM(cost)*100 as summed
            FROM 
                utils_customerclv 
            
            """ + filter + """ 
            
            GROUP BY 
                `first_ordered_at`
            ORDER BY 
                `first_ordered_at`
        """)
        date_range = self.get_date_range()
        
        data = []
        date_counter = 0
        for d in raw_data:
            print "%s==%s" % (d.first_ordered_at, date_range[date_counter])
            if d.first_ordered_at.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(d.first_ordered_at.strftime('%s000')), d.summed])
            else:
                print date_range[date_counter]
                placeholder = datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000')
                data.append([placeholder, 0])
            date_counter += 1
        
        return data

class ClvMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    
    def get_data(self):
        
        per_unit = ''
        if 'per_unit' in self.options:
            per_unit = '/count(DISTINCT customer_id)'
        
        filter = self.get_filter_sql()
        
        model = self.model
        raw_data = CustomerCLV.objects.raw("""
            SELECT 
                id, 
                `first_ordered_at`, 
                SUM(`clv_""" + model + """_added`)""" + per_unit + """ as summed
            FROM 
                utils_customerclv 
            
            """ + filter + """ 
            
            GROUP BY 
                `first_ordered_at`
            ORDER BY 
                `first_ordered_at`
        """)
        date_range = self.get_date_range()
        
        data = []
        date_counter = 0
        for d in raw_data:
            print "%s==%s" % (d.first_ordered_at, date_range[date_counter])
            if d.first_ordered_at.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(d.first_ordered_at.strftime('%s000')), d.summed])
            else:
                print date_range[date_counter]
                placeholder = datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000')
                data.append([placeholder, 0])
            date_counter += 1
        
        return data

class RevenueMetric(BasicMetric):
    
    date_column = 'date'
    
    def get_data(self):
    
        filter = self.get_filter_sql()
        model  = self.model
        
        raw_data = Attributions.objects.raw("""
            SELECT 
                id, 
                SUM(`""" + model + """`) as summed
            FROM 
                utils_attributions 
            """ + filter + """ 
            GROUP BY 
                `date`
            ORDER BY 
                `date`
        """)
        
        date_range = self.get_date_range()
        data = []
        date_counter = 0
        for d in raw_data:
            print "%s==%s" % (d.date, date_range[date_counter])
            if d.date.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(d.date.strftime('%s000')), d.summed])
            else:
                print date_range[date_counter]
                placeholder = datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000')
                data.append([placeholder, 0])
            date_counter += 1
        
        
        return data
    
    

class CostMetric(BasicMetric):
    table       = 'utils_customerclv'
    date_column = 'first_ordered_at'
    
    def get_data(self):
        
        filter = self.get_filter_sql()
        
        per_unit = ''
        if 'per_unit' in self.options:
            per_unit = '/count(DISTINCT customer_id)'
        
        
        model = self.model
        raw_data = CustomerCLV.objects.raw("""
            SELECT 
                id, 
                `first_ordered_at`, 
                SUM(cost)""" + per_unit + """  as summed
            FROM 
                utils_customerclv 
            
            """ + filter + """ 
            
            GROUP BY 
                `first_ordered_at`
            ORDER BY 
                `first_ordered_at`
        """)
        date_range = self.get_date_range()
        
        data = []
        date_counter = 0
        for d in raw_data:
            print "%s==%s" % (d.first_ordered_at, date_range[date_counter])
            if d.first_ordered_at.strftime('%Y-%m-%d') == date_range[date_counter]:
                data.append([int(d.first_ordered_at.strftime('%s000')), d.summed])
            else:
                print date_range[date_counter]
                placeholder = datetime.strptime(date_range[date_counter], '%Y-%m-%d').strftime('%s000')
                data.append([placeholder, 0])
            date_counter += 1
        
        return data

METRICS = {
    'roi': {
        'label': 'Return on Investment', 
        'class': RoiMetric, 
        'options': {}
    },
    'profit_per_customer':  {
        'label': 'Profit (per Customer)', 
        'class': ProfitMetric, 
        'options': {}
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
        'options': {}
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
}