'''
Created on Feb 10, 2017

@author: Alex
'''
import urlparse,re
def extract_user_content(url,domain):
    parsed = urlparse.urlparse(url)
    params_raw = urlparse.parse_qs(parsed.query)
    query = None
    read_id = None
    download_id = None
    if re.match(r'.*\.lawnet\.sg$',domain):
        for k,v in  params_raw.iteritems():
            if k =='queryStr':
                query = v
            if k == 'pdfFileName':
                download_id = v
            if k == 'contentDocID':
                read_id = v
    return query, read_id, download_id
        
        
    