'''
Created on Feb 10, 2017

@author: Alex
'''
import csv,traceback,urlparse

working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'sample2.txt'

out_csv = csv.writer(open(working_dir+'canremove.txt', 'wb'), quoting=csv.QUOTE_ALL)
out_csv.writerow(["row","query"])
def in_domain_list(domain):
    return domain == 'a.ebscohost.com'
def correct_empty_string(alist):
    if len(alist)==1 and len(alist[0])==0: return []
    else: return alist
def correct_time_token(row):
    new_row = row[:3]
    new_row.append(row[3]+' '+row[4])
    new_row.extend(row[5:9])
    return new_row
input_file = working_dir+ input_file_name
row_counter = 0
with open(input_file, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    input_counter = 0
    for row in reader:
        row_counter += 1
        try:
            new_row = correct_time_token(row)
            url = new_row[4].split(' ')[1]
            domain_full = url.split('/')[2]
            domain_w_port = domain_full.split('.', 1)[1]
            domain = domain_w_port.split(':', 1)[0]
            if not in_domain_list(domain): continue
            parsed = urlparse.urlparse(url)
            params_raw = urlparse.parse_qs(parsed.query)
            if 'bquery' in params_raw:
                out_csv.writerow([row_counter,params_raw['bquery']])
        except:
            print traceback.print_exc()
            print "Exception:  " + row
