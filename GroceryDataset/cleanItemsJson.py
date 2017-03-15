#-*- coding: utf-8 -*-

'''
Created on 7 mar. 2017

@author: Alberto
'''
import json
import codecs
import os

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

iter = 0
items=[]
d={}

with open(os.path.join(dir, 'Digital_Music.json')) as itemsfile:
    itemsfile = json.load(itemsfile)


    for item in itemsfile:
        if 'related' in item:
            del item['related']
        if 'salesRank' in item:
            del item['salesRank']
        cats=[]
        for l in item['categories']:
            for c in l:
                cats.append(c)
        item['categories']=list(set(cats))
        #l=item['categories']
        #del item['categories']
        #l=list(set([item for sublist in l for item in sublist]))
        #item['categories']=l
        if 'asin' in item['asin']:
            del item['asin']
        items.append(item)
        iter = iter+1
        if iter % 10000 == 0:
            print item
            print iter

with codecs.open(os.path.join(dir, 'clean_Digital_Music.json'), 'w', encoding="ISO-8859-1") as outfile:
    json.dump(items, outfile,  ensure_ascii=False) #para asegurar las tildes
    print "Done"


