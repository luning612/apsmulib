'''
Created on Feb 10, 2017

@author: Alex
'''
import urlparse,re
def _encode_query(v):
    return v[0].replace(",","$C") if len(v)==1 else '(empty)'
def _get_parsed_raw(url):
    parsed = urlparse.urlparse(url)
    return urlparse.parse_qs(parsed.query)
def extract_user_content(url,domain):
    query = None
    read_id = None
    download_id = None
    if re.match(r'.*\.lawnet\.sg$',domain):
        params_raw = _get_parsed_raw(url)
        for k,v in  params_raw.iteritems():
            if k =='docguid':
                download_id = _encode_query(v)
    if re.match(r'.*\.westlaw\..*$',domain):
        params_raw = _get_parsed_raw(url)
        for k,v in  params_raw.iteritems():
            if k =='queryStr':
                query       = _encode_query(v)
            if k == 'docguid':
                read_id     =  _encode_query(v)
    if re.match(r'.*\.ebscohost\.com$',domain):
        params_raw = _get_parsed_raw(url)
        for k,v in  params_raw.iteritems():
            if k =='bquery':
                query       = _encode_query(v)
    if re.match(r'.*\.myilibrary\.com$',domain):
        params_raw = _get_parsed_raw(url)
        for k,v in  params_raw.iteritems():
            if k =='tid':
                read_id       = _encode_query(v)
    if re.match(r'.*\.ebrary\.com$',domain):
        params_raw = _get_parsed_raw(url)
        temp_query = None
        is_query = True
        for k,v in  params_raw.iteritems():
            if k =='p00':
                temp_query  = _encode_query(v)
            if k == 'docID':
                is_query = False
        if is_query: query = temp_query
    return (query, read_id, download_id)
        
        
    