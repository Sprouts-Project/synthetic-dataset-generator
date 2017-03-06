import re
import json
s = "{'asin': 'B0000CDBQT', 'related': {'also_bought': ['B0000CDBRA', 'B0000CDBRZ', 'B0000CDBRH', 'B0000CDBRQ', 'B0000CDBRV', 'B0000CDBPW', 'B0000CDBRM', 'B0000CDBRK', 'B0000CDBPT', 'B0000CDBPL', 'B0000CDBQL', 'B006307KDQ', 'B001EQ57DO', 'B0000CDBQB', 'B0000CDBQF', 'B0000CDBQN', 'B0078OD9FO', 'B0041FTPCY', 'B0000CDBQZ', 'B001EQ59CS', 'B006307GHG', 'B000CC60G4', 'B0041FPIWK', 'B000M1HQFY', 'B006307LQC', 'B0000CDBQO', 'B0082DNCHU', 'B000JUTCEQ', 'B0000CDBRS'], 'also_viewed': ['B0000CDBRV', 'B0000CDBRA', 'B0000CDBPL', 'B0000CDBRZ', 'B0000CDBRK', 'B0000CDBRQ', 'B0000CDBPT', 'B0000CDBRH', 'B0000CDBRM', 'B0000CDBQO', 'B0000CDBPW', 'B0000CDBQL', 'B0000CDBQF', 'B006307KDQ', 'B001EQ59CS', 'B0000CDBQB', 'B006307LQC', 'B0005YVU82', 'B0000CDBQN', 'B001EQ57DO', '0688028470', 'B0078OD9FO', 'B000M1HQFY', 'B001EPQQD0', 'B00KHACRP4', 'B00744ZBPO', 'B006307GHG', 'B006307HT8', 'B0000CDBPV', 'B0000CDBQG', 'B00258I5PM', 'B0041FTPCY', 'B0041FWDFK', 'B00838IOUY', 'B002W5SDEQ', 'B00AITWSZ8', 'B005KRON6A', 'B000MTTLZ4', 'B004W8LT10', 'B001EQ5A5E', 'B0000CDBQZ', 'B000YV7X1O', 'B0041FWE54', 'B0000CDBRT', 'B0000CDBPZ', 'B001EQ4YEC', 'B00FKBR1ZG'], 'bought_together': ['B0000CDBRA', 'B0000CDBRZ']}, 'title': \"Chef Paul Prudhomme's Magic Seasoning Blends ~ Meat Magic, 24-Ounce Canister\", 'price': 14.95, 'salesRank': {'Grocery & Gourmet Food': 19905}, 'imUrl': 'http://ecx.images-amazon.com/images/I/519AB5ZVFXL._SY300_.jpg', 'brand': 'Magic Seasoning Blends', 'categories': [['Grocery & Gourmet Food']], 'description': 'Chef Paul Prudhommes Magic Seasoning Blends has been in business since 1982 when customers from Chef Pauls New Orleans-based K-Pauls Louisiana Kitchen restaurant began asking to take home the chefs unique seasonings. What was once a garage-housed operation has grown to a 50,000 square-foot plant. Currently, Magic Seasoning Blends offers all-natural, MSG free products in sixteen different blends; Magic Pepper Sauce; seven ground, dried Magic Chiles; four Magic Sauce & Marinades; and several cookbook gift-packs.To use Magic Seasoning Blends in Chef Pauls recipes simply add up the amount of dry herbs and spices called for in the recipes \"Seasoning Mix\". Substitute the appropriate blend (for example, if you were doing a chicken dish, youd substitute Poultry Magic) in the proportioned amounts for each cookbook listed below:Substitute approximately  the amount for Chef Paul Prudhommes \"Seasoned America\" CookbookSubstitute approximately  the amount for Chef Paul Prudhommes \"Fork In The Road\" CookbookSubstitute approximately the same amount for Chef Paul Prudhommes \"Fiery Foods That I Love\", \"Louisiana Kitchen\", \"Kitchen Expedition\", and \"Louisiana Tastes\" cookbooksIf a recipe calls for a sweet spice or an unusual ingredient subtract the amount of sweet or unusual spice prior to adding up the dry herb seasoning mix, then add back the subtracted ingredient(s) to the Magic Seasoning Blends amount required for the conversion.'}"



def fixed_json(s):
    s = s.replace("'", '"').replace("\n", "")
    positions = []
    while(True):
        try:
            print s
            result = json.loads(s)   # try to parse...
            print result
            """
            if 'description' in result:
                result['description'] = result['description'].replace('"', "\'")
            if 'title' in result:
                result['title'] = result['description'].replace('"', "\'")
            """
            break
        except Exception as e:
            print e
            # "Expecting , delimiter: line 34 column 54 (char 1158)"
            # position of unexpected character after '"'
            unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
            #print unexp
            # position of unescaped '"' before that
            unesc = s.rfind(r'"', 0, unexp)
            pos = unesc
            if len(positions) > 0:
                if positions[-1] > pos:
                    #pos = s.find(r'"', positions[-1] + 2)
                    pos = unesc
                    positions.append(pos)
                else:
                    positions.append(pos)
            else:
                positions.append(pos)
            print pos
            if len(positions)>14 and pos==-1:
                break
            
            print positions
            print s[2606-5:2606+5]
            s = list(s)
            s[pos] = "'"
            s = "".join(s)
    return result
    
print fixed_json(s)

