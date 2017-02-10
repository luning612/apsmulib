'''
Created on Feb 8, 2017
This module transforms the given clf file to csv with, and splits out domain

@author: Alex
'''


import os
import csv
import domain_mapping

remove_junk = True

#setting the file path
working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'sample2.txt'


input_file_path = os.path.join(working_dir, input_file_name)

output_file = os.path.join(working_dir, "cleaned_"+input_file_name+".csv")

#open a writer and pending for the write, the target is location is the first variable in open()
out_csv = csv.writer(open(output_file, 'wb'), quoting=csv.QUOTE_ALL)
out_csv.writerow(["uip","rmtname","uid","datetime","method",
                  "url","protocol","status","size","user-agent",
                  "domain","port","smt-domain","is-user-action","query-content","view-content","download-content"])
counter_junk = 0
counter_libproxy = 0
counter_ibproxy = 0
counter_row = 0

def correct_time_token(row):
    new_row = row[:3]
    new_row.append(row[3]+' '+row[4])
    new_row.extend(row[5:9])
    return new_row

def split_method_and_url(row):
    new_row = row[:4]
    tlist = row[4].split()
    new_row.append(tlist[0]) #method
    new_row.append(tlist[1]) #url
    try:
        new_row.append(tlist[2]) #protocol
    except IndexError:
        new_row.append("-")
    new_row.extend(row[5:9])
    return new_row
def attach_decomposed_url_info(row):
    url = row[5]
    domain_port = url[8:].split('/')[0]
    domain = domain_port.split(':')[0]
    row.append(domain) #domain
    row.append(domain_port.split(':')[1]) #port
    row.append(domain_mapping.translate(domain) ) #semantic domain
# determine if it's junk and maintains count for junks
def is_junk(url):
    global counter_libproxy, counter_ibproxy,counter_junk
    for kwd in ['.gif','.min.js','.js', '.ttf', '.woff', '.eot']:
        if kwd in url :
            counter_junk += 1 
            return True
    if "//libproxy.smu.edu.sg:" in url:
        counter_libproxy += 1
        return True
    if "//ibproxy.smu.edu.sg:" in url:
        counter_ibproxy += 1
        return True
    return False
with open(input_file_path, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    conversion = set('[]')
    for row in reader:
        counter_row += 1
        # splitting and joining fields
        row2 = [''.join('' if c in conversion else c for c in entry) for entry in row]
        row3 = correct_time_token(row2)
        row4 = split_method_and_url(row3)
        attach_decomposed_url_info(row4)
        if remove_junk and not is_junk(row4[5]):
            out_csv.writerow(row4)
print 'rows: %s\n junks: %s\n libproxy: %s\n ibproxy: %s'%(counter_row, counter_junk,counter_libproxy,counter_ibproxy)



