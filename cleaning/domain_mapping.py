'''
Created on Feb 9, 2017
Purpose: to get semantic domain for each url
@author: Alex
'''
import re
domain_map = {"lawnet": ["*.lawnet.sg"],
              "westlaw":["*.westlaw.co.uk","*.westlaw.com","*.westlaw.co"],
              "Ebsco ebooks":["*.ebscohost.com"],
              "MyiLibrary":["*.myilibrary.com"],
              "ebrary":["*.ebrary.com"],
              "SAGE":["*.sagepub.com"],
              "MarketLine Advantage":["*.marketline.com"],
              "ProQuest":["*.eblib.com.au"],
              "Lexis":["*.lexis.com"],
              "SpringerLINK":["*.springer.com"],
              "Wiley":["*.wiley.com"],
              "OECD iLibrary":["*.oecd.org","*.sourceoecd.org","*.oecdilibrary.org"]}
def _domain_map_regex_generate(t):
    r_str = "^{}$".format(t).replace(".","\.").replace("*",".*")
    return re.compile(r_str)
for k in domain_map:
    for i,t in enumerate(domain_map[k]):
        domain_map[k][i] = _domain_map_regex_generate(t)
def translate(domain):
    for k in domain_map:
        for i,r in enumerate(domain_map[k]):
            if re.match(r, domain):
                return k
    
    return ""
        