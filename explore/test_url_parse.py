'''
Created on Feb 4, 2017

@author: Alex
'''
import urlparse,urllib2
unquoted = urllib2.unquote('https://www.lawnet.sg:443/lawnet/group/lawnet/legal-research/advanced-search?p_p_id=searchadvancedformportlet_WAR_lawnet3legalresearchportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_searchadvancedformportlet_WAR_lawnet3legalresearchportlet_isSearchExpression=true&_searchadvancedformportlet_WAR_lawnet3legalresearchportlet_action=vldbSearch&_searchadvancedformportlet_WAR_lawnet3legalresearchportlet_legisSearch=%28misrepresentation+act%29')
parsed = urlparse.urlparse('http://web.a.ebscohost.com:80/ehost/resultsadvanced?sid=31b67e7c-7594-4ea1-ab33-216ea12647a0%40sessionmgr4001&vid=9&hid=4209&bquery=(JN+%22Corporate+Social+Responsibility+%26+Environmental+Management%22+AND+DT+20140101)+AND+(singapore)&bdata=JmRiPWJ0aCZ0eXBlPTEmc2l0ZT1laG9zdC1saXZlJnNjb3BlPXNpdGU%3d')
print unquoted
path  = parsed.path
# print path
# print urlparse.parse_qs(parsed.query)
