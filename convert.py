from os import listdir
from os.path import isfile
import sys
from enum import Enum

class Format(Enum):
  phone = 'phone'
  panasonic = 'panasonic'

def print_usage():
  src_file = sys.argv[0]
  print('Usage: %s {%s}' % (src_file, ', '.join([e.value for e in Format])))
  print()
  print('The argument refers to the destination format (e.g. "phone" converts from panasonic to phone format).')
  exit()

try:
  dest_format = Format[sys.argv[1]]
except:
  print_usage()

print(dest_format)

files = [f for f in listdir() if isfile(f)]
