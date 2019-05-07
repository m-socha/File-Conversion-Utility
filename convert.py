from os import listdir
from os.path import isfile
import sys
from enum import Enum
import re

class Format(Enum):
  panasonic = 'panasonic'
  phone = 'phone'

FORMAT_TO_REGEX = {
  Format.panasonic: re.compile('^\d{2}-\d{2}-\d{4}_\d{6}\.m2ts$'),
  Format.phone: re.compile('^\d{8}_\d{6}P\.m2ts$'),
}

def print_usage():
  src_file = sys.argv[0]
  print('Usage: %s {%s}' % (src_file, ', '.join([e.value for e in Format])))
  print()
  print('The argument refers to the initial format (e.g. "panasonic" converts from panasonic to phone format).')
  exit()

try:
  src_format = Format[sys.argv[1]]
except:
  print_usage()

files = [f for f in listdir() if isfile(f)]
regex = FORMAT_TO_REGEX[src_format]
filtered_files = [f for f in files if regex.match(f)]
