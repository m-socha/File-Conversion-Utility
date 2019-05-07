from os import listdir
from os.path import isfile

files = [f for f in listdir() if isfile(f)]
