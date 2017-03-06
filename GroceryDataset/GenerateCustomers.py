'''
Created on 11 feb. 2017

@author: Alvaro
'''

import json
import os
import bson
from faker import Factory
import codecs
from dateutil import tz
from bson import json_util

fake = Factory.create('en_US')

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

reviewerIDs = {} #Reviewer IDs
customers = [] #Generated customers
iter = 0
with open(os.path.join(dir, '../inputs/reviews.json')) as reviewsfile:
    reviews = reviewsfile.read()
    
    reviews = json_util.loads(reviews)
    print len(reviews)
    
    for review in reviews:
        
        #---GENERATES THE CUSTOMER FROM THE REVIEW---#
        #Takes the reviewerID of this review
        reviewerID = review['reviewerID']
        #Checks if the Customer for this reviewerID was already created
        if reviewerID not in reviewerIDs:
            #Generates random data for the customer
            profile = fake.profile()
            customerID = review['customer'].id #Gets the BSON ObjectID of this customer
            customer = {
                    '_id' : bson.objectid.ObjectId(customerID),
                    'amzRevId': review['reviewerID'], #TODO unnecessary field
                    'name': profile['name'],
                    'state': fake.state(),
                    'email': profile['name'].replace(" ", "").lower() + '@'+ fake.free_email_domain(),
                    'sex': profile['sex'],
                    'birthdate': fake.date_time_between(start_date="-47y", end_date="-18y", tzinfo=tz.tzutc())
                }
            
            customers.append(customer)
            reviewerIDs[reviewerID] = review['customer']
        
        iter = iter + 1
        if iter%10000 == 0:
            print iter
            print customer
        #anadir referencia a la review

print 'Number of generated customers: ' + str(len(customers))
with codecs.open(os.path.join(dir, '../outputs/customers.json'), 'w', encoding="ISO-8859-1") as outfile:
    to_dump = json_util.dumps(customers)
    print "I have dumped to BSON successfully"
    outfile.write(to_dump)
        