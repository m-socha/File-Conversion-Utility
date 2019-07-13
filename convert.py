from os import listdir, rename
from os.path import isfile
import sys
from enum import Enum
import re
from datetime import datetime, timedelta

class Format(Enum):
  panasonic = 'panasonic'
  phone = 'phone'

FORMAT_TO_REGEX = {
  Format.panasonic: re.compile('^\d{2}-\d{2}-\d{4}_\d{6}\.m2ts$'),
  Format.phone: re.compile('^\d{8}_\d{6}p\.m2ts$'),
}

def print_usage():
  src_file = sys.argv[0]
  formats_str = ', '.join([e.value for e in Format])
  print('Usage: %s {%s}, {%s}, timeshift' % (src_file, formats_str, formats_str))
  print()
  print('The first argument is the source format.')
  print('The second argument is the destination format.')
  print('The third argument is an optional time shift in hours (e.g. 8 means 8 hours forward, -2 means 2 hours backward).')
  exit(1)

def get_time_from_filename(filename, src_format):
  if src_format == Format.panasonic:
    month = filename[:2]
    day = filename[3:5]
    year = filename[6:10]
    hour = filename[11:13]
    minute = filename[13:15]
    second = filename[15:17]
  elif src_format == Format.phone:
    year = filename[:4]
    month = filename[4:6]
    day = filename[6:8]
    hour = filename[9:11]
    minute = filename[11:13]
    second = filename[13:15]
  return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second));

def get_shifted_time(time, hour_shift):
  return time + timedelta(hours=hour_shift)

def get_filename_from_time(time, dest_format):
  if dest_format == Format.panasonic:
    return time.strftime('%m-%d-%Y_%H%M%S') + '.m2ts'
  elif dest_format == Format.phone:
    return time.strftime('%Y%m%d_%H%M%S') + 'p.m2ts'

try:
  src_format = Format[sys.argv[1]]
  dest_format = Format[sys.argv[2]]
  if (len(sys.argv) >= 4):
    hour_shift = int(sys.argv[3])
  else:
    hour_shift = 0
except:
  print_usage()

filenames = [f for f in listdir() if isfile(f)]
regex = FORMAT_TO_REGEX[src_format]
filtered_filenames = [f for f in filenames if regex.match(f)]

if not filtered_filenames:
  print('No files found to convert.')
  exit()

times = [get_time_from_filename(f, src_format) for f in filtered_filenames]
shifted_times = [get_shifted_time(t, hour_shift) for t in times]
converted_filenames = [get_filename_from_time(t, dest_format) for t in shifted_times]

for filename, converted_filename in zip(filtered_filenames, converted_filenames):
  rename(filename, converted_filename)
  print('%s --> %s' % (filename, converted_filename))
print('Files converted: %d' % (len(filtered_filenames)))
