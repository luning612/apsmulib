'''
Created on Feb 11, 2017

@author: Alex
'''

import csv,urllib,traceback, os
import re, time
from datetime import datetime
traceback.print_exc()
working_dir = 'L:\\Ezproxy (Hashed) 2016'
# working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'Apr2016removedlines(anony).txt'

domain_dic = {}
line_counter = 0
read_counter = 0
#read_max = 1000000
def is_junk(url):
    global counter_libproxy, counter_ibproxy,counter_junk
    for kwd in ['.gif','.min.js','.js', '.ttf', '.woff', '.eot']:
        if kwd in url :
            return True
    return False

input_file = os.path.join(working_dir, input_file_name)
with open(input_file, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        line_counter  += 1
        read_counter += 1
        try:
            #uid row[2]
            uid = row[2]
            time_obj = datetime.strptime(row[3]+" "+row[4], "[%d/%b/%Y:%H:%M:%S +0800]")
            ts = time.mktime(time_obj.timetuple())
            method = row[5].split(' ')[0]
            uri = row[5].split(' ')[1]
            
            domain_full = uri.split('/')[2]
            domain = domain_full.split('.', 1)[1]
            domain_encoded = domain.split(':')[0].replace("?","$Q").replace("<","$LT").replace(">","$GT").replace("*","$ST")
            
            if domain_encoded not in domain_dic:
                domain_dic[domain_encoded] = {'records':0, 'post':0,'junk':0, 
                                              'users':{},'lasttime':0, 
                                              'sessions':0}
            # anyways, append this url into its list
            this = domain_dic[domain_encoded]
            this["records"] += 1
            if method == "POST" : this["post"] += 1
            if is_junk(uri): 
                this['junk'] += 1
            else:
                lasttime = this["users"][uid] if uid in this["users"] else 0
                if uid not in this["users"]:  this["users"][uid] = ts
                if ts - lasttime > 30*60: this['sessions'] += 1
            
        except:
            print traceback.print_exc()
#     write_dmdic_to_file()
out_csv = csv.writer(open(os.path.join(working_dir,"domain_summary_apr.csv"), 'wb'))
out_csv.writerow(["domain","smt-domain","count","post","junk","users","sessions"])
for de,stat in domain_dic.iteritems():
    out_csv.writerow([de,"",stat['records'],stat['post'],stat['junk'],
                      len(stat['users']),stat['sessions']])

