'''
Created on 13 feb. 2017

@author: Alvaro
'''
import re
import json
s = "{'asin': 'B0000CDBQT', 'related': {'also_bought': ['B0000CDBRA', 'B0000CDBRZ', 'B0000CDBRH', 'B0000CDBRQ', 'B0000CDBRV', 'B0000CDBPW', 'B0000CDBRM', 'B0000CDBRK', 'B0000CDBPT', 'B0000CDBPL', 'B0000CDBQL', 'B006307KDQ', 'B001EQ57DO', 'B0000CDBQB', 'B0000CDBQF', 'B0000CDBQN', 'B0078OD9FO', 'B0041FTPCY', 'B0000CDBQZ', 'B001EQ59CS', 'B006307GHG', 'B000CC60G4', 'B0041FPIWK', 'B000M1HQFY', 'B006307LQC', 'B0000CDBQO', 'B0082DNCHU', 'B000JUTCEQ', 'B0000CDBRS'], 'also_viewed': ['B0000CDBRV', 'B0000CDBRA', 'B0000CDBPL', 'B0000CDBRZ', 'B0000CDBRK', 'B0000CDBRQ', 'B0000CDBPT', 'B0000CDBRH', 'B0000CDBRM', 'B0000CDBQO', 'B0000CDBPW', 'B0000CDBQL', 'B0000CDBQF', 'B006307KDQ', 'B001EQ59CS', 'B0000CDBQB', 'B006307LQC', 'B0005YVU82', 'B0000CDBQN', 'B001EQ57DO', '0688028470', 'B0078OD9FO', 'B000M1HQFY', 'B001EPQQD0', 'B00KHACRP4', 'B00744ZBPO', 'B006307GHG', 'B006307HT8', 'B0000CDBPV', 'B0000CDBQG', 'B00258I5PM', 'B0041FTPCY', 'B0041FWDFK', 'B00838IOUY', 'B002W5SDEQ', 'B00AITWSZ8', 'B005KRON6A', 'B000MTTLZ4', 'B004W8LT10', 'B001EQ5A5E', 'B0000CDBQZ', 'B000YV7X1O', 'B0041FWE54', 'B0000CDBRT', 'B0000CDBPZ', 'B001EQ4YEC', 'B00FKBR1ZG'], 'bought_together': ['B0000CDBRA', 'B0000CDBRZ']}, 'title': \"Chef Paul Prudhomme's Magic Seasoning Blends ~ Meat Magic, 24-Ounce Canister\", 'price': 14.95, 'salesRank': {'Grocery & Gourmet Food': 19905}, 'imUrl': 'http://ecx.images-amazon.com/images/I/519AB5ZVFXL._SY300_.jpg', 'brand': 'Magic Seasoning Blends', 'categories': [['Grocery & Gourmet Food']], 'description': 'Chef Paul Prudhommes Magic Seasoning Blends has been in business since 1982 when customers from Chef Pauls New Orleans-based K-Pauls Louisiana Kitchen restaurant began asking to take home the chefs unique seasonings. What was once a garage-housed operation has grown to a 50,000 square-foot plant. Currently, Magic Seasoning Blends offers all-natural, MSG free products in sixteen different blends; Magic Pepper Sauce; seven ground, dried Magic Chiles; four Magic Sauce & Marinades; and several cookbook gift-packs.To use Magic Seasoning Blends in Chef Pauls recipes simply add up the amount of dry herbs and spices called for in the recipes \"Seasoning Mix\". Substitute the appropriate blend (for example, if you were doing a chicken dish, youd substitute Poultry Magic) in the proportioned amounts for each cookbook listed below:Substitute approximately  the amount for Chef Paul Prudhommes \"Seasoned America\" CookbookSubstitute approximately  the amount for Chef Paul Prudhommes \"Fork In The Road\" CookbookSubstitute approximately the same amount for Chef Paul Prudhommes \"Fiery Foods That I Love\", \"Louisiana Kitchen\", \"Kitchen Expedition\", and \"Louisiana Tastes\" cookbooksIf a recipe calls for a sweet spice or an unusual ingredient subtract the amount of sweet or unusual spice prior to adding up the dry herb seasoning mix, then add back the subtracted ingredient(s) to the Magic Seasoning Blends amount required for the conversion.'}"
s2 = "{'asin': '0657745316', 'description': 'This is real vanilla extract made with only 3 premium ingredients. GMO free, no fillers you find in store bought \"vanilla extract.\" \n\nThe taste will knock your socks off. Everyone will notice a difference in your baking and cooking and they\'ll want to know your secret. I also use this for a special homemade coffee creamer that\'s out of this world and I use it for tea and black coffee as well as espresso drinks. You can add this to make a vanilla latte and skip the sugary syrup for a healthier latte with more flavor! \n\nWhen this item arrives, there will also be instructions to refill the product as its used so that you won\'t have to age it or repurchase it. I\'ve been using the same vanilla for 2 years now and have friends who\'ve had theirs for 5 years. It\'s just as tasteful, just as sweet, strong, and yummy. \n\nI use only top shelf liquor and the product is aged a minimum of 4 months. \n\nThese also make great gifts. I currently have plenty on the shelf but they won\'t be ready to use until February (just in time to bake your honey some sweets). Contact me for details. I also make designer jars, and can add any decorative details such as ribbon upon request. Please note, custom orders will require longer shipping and prices will vary depending on how detailed you\'d like the jar or ribbons etc. \n\nMost of these will come in a small mason jar which contains approx 12-16 ounces of extract. The beans are right in the jar and I always throw in extra beans so your product will stay much longer for use in refilling. This product gets sweeter with time.. Like a fine wine it gets better with age.. So the longer you have it on the shelf the better it continues to get.', 'title': '100 Percent All Natural Vanilla Extract', 'imUrl': 'http://ecx.images-amazon.com/images/I/41gFi5h0jYL._SY300_.jpg', 'related': {'also_viewed': ['B001GE8N4Y']}, 'salesRank': {'Grocery & Gourmet Food': 374004}, 'categories': [['Grocery & Gourmet Food']]}"
s3 = "{'asin': '0657745316', 'description': 'This is real vanilla extract made with only 3 premium ingredients. GMO free, no fillers you find in store bought \"vanilla extract.\" \n\nThe taste will knock your socks off. Everyone will notice a difference in your baking and cooking and they\'ll want to know your secret. I also use this for a special homemade coffee creamer that\'s out of this world and I use it for tea and black coffee as well as espresso drinks. You can add this to make a vanilla latte and skip the sugary syrup for a healthier latte with more flavor! \n\nWhen this item arrives, there will also be instructions to refill the product as its used so that you won\'t have to age it or repurchase it. I\'ve been using the same vanilla for 2 years now and have friends who\'ve had theirs for 5 years. It\'s just as tasteful, just as sweet, strong, and yummy. \n\nI use only top shelf liquor and the product is aged a minimum of 4 months. \n\nThese also make great gifts. I currently have plenty on the shelf but they won\'t be ready to use until February (just in time to bake your honey some sweets). Contact me for details. I also make designer jars, and can add any decorative details such as ribbon upon request. Please note, custom orders will require longer shipping and prices will vary depending on how detailed you\'d like the jar or ribbons etc. \n\nMost of these will come in a small mason jar which contains approx 12-16 ounces of extract. The beans are right in the jar and I always throw in extra beans so your product will stay much longer for use in refilling. This product gets sweeter with time.. Like a fine wine it gets better with age.. So the longer you have it on the shelf the better it continues to get.', 'title': '100 Percent All Natural Vanilla Extract', 'imUrl': 'http://ecx.images-amazon.com/images/I/41gFi5h0jYL._SY300_.jpg', 'related': {'also_viewed': ['B001GE8N4Y']}, 'salesRank': {'Grocery & Gourmet Food': 374004}, 'categories': [['Grocery & Gourmet Food']]}"
s=s3

s = s.replace("\n", "")
keys = [("asin",s.find("'asin'")),( "related",s.find("'related'")), ("title",s.find("'title'")), ("price",s.find("'price'")), ("salesRank",s.find("'salesRank'")), ("imUrl",s.find("'imUrl'")), ("brand",s.find("'brand'")), ("categories",s.find("'categories'")), ("description",s.find("'description'"))]
keys = [x for x in keys if x[1] > 0]
keys = sorted(keys, key=lambda x: x[1])

ls = list(s)

for i in range(len(keys)):
    
    key = keys[i]
    ls[key[1]] = '"'
    ls[key[1] + len(key[0]) +1 ]='"'
    
    if key[0] != 'title' and key[0] != 'description':
        start = key[1]+len(key[0]) + 1
        if i != (len(keys) - 1):
            next_key = keys[i+1]
            end = next_key[1] -2
        else:
            end = len(ls) - 1
        for m in re.finditer("'", s[start:end]):
            ls[start + m.start()] = ls[start + m.start()].replace("'", '"')
    else:
        start = key[1]+len(key[0])+4        
        if i != (len(keys) - 1):
            next_key = keys[i+1]
            end = next_key[1] - 3
            while ls[end] != "'":
                end = end -1
                if ls[end] == '"':
                    break
        else:
            end = len(ls) - 2
        ls[start] = '"'
        ls[end] = '"'
        
        for m in re.finditer('"', s[start+1:end-1]):
            ls[start + m.start() +1 ] = ls[start + m.start() + 1].replace('"', "\'")
s = "".join(ls)
print json.loads(s)
