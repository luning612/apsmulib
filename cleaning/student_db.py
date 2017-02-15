'''
Created on Feb 15, 2017

@author: Alex
'''


import os,sys,traceback
import csv,time
import query_rules, url_filter
from datetime import datetime

remove_junk = True
domain_dic = {}

#setting the file path
# working_dir = os.getcwd()
# working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\' +\
#               'Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
working_dir = 'L:\\Ezproxy (Hashed) 2016'
input_fn = sys.argv[1]
input_file_path = os.path.join(working_dir, input_fn)
print "Reading ... "
output_file = os.path.join(working_dir, "session_"+input_fn+".csv")

#open a writer and pending for the write, the target is location is the first variable in open()



counter_junk = 0
counter_libproxy = 0
counter_ibproxy = 0
counter_row = 0

def correct_time_token(row):
    datetime_str = row[3]+' '+row[4]
    time_obj = datetime.strptime(datetime_str, "[%d/%b/%Y:%H:%M:%S +0800]")
    dt = time_obj.timetuple()
    time_str = time_obj.strftime('%d/%m/%y %H:00:00')
    return time_str, time.mktime(dt)

def decompose_url(row):
    method_url = row[5]
    tlist = method_url.split()
    url = tlist[1] #url
    domain_port = url.split('/', 3)[2]
    domain = domain_port.split(':')[0]
#     smt_domain = domain_mapping.translate(domain) #semantic domain
    return domain,url

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
    return False
with open(input_file_path, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        try:
            counter_row += 1
            # splitting and joining fields
            if remove_junk and not is_junk(row[5]):
                datetime_str, timestamp          = correct_time_token(row)
                domain, url= decompose_url(row)
                query_tp = query_rules.extract_user_content(url, domain)
                is_ua = 1 if any(x is not None for x in query_tp) else 0
                new_query_tp = map(lambda q: 0 if q is None else 1, query_tp)
                if domain not in domain_dic:
    #                 "ip$id":[("datetime",timestamp,count,query-count,view-count,download-count,start_time)]
                    domain_dic[domain] = {}
                keyid = row[0]+"$"+row[2]
                new_tuple = [datetime_str,timestamp,1,new_query_tp[0],new_query_tp[1],new_query_tp[2], datetime_str]
                if keyid not in domain_dic[domain]:
                    domain_dic[domain][keyid] = [new_tuple]
                else:
                    last_record  = domain_dic[domain][keyid][-1]
                    if timestamp - last_record[1] >30*60:
                        domain_dic[domain][keyid].append(new_tuple)
                    else:
                        last_record[0] = datetime_str
                        last_record[1] = timestamp
                        last_record[2] += 1
                        last_record[3] += new_query_tp[0]
                        last_record[4] += new_query_tp[1]
                        last_record[5] += new_query_tp[2]
            
        except:
            print traceback.print_exc()
            print "Exception:  " + row
print "writing to %s ... "%(output_file)
out_csv = csv.writer(open(output_file, 'wb'))
out_csv.writerow(["uip","uid","domain","starttime","endtime","hour","day","dow","week","month","count","query-count","view-count","download-count"])
# "ip$id":[("datetime",timestamp,count,query-count,view-count,download-count)]
for domain, stlist in domain_dic.iteritems():
    for keyid, sttuplelist in stlist.iteritems():
        sip = keyid.split("$")[0]
        sid = keyid.split("$")[1]
        for index, sttuple in enumerate(sttuplelist):
            time_obj = datetime.strptime(sttuple[0], '%d/%m/%y %H:00:00')
            dtt = time_obj.timetuple()
            dow = time_obj.isocalendar()[1]
            orow = [sip, sid, domain, sttuple[6],sttuple[0],dtt[3],dtt[2],dtt[6], 
                    dow, dtt[1], sttuple[2], sttuple[3], sttuple[4],sttuple[5]]
            out_csv.writerow(orow)
print "===================="