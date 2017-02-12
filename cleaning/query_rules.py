'''
Created on Feb 10, 2017

@author: Alex
'''
import urlparse,re
def _encode_query(v):
    return v[0].replace(",","$C") if len(v)==1 else '(empty)'
def extract_user_content(url,domain):
    query = None
    read_id = None
    download_id = None
    if re.match(r'.*\.lawnet\.sg$',domain):
        parsed = urlparse.urlparse(url)
        params_raw = urlparse.parse_qs(parsed.query)
        for k,v in  params_raw.iteritems():
            if k =='queryStr':
                query       = _encode_query(v)
            if k == 'pdfFileName':
                download_id = _encode_query(v)
            if k == 'contentDocID':
                read_id     =  _encode_query(v)
    return (query, read_id, download_id)
        
        
    