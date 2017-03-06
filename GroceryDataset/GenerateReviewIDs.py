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
import datetime
import random
from bson import json_util

def probability(percent):
    r = random.random()
    if r <= percent:
        return True
    else:
        return False

fake = Factory.create('en_US')

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

reviews = [] #Keeps all the processed reviews
reviewerIDs = {} #Keeps all the processed reviewerIDs, mapped with the BSON DBRef identifier
asins = {} #Keeps all the processed asins, mapped with the BSON DBRef identifier
generated_ids = {} #Keeps all the generated IDs.
iter = 0
with open(os.path.join(dir, '../inputs/grocery_reviews.json')) as reviewsfile:
    
    for line in reviewsfile:
        review = json.loads(line)
        #25% probability for adding this review
        if probability(0.25):

            #--- CUSTOMER ID GENERATION AND DATE FORMATTING ---#
            reviewerID = review['reviewerID'] #Get the reviewer ID
            
            #Check if the ID for this reviewerID was already generated
            if reviewerID not in reviewerIDs:
                objectid = str(bson.ObjectId()) #generates a random BSON ID
                while objectid in generated_ids: #Checks if it had been generated
                    print 'collision'
                    objectid = str(bson.ObjectId())
                generated_ids[objectid] = reviewerID
                # Sets the customer by creating a DBRef using the objectID
                review['customer'] = bson.DBRef("customers", bson.objectid.ObjectId(objectid))
                # Sets this reviewerID with the DBRef object
                reviewerIDs[reviewerID] = bson.DBRef("customers", bson.objectid.ObjectId(objectid))
            else: # If the ID was already generated, assign it
                review['customer'] = reviewerIDs[reviewerID]
            # Formats the date by taking the review timestamp
            review['date'] = datetime.datetime.fromtimestamp(review['unixReviewTime']).replace(tzinfo=tz.tzutc())
            
            #--- ITEM ID GENERATION ---#
            asin = review['asin']
            if asin not in asins: #Check if the ID for this item was already generated
                objectiditem = str(bson.ObjectId())
                while objectiditem in generated_ids: #Checks for collisions
                    print 'collision'
                    objectiditem = str(bson.ObjectId())
                generated_ids[objectiditem] = asin 
                #Sets the item with the DBRef using the objectiditem
                review['item'] = bson.DBRef("items", bson.objectid.ObjectId(objectiditem))
                #Sets this asin with the DBRef object
                asins[asin] = bson.DBRef("items", bson.objectid.ObjectId(objectiditem))
            else:
                # If the asin was already generated, assign it
                review['item'] = asins[asin]
            
            #--- _id FOR REVIEW GENERATION ---#
            #_id generate review id
            objectidrev = str(bson.ObjectId())
            while objectidrev in generated_ids:
                print 'collision'
                objectidrev = str(bson.ObjectId())
            generated_ids[objectidrev] = 'review _id' #i just wanna keep the _id str
            review['_id'] = bson.objectid.ObjectId(objectidrev)

            reviews.append(review)
            
            #Prints each 10,000 iterations
            iter = iter + 1
            if iter%10000 == 0:
                print iter
                print review

print 'Number of generated reviews: ' + str(len(reviews))

with codecs.open(os.path.join(dir, '../outputs/reviews.json'), 'w', encoding="ISO-8859-1") as outfile:
    to_dump = json_util.dumps(reviews)
    print "I have dumped to BSON successfully"
    outfile.write(to_dump)
        