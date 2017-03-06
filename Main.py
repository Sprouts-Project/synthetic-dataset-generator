'''
Created on 11 feb. 2017

@author: Alvaro
'''
from faker import Factory
import json
import codecs
import bson
from datetime import datetime, tzinfo, timedelta
from dateutil import tz
import os
import bson
fake = Factory.create('en_US')
import pymongo


print fake.state()

print bson.ObjectId()

class simple_utc(tzinfo):
    def tzname(self):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)

#print fake.surname()
"""
for _ in range(1000):
    name = fake.profile()['name']
    name = name.split(" ")
    if len(name) > 2:
        print name
    print fake.profile()['residence']
"""
"""
print fake.date_time_between(start_date="-47y", end_date="-18y", tzinfo=tz.tzutc()).isoformat()
dir = os.path.dirname(__file__) #<-- absolute dir the script is in

with open(os.path.join(dir, 'outputs/reviews.json')) as customersfile:
    
    amzids = []
    customers = json.load(customersfile)
    for customer in customers:
        print customer
"""

id = str(bson.ObjectId())

id1 = str(bson.DBRef("customers", bson.objectid.ObjectId(id)).id)
id2 = str(bson.DBRef("customers", bson.objectid.ObjectId(id)).id)

print id1
print type(id2)

d = {}
d[id1] = 'asin'

print id2 in d

