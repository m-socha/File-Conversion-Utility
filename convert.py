from os import listdir, rename
from os.path import isfile
import sys
from enum import Enum
import re

class Format(Enum):
  panasonic = 'panasonic'
  phone = 'phone'

FORMAT_TO_REGEX = {
  Format.panasonic: re.compile('^\d{2}-\d{2}-\d{4}_\d{6}\.m2ts$'),
  Format.phone: re.compile('^\d{8}_\d{6}p\.m2ts$'),
}

def print_usage():
  src_file = sys.argv[0]
  print('Usage: %s {%s}' % (src_file, ', '.join([e.value for e in Format])))
  print()
  print('The argument refers to the initial format (e.g. "panasonic" converts from panasonic to phone format).')
  exit(1)

def get_converted_filename(filename, src_format):
  if src_format == Format.panasonic:
    month = filename[:2]
    day = filename[3:5]
    year = filename[6:10]
    time = filename[11:17]
    return year + month + day + '_' + time + 'p.m2ts'
  elif src_format == Format.phone:
    year = filename[:4]
    month = filename[4:6]
    day = filename[6:8]
    time = filename[9:15]
    return month + '-' + day + '-' + year + '_' + time + '.m2ts'

try:
  src_format = Format[sys.argv[1]]
except:
  print_usage()

filenames = [f for f in listdir() if isfile(f)]
regex = FORMAT_TO_REGEX[src_format]
filtered_filenames = [f for f in filenames if regex.match(f)]

if not filtered_filenames:
  print('No files found to convert.')
  exit()

converted_filenames = [get_converted_filename(f, src_format) for f in filtered_filenames]
for filename, converted_filename in zip(filtered_filenames, converted_filenames):
  rename(filename, converted_filename)
  print('%s --> %s' % (filename, converted_filename))
