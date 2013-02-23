import mongobean.orm as orm

class MarketingCost(orm.Document):
	pass

class Click(orm.Document):
	pass

class Customer(orm.Document):
    
    class CustomerException(Exception):
        pass

    def clicks(self,filters = {}):
        if not 'custom_var_1_values' in self.keys():
            raise CustomerException("custom_var_1_value not defined!")
        filters['custom var value 1']= {'$in':self['custom_var_1_values']}
        return Click.collection.find(filters)

    def orders(self,filters = {}):
        filters['Customer ID'] = self['customer_id']
        return Order.collection.find(filters)

class CustomerIdMapping(orm.Document):
	pass

class Order(orm.Document):
	pass