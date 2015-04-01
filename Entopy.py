"""I just read about entropy. Entropy shows how useful a certain attribute is for classification. Entropy is the average amount of information contained in each item received. The less likely an event occurs the more information it provides. Entropy's formula is simply, -p1(log(p1)) - p2(log(p2)) - ... where the log is base 2. Max entropy is found when the data is most impure, or when there are equal number of different outputs.
Ex. Looking to see if an item is a + or -, entropy is max when there are equal +'s and -'s. On the flip side, entropy is minimized when the data contains only one result, all +'s.

The data set I am using to test entropy was found at: 
https://archive.ics.uci.edu/ml/datasets/Mushroom

There are 22 attributes:
1. cap-shape: bell=b,conical=c,convex=x,flat=f, knobbed=k,sunken=s 
2. cap-surface: fibrous=f,grooves=g,scaly=y,smooth=s 
3. cap-color: brown=n,buff=b,cinnamon=c,gray=g,green=r, pink=p,purple=u,red=e,white=w,yellow=y 
4. bruises?: bruises=t,no=f 
5. odor: almond=a,anise=l,creosote=c,fishy=y,foul=f, musty=m,none=n,pungent=p,spicy=s 
6. gill-attachment: attached=a,descending=d,free=f,notched=n 
7. gill-spacing: close=c,crowded=w,distant=d 
8. gill-size: broad=b,narrow=n 
9. gill-color: black=k,brown=n,buff=b,chocolate=h,gray=g, green=r,orange=o,pink=p,purple=u,red=e, white=w,yellow=y 
10. stalk-shape: enlarging=e,tapering=t 
11. stalk-root: bulbous=b,club=c,cup=u,equal=e, rhizomorphs=z,rooted=r,missing=? 
12. stalk-surface-above-ring: fibrous=f,scaly=y,silky=k,smooth=s 
13. stalk-surface-below-ring: fibrous=f,scaly=y,silky=k,smooth=s 
14. stalk-color-above-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y 
15. stalk-color-below-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y 
16. veil-type: partial=p,universal=u 
17. veil-color: brown=n,orange=o,white=w,yellow=y 
18. ring-number: none=n,one=o,two=t 
19. ring-type: cobwebby=c,evanescent=e,flaring=f,large=l, none=n,pendant=p,sheathing=s,zone=z 
20. spore-print-color: black=k,brown=n,buff=b,chocolate=h,green=r, orange=o,purple=u,white=w,yellow=y 
21. population: abundant=a,clustered=c,numerous=n, scattered=s,several=v,solitary=y 
22. habitat: grasses=g,leaves=l,meadows=m,paths=p, urban=u,waste=w,woods=d

Missing Attribute Values: 2480 of them (denoted by "?"), all for
attribute #11.

Class Distribution: 
    --    edible: 4208 (51.8%)
    -- poisonous: 3916 (48.2%)
    --     total: 8124 instances"""

import pandas as pd
import numpy as np

shrooms = pd.read_csv("mushrooms.csv")

"""Create a function for calculating entropy
Params: p = count of positives
        q = count of negatives
returns: entropy in the form of a float
"""
def calc_entropy(p,q):
    total = float(p + q)
    pos = p/total
    neg = q/total
    entr = -((pos*np.log2(pos))+((neg*np.log2(neg))))
    return entr
"""
Although I am given the total number of poisonous and edible mushrooms, I am going to search through the table to check to see
if I can get the same number.
"""

edible = 0
edible_rows = shrooms[shrooms.Poisonous == "e"]
for each in edible_rows.to_records():
    edible += 1
print edible

poisonous = 0
poison_rows = shrooms[shrooms.Poisonous == "p"]
for each in poison_rows.to_records():
    poisonous += 1
print poisonous

#Excellent I got the same numbers for both poisonous and edible.

#Next task will be to identify the parent entropy. Aka the entropy for the entire data set. This is straightforward since I made the function to calculate entropy if you have positive and negative counts. In this case we will say that positive is edible. that's a better situation than eating a poisonous mushroom.

parent_entropy = calc_entropy(edible,poisonous)
print parent_entropy

"""That number is pretty damn close to 1 meaning the entropy is high in this data set. This is expected because the mushrooms are almost split 50/50 between poisonous and edible.

Now that I have the parent entropy I can calculate the information gained from each attribute in the data set. The formula for this is also quite simple:

IG(parent,attribute) = entropy(parent) - (p(a1)*entropy(a1) + p(a2)*entropy(a2) + ...) 

A high IG is good. A high IG means that using this attribute to seperate the data lowers the entropy in each cohort. If you look at the formula, it takes the parent entropy and subtracts the weighted entropy of each cohort. Meaning if the cohort entropy is small, there will not be much to take away from the parent entropy.

Before I go into the next part I am going to remove spaces from the column headers.
"""

cols = shrooms.columns
cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str, unicode)) else x)
shrooms.columns = cols

#cap-shape: bell=b,conical=c,convex=x,flat=f, knobbed=k,sunken=s 
#First calculate the entropy for all children

def calc_IG(df):
    #Get column names
    cols = df.columns
    #Iterate through all except for the poisonous column
    for each in cols[1:]:
        unique_attr = df[each].unique()    #Extracts all unique values in the column
        count = 0
        for temp in unique_attr:
            print each+" "+temp
            total = df[df[each] == temp].shape[0]
            neg = df[(df[each] == temp) & (df.Poisonous == 'p')].shape[0]
            pos = df[(df[each] == temp) & (df.Poisonous == 'e')].shape[0]
            ent = calc_entropy(pos,neg)
            print "Entropy for "+each+" "+temp+": "+str(ent)
calc_IG(shrooms)
