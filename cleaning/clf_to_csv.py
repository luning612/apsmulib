'''
Created on Feb 8, 2017
This module transforms the given clf file to csv with, and splits out domain

@author: Alex
'''


import os
import csv,time
import domain_mapping
import query_rules, url_filter
from datetime import datetime

remove_junk = True

#setting the file path
working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\' +\
              'Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_fn = 'May2016removedlines(anony).txt'


input_file_path = os.path.join(working_dir, input_fn)

output_file = os.path.join(working_dir, "cleaned_"+input_fn+"May.csv")

#open a writer and pending for the write, the target is location is the first variable in open()

out_csv = csv.writer(open(output_file, 'wb'))
out_csv.writerow(["uip","rmtname","uid",
                  "datetime","timestamp","hour","day","dow","week","month","method",
                  "url","protocol","status","size","user-agent",
                  "domain","port","smt-domain","is-user-action",
                  "query-content","view-content","download-content"
                  ])

counter_junk = 0
counter_libproxy = 0
counter_ibproxy = 0
counter_row = 0

def correct_time_token(row):
    datetime_str = row[3]+' '+row[4]
    time_obj = datetime.strptime(datetime_str, "[%d/%b/%Y:%H:%M:%S +0800]")
    dt = time_obj.timetuple()
    dow = time_obj.isocalendar()[1]
    time_str = time_obj.strftime('%d/%m/%y %H:00:00')
    return time_str, time.mktime(dt), dt, dow

def decompose_url(row):
    method_url = row[5]
    tlist = method_url.split()
    method = tlist[0] #method
    url = tlist[1] #url
    protocol = "-"
    if len(tlist) == 3: protocol = tlist[2]
    domain_port = url.split('/', 3)[2]
    domain = domain_port.split(':')[0]
    port = domain_port.split(':')[1] if ':' in domain_port else ""
    smt_domain = domain_mapping.translate(domain) #semantic domain
    return method, url, protocol, domain, port, smt_domain

def encode_comma_in_ua(row):
    return row[8].replace(",","$C")
# determine if it's junk and maintains count for junks
def is_junk(url):
    global counter_libproxy, counter_ibproxy,counter_junk
    if url_filter.is_rubbish(url):
        counter_junk
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
    for row in reader:
        counter_row += 1
        # splitting and joining fields
        if remove_junk and not is_junk(row[5]):
            datetime_str, timestamp, dt_tuple, dow          = correct_time_token(row)
            method, url, protocol, domain, port, smt_domain = decompose_url(row)
            ua                                              = encode_comma_in_ua(row)
            query_tp = query_rules.extract_user_content(url, domain)
            is_ua = 1 if any(x is not None for x in query_tp) else 0
            new_query_tp = map(lambda q: "" if q is None else q, query_tp)
            download_content = "<size>" if row[7]>20000 and new_query_tp[2] else new_query_tp[2]
            '''
                  "uip","rmtname","uid",
                  "datetime","timestamp","hour","day","dow","week","month","method",
                  "url","protocol","status","size","user-agent",
                  "domain","port","smt-domain","is-user-action",
                  "query-content","view-content","download-content"
            '''
            # "timestamp","hour","day","dow","week","month"
            #new_row.extend([time.mktime(dt), dt[3],dt[2], dt[6], 
            #                time_obj.isocalendar()[1], dt[1]])        
            orow = row[0:3] + [datetime_str,timestamp, dt_tuple[3],dt_tuple[2],
                               dt_tuple[6], dow, dt_tuple[1]] + \
                   [method, url, protocol] + row[6:8] + \
                   [ua, domain, port, smt_domain, is_ua, new_query_tp[0], 
                    new_query_tp[1], new_query_tp[2]]
            out_csv.writerow(orow)
print 'rows: %s\njunks: %s\nlibproxy: %s\nibproxy: %s'%(counter_row, counter_junk,
                                                        counter_libproxy,counter_ibproxy)



