'''
Created on Dec 9, 2016

@author: Alex
'''
import csv,urllib
working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'Jan 2016removedlies(anony).txt'
domain_dic = {}
post_counter = 0
record_counter = 0

def correct_time_token(row):
    new_row = row[:3]
    new_row.append(row[3]+' '+row[4])
    new_row.extend(row[5:9])
    return new_row
def print_url(line):
    uri = line[4].split(' ')[1]
    #print "#####".join(uri)
    url_unquote =  urllib.unquote(uri)
    print url_unquote
def print_domain(line):
    uri = line[4].split(' ')[1]
    #print "#####".join(uri)
    url_unquote =  urllib.unquote(uri)
    domain = url_unquote[8:].split('/')[0]
    if domain not in domain_dic:
        domain_dic[domain] = 0
    domain_dic[domain] += 1
def is_js(url):
    if 'min.js' in url: 
        return True
    if '.gif' in url:
        return True
    if url[-3:] =='.js':
        return True
    if '?v=' in url:
        ending_index = url.index('?v=')
        if url[(ending_index-3):ending_index] =='.js':
            return True
    return False
def count_post(line):
    global post_counter
    method = line[4].split(' ')[0]
    if method == 'POST':
        post_counter+=1
def print_url_not_js(line):
    uri = line[4].split(' ')[1]
    #print "#####".join(uri)
    url_unquote =  urllib.unquote(uri)
    if not is_js(url_unquote):
        print url_unquote
def count_url_not_js(line):
    global record_counter
    uri = line[4].split(' ')[1]
    #print "#####".join(uri)
    url_unquote =  urllib.unquote(uri)
    if not is_js(url_unquote):
        record_counter +=1
def print_not_200(line):
    status = line[5]
    if status != '200':
        print line
input_file = working_dir+ input_file_name
csv.list_dialects
with open(input_file, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        new_row = correct_time_token(row)
        #action here
        #print_url_not_js(new_row)
        count_url_not_js(new_row)
    print record_counter
#     for domain in domain_dic:
#         print "{0} {1}".format(domain, domain_dic[domain])
