#-*- coding: utf-8 -*-

'''
Created on 13 feb. 2017

@author: Alvaro
'''
import json
import re
import os
import codecs
dir = os.path.dirname(__file__) #<-- absolute dir the script is in

d=set()
with open(os.path.join(dir, 'asins.json')) as asinsfile:
    for asi in asinsfile:
        asi2= json.loads(asi)
        d.add(asi2['asin'])
    print d


# http://stackoverflow.com/questions/18514910/how-do-i-automatically-fix-an-invalid-json-string
def fixed_json(s):
    s = s.replace("\n", "").replace('"', "'").replace("\t", " ")
    s = re.sub(r"\n", " ", s)
    #Find position for each attribute
    keys = [("asin",s.find("'asin'")),( "related",s.find("'related'")), ("title",s.find("'title'")), ("price",s.find("'price'")), ("salesRank",s.find("'salesRank'")), ("imUrl",s.find("'imUrl'")), ("brand",s.find("'brand'")), ("categories",s.find("'categories'")), ("description",s.find("'description'"))]
    #Get the keys available in the document
    keys = [x for x in keys if x[1] > 0]
    #Sort by char position
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
                """
                while ls[end] != "'":
                    end = end -1
                    if ls[end] == '"':
                        break
                """
            else:
                end = len(ls) - 2
            ls[start] = '"'
            ls[end] = '"'
            """
            for m in re.finditer('"', s[start+1:end-1]):
                ls[start + m.start() +1 ] = "'"
            """
    s = "".join(ls)
    s = s.decode('string_escape').decode("ISO-8859-1").replace('Children"s',"Children's").replace('Today"s',"Today's").replace('Baker"s', "Baker's").replace('\\', "-").replace("\t","")
    s = re.sub(r"\n", " ", s)
    #print s[986-20: 986+20]
    #print s
    return json.loads(s)
    


iter = 0
items = []
with open(os.path.join(dir, 'meta_Digital_Music.json')) as itemsfile:
    
    for line in itemsfile:
        #print line
        item=fixed_json(line)
        if item['asin'] in d:
            items.append(item)
            iter = iter + 1



with codecs.open(os.path.join(dir, 'meta_Digital_Music_fixed.json'), 'w', encoding="ISO-8859-1") as outfile:
    json.dump(items, outfile,  ensure_ascii=False) #para asegurar las tildes
