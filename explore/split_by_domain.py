'''
Created on Jan 15, 2017

@author: Alex
'''
import csv,urllib,traceback
import re
traceback.print_exc()
# working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
working_dir = 'F:\\Y4T2\\AP\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\Alma User & Jan16 EzProxy (for Swapna) 9Nov16\\'
input_file_name = 'Jan 2016removedlies(anony).txt'
output_folder_name = "domains_lg"
domain_dic = {}
domain_list = []
line_counter = 0
read_counter = 0
#read_max = 1000000

def construct_dmf_pth(domain):
    return output_dir + domain +".txt"
def write_dmdic_to_file():
    for de in domain_dic:
        with open(construct_dmf_pth(de),"a+") as dmf:
            for duri in domain_dic[de]['records']:
                dmf.write(duri+"\n")
        domain_dic[de] = {'records':[], 'post':0, 'count':0}
def is_rubbish_url(url):
    if '.gif' in url:
        return True
    if '.ico' in url:
        return True
    if '.js' in url:
        return True
    return False

input_file = working_dir + input_file_name
output_dir = working_dir + output_folder_name + "\\"
with open(input_file, 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096),' ')
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    for row in reader:
        line_counter  += 1
        read_counter += 1

        try:
            method = row[5].split(' ')[0]
            if method == "POST":
                continue
            uri = row[5].split(' ')[1]
#             if "query" not in uri.lower() and not re.match( r'.*\Wq=.*', uri.lower(), re.M|re.I):
#                 continue
#             if re.match( r'.*\Wjquery.*', uri.lower(), re.M|re.I):
#                 continue
            if is_rubbish_url(uri):
                continue
            domain_full = uri.split('/')[2]
            domain = domain_full.split('.', 1)[1]
            domain_encoded = domain.replace(":","$C").replace("?","$Q").replace("<","$LT").replace(">","$GT").replace("*","$ST")
            
            if domain_encoded not in domain_list:
                f = open(construct_dmf_pth(domain_encoded),"w+")
                domain_list.append(domain_encoded)
                domain_dic[domain_encoded] = {'records':[], 'post':0, 'count':0}
            # anyways, append this url into its list

            domain_dic[domain_encoded]["records"].append(uri)
            if line_counter == 100000:
                # purge domain_dic, write lines to file
                write_dmdic_to_file()
                
        except:
            print traceback.print_exc()
            print "Exception: " + row[5]
    write_dmdic_to_file()

# def get_domain_from_url(url):
#     

