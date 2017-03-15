'''
Created on 12 feb. 2017

@author: Alvaro
'''
import os
import codecs
import json
import bson
import random
from bson import json_util
dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def probability(percent):
    r = random.random()
    if r <= percent:
        return True
    else:
        return False

items = {}
#save all reviews in memory, using asin-item dictionary (extract just ObjectID)
with open(os.path.join(dir, 'reviews.json')) as reviewsfile:
    reviews = reviewsfile.read()
    #print len(reviews)
    reviews = json_util.loads(reviews)
    print 'I have loaded the reviews'
    for review in reviews:
        
        if review['asin'] not in items:
            items[review['asin']] = str(review['item'].id)
            #print type(items[review['asin']])
#loop items file
items_modified = []
print 'I am going to load the items metadata'
#generated_ids = []
iter = 0
without_reviews = 0
without_prices = 0
all_ids = {}
with open(os.path.join(dir, 'meta_Digital_Music_fixed.json')) as itemsfile:
    items_loaded = json.load(itemsfile)
    for item in items_loaded:

        if item['asin'] in items:
            item['_id'] = bson.objectid.ObjectId(items[item['asin']])
            #print type(item['_id'])
            #print items[item['asin']]
            items_modified.append(item)
            all_ids[str(item['_id'])] = item['asin']
        #If item has not review, we generate its _id
        else:
            new_id = str(bson.ObjectId())
            while new_id in all_ids:
                new_id = str(bson.ObjectId())
                print 'Conflict!'
            without_reviews = without_reviews + 1
            item['_id'] = bson.objectid.ObjectId(new_id)
            items_modified.append(item)
            all_ids[new_id] = item['asin']
            #print item
        
        if 'price' not in item:
            without_prices = without_prices + 1
            item['price'] = round(random.uniform(0.5, 15.0),2)
        
        iter = iter + 1
        if iter%10000 == 0:
            print iter
            print item


print "Items without reviews "+without_reviews.__str__()
print "Items without prices "+without_prices.__str__()
print "Total items "+items_modified.__len__().__str__()
with codecs.open(os.path.join(dir, 'Digital_Music.json'), 'w', encoding="ISO-8859-1") as outfile:
    to_dump = json_util.dumps(items_modified)
    print "I have dumped to BSON successfully"
    outfile.write(to_dump)