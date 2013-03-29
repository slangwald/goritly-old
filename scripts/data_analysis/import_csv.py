import sys, os
import argparse
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."))

import cc_django.settings as settings
from django.core.management import setup_environ

setup_environ(settings)



class CsvImporter():
	files = {
		
	}
	pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Import CSV Files")
	parser.add_argument('filename', metavar='filename', type=str, nargs=1,
	               help='the filename')
	parser.add_argument('-c','--clear',action='store_true')
	
	#parser.add_argument('keywords-brand'  id_matching.csv     orders.csv    returns.csv
	#clickchain.csv      marketing_cost.csv  products.csv  voucher.csv
	
	parser.add_argument('--keywords-brand',type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--id-matching', type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--orders', type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--returns', type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--clickchain',  type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--marketing-cost',type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--products', type=str, nargs=1,
	               help='the filename')
	parser.add_argument('--voucher', type=str, nargs=1,
	               help='the filename')
	
	args = parser.parse_args()
	
	