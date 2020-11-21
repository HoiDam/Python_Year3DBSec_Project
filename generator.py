import random
import json
import math

max_patch_no=10

max_event_no=70
max_events_in_risk=5

pr_loc="patch_mapping.json"
pr_mapping_array=[]
max_addict=3
last_digit=1
for i in range(max_patch_no):
    singleset={}
    generated_risks=[]
   
    randomize_value=random.randint(int(max_addict/2),max_addict)
    for j in range(1,last_digit+randomize_value):
        generated_risks.append(j)
    
    last_digit+=randomize_value
    
    singleset["patch"]=i+1
    singleset["risk"]=generated_risks
    pr_mapping_array.append(singleset)

max_risk_no=last_digit-1

rm_loc="risk_mapping.json"
mapping_array=[]

for i in range(max_risk_no):
    singleset={}
    generated_events=[]
    for j in range(random.randint(1,max_events_in_risk)):
        generated_events.append(random.randint(1,max_event_no))
    singleset["risk"]=i+1
    singleset["events"]=generated_events
    mapping_array.append(singleset)

with open(pr_loc, 'w') as f:
    json.dump(pr_mapping_array, f,indent=4)

with open(rm_loc, 'w') as f:
    json.dump(mapping_array, f,indent=4)

