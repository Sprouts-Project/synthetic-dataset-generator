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
from random import randint
import datetime
from bson import json_util

dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def probability(percent):
    r = random.random()
    if r <= percent:
        return True
    else:
        return False

def generate_credit_card():
    return {"number": fake.credit_card_number(),
           "cvv": fake.credit_card_security_code(),
           "expire": fake.credit_card_expire(start="now", end="+10y", date_format="%m/%y"),
           "brand": fake.credit_card_provider(card_type=None)}

def select_quantity(price):
    if price<=1.0:
        return randint(1,30)
    if price>1.0 and price<=5.0:
        return randint(1,15)
    if price>5.0 and price <=10.0:
        return randint(1,5)
    else:
        return randint(1,2)

def calculate_total_price(ordered_items):
    total_price = 0.0
    for item in ordered_items:
        total_price = total_price + (item['quantity'] * item['price'])
    return round(total_price,2)

def buy_items_with_probability(percent, ordered_items, to_buy, all_items):
    for i_asin in to_buy:
        #print i_asin
        if i_asin in all_items:
            if probability(percent):
                ordered_items.append({
                        "item": json_util.DBRef("items", bson.objectid.ObjectId(str(all_items[i_asin]['_id']))),#'DBRef("items", ObjectId("'+all_items[i_asin]['_id']+'") )',
                        "price": all_items[i_asin]['price'],
                        "quantity": select_quantity(all_items[i_asin]['price'])
                    })

def create_orders_with_probability(percent, item_percent, orders, to_buy, all_items, review, credit_card):
    for i_asin in to_buy:
        if i_asin in all_items:
            if probability(percent):
                ordered_items = []
                ordered_items.append({"item": json_util.DBRef("items", bson.objectid.ObjectId(str(all_items[i_asin]['_id']))),#'DBRef("items", ObjectId("'+all_items[i_asin]['_id']+'") )',
                                      "price": all_items[i_asin]['price'],
                                      "quantity": select_quantity(all_items[i_asin]['price'])
                                    })
                
                buy_items_with_probability(item_percent, ordered_items, to_buy, all_items)
                orders.append(create_order(review, ordered_items, all_items, credit_card, is_review_order=False))
    
def create_order(review, ordered_items, all_items, credit_card, is_review_order=True):
    
    if is_review_order:
        #The order will be ordered between 1 and 10 days after the review was written
        date = fake.date_time_between(start_date=datetime.datetime.fromtimestamp(int(review['unixReviewTime']) + 24*60*60), 
                                      end_date=datetime.datetime.fromtimestamp(int(review['unixReviewTime']) + 10*24*60*60), tzinfo=tz.tzutc())
    else:
        #The order will be ordered between -60 and 60 days after the review was written
        date = fake.date_time_between(start_date=datetime.datetime.fromtimestamp(int(review['unixReviewTime']) - 60*24*60*60), 
                                      end_date=datetime.datetime.fromtimestamp(int(review['unixReviewTime']) + 60*24*60*60), tzinfo=tz.tzutc())
        
    #The order will be delivered between 1 and 10 days after it was ordered
    delivered_date = fake.date_time_between(start_date=(date + datetime.timedelta(days=1)), 
                                  end_date=(date + datetime.timedelta(days=10)), tzinfo=tz.tzutc())
    
    return {
            "_id": bson.objectid.ObjectId(str(bson.ObjectId())),
            "customer": bson.DBRef("customers", bson.objectid.ObjectId(review['customer'].id)),
            "ordered_items": ordered_items,
            "credit_card": credit_card,
            "date": date,
            "delivered_date":delivered_date,
            "total_price": calculate_total_price(ordered_items),
            "address": fake.address().replace("\n"," ")
        }

items = {} # {"asin": , "item":{cuerpo del item}}
with open(os.path.join(dir, 'Digital_Music.json')) as itemfiles:
    itemsinfile = itemfiles.read()
    itemsinfile = json_util.loads(itemsinfile)
    for item in itemsinfile:
        items[item['asin']] = item 

print("I finished the items dictionary!")

fake = Factory.create('en_US')

orders = []
iter = 0
with open(os.path.join(dir, 'reviews.json')) as reviewsfile:
    
    reviews = reviewsfile.read()
    reviews = json_util.loads(reviews)
    customer_credit_cards = {} #{"customer": ["creditcard", "creditcard"]}
    
    for review in reviews:
        customer_id = review['customer']
        if customer_id not in customer_credit_cards or probability(0.02):
            credit_card = generate_credit_card()
            if customer_id not in customer_credit_cards:
                customer_credit_cards[customer_id] = [credit_card]
            else:
                customer_credit_cards[customer_id].append(credit_card)
        else:
            credit_card = random.sample(customer_credit_cards[customer_id], 1)[0]
        also_bought = []
        bought_together = []
        also_viewed = []
        #print item
        item = items[review['asin']]
        #print review['asin']
        if 'related' in item:
            if 'also_bought' in item['related']:
                #print "hola"
                also_bought = item['related']['also_bought']
                
            if 'also_viewed' in item['related']:
                also_viewed = item['related']['also_viewed']
            
            if 'bought_together' in item['related']: 
                bought_together = item['related']['bought_together']
        #print item
        ordered_items = []
        ordered_items.append({"item": review['item'], #item ref
                              "price": item['price'],
                              "quantity": select_quantity(item['price'])})
        
        buy_items_with_probability(0.85, ordered_items, bought_together, items)
        buy_items_with_probability(0.05, ordered_items, also_bought, items)
        buy_items_with_probability(0.01, ordered_items, also_viewed, items)
        
        #print bought_together

        
        orders.append(create_order(review, ordered_items, items, credit_card))
        
        #create several orders with 5% probability per also_bought item. each item will be added with 0.9% probability
        create_orders_with_probability(0.05, 0.009, orders, also_bought, items, review, credit_card)
        #create several orders with 0.5% probability per also_bought item. each item will be added with 0.3% probability
        create_orders_with_probability(0.005, 0.003, orders, also_viewed, items, review, credit_card)
        
        iter = iter + 1
        #print iter
        if iter%1000 == 0:
            print iter
            print orders[-1]
            print "created orders: " + len(orders).__str__()
        
print "Total orders created: " + len(orders).__str__()
with codecs.open(os.path.join(dir, 'orders_completed.json'), 'w', encoding="ISO-8859-1") as outfile:
    to_dump = json_util.dumps(orders)
    print "I have dumped to BSON successfully"
    outfile.write(to_dump)
