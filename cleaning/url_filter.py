'''
Created on Feb 15, 2017

@author: Alex
'''
def is_rubbish(url):
    for kwd in ['.gif','.js', '.css','.ico','.png','.jpg', '.ttf', '.woff', '.eot']:
        if kwd in url: return True
    return False