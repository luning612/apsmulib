'''
Created on Jan 21, 2017

@author: Ray
'''

#this version is created on mac, and can be used for MacOS only

import os
import csv,urllib,traceback
import re


#setting the file path
fileName = "example.txt"
working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'sample2.txt'


input_file_path = os.path.join(working_dir, input_file_name)

output_file = os.path.join(working_dir, "mycsv.csv")

#open a writer and pending for the write, the target is location is the first variable in open()
out_csv = csv.writer(open(output_file, 'wb'), quoting=csv.QUOTE_ALL)
out_csv.writerow(["uip","","uid","datetime","method","url","protocol","status","size","user-agent"])
#open the file and read 
# with open(inputFilePath, 'rb') as csvfile:
#     dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
#     csvfile.seek(0)
#     reader = csv.reader(csvfile, dialect)

# in_txt = csv.reader(open(inputFilePath, "rb"), delimiter = ' ',)

def correct_time_token(row):
    new_row = row[:3]
    new_row.append(row[3]+' '+row[4])
    new_row.extend(row[5:9])
    return new_row

def split_method_and_url(row):
    new_row = row[:4]
    tlist = row[4].split()
    new_row.append(tlist[0])
    new_row.append(tlist[1])
    try:
        new_row.append(tlist[2])
    except IndexError:
        new_row.append("-")
    new_row.extend(row[5:9])
    return new_row

with open(input_file_path, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    conversion = set('[]')
    for row in reader:
        row2 = [''.join('' if c in conversion else c for c in entry) for entry in row]
        row3 = correct_time_token(row2)
        row4 = split_method_and_url(row3)
        out_csv.writerow(row4)


# use 'with' if the program isn't going to immediately terminate
# so you don't leave files open
# the 'b' is necessary on Windows
# it prevents \x1a, Ctrl-z, from ending the stream prematurely
# and also stops Python converting to / from different line terminators
# On other platforms, it has no effect





