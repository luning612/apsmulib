'''
Created on Feb 11, 2017

@author: Alex
'''
from datetime import datetime
import time
t1 = '[01/Jan/2016:00:00:38 +0800]'
t2 = '[01/Jan/2016:00:01:37 +0800]'
time_obj1 = datetime.strptime(t1, "[%d/%b/%Y:%H:%M:%S +0800]")

time_obj2 = datetime.strptime(t2, "[%d/%b/%Y:%H:%M:%S +0800]")
ts1 = time.mktime(time_obj1.timetuple())
ts2 = time.mktime(time_obj2.timetuple())
ic = time_obj1.isocalendar()[1]
tp = (1,2,3,None)
new_query_tp = map(lambda q: "" if q is None else q + 1, tp)
print str(new_query_tp)

print ic
