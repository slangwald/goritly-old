import argparse
from cc_django.settings import *

UTILS_DATABASE = None

parser = argparse.ArgumentParser(description="Import CSV Files")
parser.add_argument('--utils-db',type=str)
args, unknown = parser.parse_known_args()
if args.utils_db:
    UTILS_DATABASE = args.utils_db
