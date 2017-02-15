'''
Created on Jan 18, 2017

@author: Alex
'''
import csv,traceback,urllib,re,urlparse
import sys, cleaning.url_filter as url_filter

working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'May2016removedlines(anony).txt'
target_domain =  "westlaw1"
patterns = []

def correct_empty_string(alist):
    if len(alist)==1 and len(alist[0])==0: return []
    else: return alist
def in_domain_list(domain):
    return domain in ["westlaw.co.uk", "westlaw.com","westlaw.co"]
def tokenize(url_info):
#     print ("url_info  "+url_info)
    parsed = urlparse.urlparse(url)
    params_raw = urlparse.parse_qs(parsed.query)
    params = dict.keys(params_raw)
    sub_doms_sec  = parsed.path
    #print "sub_doms_sec   "+ sub_doms_sec
    sub_doms_raw = sub_doms_sec.split("/")
    for idx, sub_dom in enumerate(sub_doms_raw):
        length = len(sub_dom)
        if sub_dom.isdigit():
            sub_doms_raw[idx] = "$NUM%s" % (length)
        elif length>=12 and re.compile('\d').search(sub_dom) and re.compile('[a-zA-Z]').search(sub_dom) and re.match("^[a-zA-Z0-9_]*$", sub_dom):
            sub_doms_raw[idx] = "$ALN%s" % (length)
        elif length>=16 and not re.match("^[a-zA-Z0-9_]*$", sub_dom):
            sub_doms_raw[idx] = "$STR%s" % (length)
    return correct_empty_string(sub_doms_raw), correct_empty_string(params)
def post_pattern(url):
#     url_info = url.split("//",1)[1]
    new_sub_doms, new_params = tokenize(url)
#     print ("new_sub_doms   " + str(new_sub_doms))
#     print ("new_params    " + str(new_params))
    match_index = -1
    for idx, pattern in enumerate(patterns):
        if_prm_match = pattern['prm'] == new_params
        if_sdo_match = pattern['sdo'] == new_sub_doms
        if if_prm_match and if_sdo_match:
            match_index = idx
    if match_index != -1: 
        patterns[match_index]['count']  += 1
    else:
        # create new Pattern
        ptrn = {'url': url, 'prm': [], 'sdo':[], 'prmlen': 0, 'sdolen':0, 'count':1}
    #     for p in new_params:
    #         ptrn['prm'].append([p,0])
    #     for d in new_sub_doms:
    #         ptrn['sdo'].append([d,0])
        ptrn['prm'] = new_params
        ptrn['sdo'] = new_sub_doms
        patterns.append(ptrn)
#         print ("created new "+ ptrn['url'])
def print_result():
    with open(working_dir+"domain_patterns_"+target_domain+".csv", 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for pattern in patterns:
            pattern_str = "/".join(pattern['sdo'])+"?"+"&".join(pattern['prm'])
            writer.writerow([pattern_str, pattern['count'], pattern['url']])
def correct_time_token(row):
    new_row = row[:3]
    new_row.append(row[3]+' '+row[4])
    new_row.extend(row[5:9])
    return new_row
input_file = working_dir+ input_file_name
with open(input_file, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    input_counter = 0
    for row in reader:
        try:
#             input_counter += 1
#             if input_counter == 10: break
            new_row = correct_time_token(row)
            url = new_row[4].split(' ')[1]
            domain_full = url.split('/')[2]
            domain_w_port = domain_full.split('.', 1)[1]
            domain = domain_w_port.split(':', 1)[0]
            if not in_domain_list(domain): continue
            if url_filter.is_rubbish(url): continue
            post_pattern(url)
        except:
            print traceback.print_exc()
            print "Exception:  " + row
print_result()