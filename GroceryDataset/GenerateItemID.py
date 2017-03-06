'''
Created on 12 feb. 2017

@author: Alvaro
'''

import json
import os
import bson
from faker import Factory
import codecs
from dateutil import tz
import random

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

fake = Factory.create('en_US')

reviews_modified = []

iter = 0

with open(os.path.join(dir, '../inputs/reviews_customers_ids.json')) as reviewsfile:
    
    reviews = json.load(reviewsfile)
    asins = {}
    
    for review in reviews:
        asin = review['asin']
        
        #if it has not been processed yet, generate objectid and add to asins
        if asin not in asins:
            objectid = str(bson.ObjectId())
            
            review['item'] = 'DBRef("items", ObjectId("'+objectid+'"))'
            asins[asin] = 'DBRef("items", ObjectId("'+objectid+'"))'
        #else, assign existing id
        else:
            review['item']= asins[asin]
        
        reviews_modified.append(review)
        
        iter = iter + 1
        if iter%1000 == 0:
            print iter
            print review
            
with codecs.open(os.path.join(dir, '../outputs/reviews.json'), 'w', encoding="ISO-8859-1") as outfile:
    json.dump(reviews_modified, outfile,  ensure_ascii=False) #para asegurar las tildes