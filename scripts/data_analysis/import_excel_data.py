import xlrd
import sys
import datetime
import argparse

import cc_django.apps.utils.models as models
import cc_django.settings as settings

from django.core.management import setup_environ

setup_environ(settings)

def marketing_cost_row_mapper(row,type):
    row['type']=type
    return row

sheets = {
    'GA 1':
    {
        'model': models.Click,
        'mappers':
            {
                'date': lambda value,row:datetime.datetime.strptime("%d %d" % (int(value),int(row['hour'])),"%Y%m%d %H"),
                'hour': lambda value,row:int(value),
                'new_visits': lambda value,row:int(value),
                'visits': lambda value,row:int(value),
                'goal 1 completions': lambda value,row:int(value)
            }
    },
    'GA 2 - Customer ID matching':
    {
        'model': models.CustomerIdMapping,
        'mappers':
            {
                'date': lambda value,row:datetime.datetime.strptime("%d %d" % (int(value),int(row['hour'])),"%Y%m%d %H"),
            }
    },
    'Order Rev Data':
    {
        'model':models.Order,
        'mappers':
            {
                'Order date': lambda value,row:datetime.datetime(*xlrd.xldate_as_tuple(value,0))
            }
    },
    'Cost AdWords':
    {
        'model':models.MarketingCost,
        'row_mapper': lambda row:marketing_cost_row_mapper(row,type='adwords'),
        'mappers':
            {
                'date': lambda value,row:datetime.datetime.strptime("%d" % (int(value)),"%Y%m%d"),
            }
    },
    'Cost FB':
    {
        'model':models.MarketingCost,
        'row_mapper': lambda row:marketing_cost_row_mapper(row,type='fb'),
        'mappers':
            {
                'date': lambda value,row:datetime.datetime(*xlrd.xldate_as_tuple(value,0))
            }
    },
    'Cost AFF':
    {
        'model':models.MarketingCost,
        'row_mapper': lambda row:marketing_cost_row_mapper(row,type='affiliate'),
        'mappers':
            {
            }
    }
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='N', type=str, nargs=1,
                   help='the filename')
    parser.add_argument('-c','--clear',action='store_true')
    args = parser.parse_args()
    filename = args.filename[0]
    if args.clear:
        print "Clearing database before storing new objects..."
        clear = True
    else:
        clear = False
    with xlrd.open_workbook(filename) as wb:
        sh = wb.sheet_by_name('GA 1')
        for sheet in sheets.keys():
            print "Processing %s" % sheet
            if sheet in wb.sheet_names():
                rows = []
                sh = wb.sheet_by_name(sheet)
                row_names = sh.row_values(0)
                for rownum in range(1,sh.nrows):
                    row = dict(zip(row_names,sh.row_values(rownum)))
                    for key in row.keys():
                        if key in sheets[sheet]['mappers']:
                            row[key] = sheets[sheet]['mappers'][key](row[key],row)
                    rows.append(row)
                if clear:
                    sheets[sheet]['model'].collection.drop()
                cls = sheets[sheet]['model']
                for row in rows:
                    modelInstance = cls(**row)
                    modelInstance.save()
                print "%d objects of class %s in DB." % (cls.collection.find().count(),cls.__name__)
