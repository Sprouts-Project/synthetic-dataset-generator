#-*- coding: utf-8 -*-

'''
Created on 8 mar. 2017

@author: Alberto
'''
import json
import codecs
import os

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

iter = 0
items=[]

with open(os.path.join(dir, 'reviews.json')) as reviewsfile:
    reviewsfile = json.load(reviewsfile)
    for review in reviewsfile:
        if 'unixReviewTime' in review:
            del review['unixReviewTime']
        if 'reviewTime' in review:
            del review['reviewTime']
        if 'reviewerName' in review:
            del review['reviewerName']
        if 'asin' in review:
            del review['asin']
        if 'reviewerID' in review:
            del review['reviewerID']
        if 'helpful' in review:
            h=review['helpful']
            review['helpful']=h[0]
            review['unhelpful']=h[1]-h[0]
        else:
            review['helpful'] = 0
            review['unhelpful'] = 0
        items.append(review)
        print review
        iter = iter+1
        if iter % 10000 == 0:
            print review
            print iter

with codecs.open(os.path.join(dir, 'clean_reviews.json'), 'w', encoding="ISO-8859-1") as outfile:
    json.dump(items, outfile,  ensure_ascii=False) #para asegurar las tildes
    print "Done"


