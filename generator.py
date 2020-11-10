import random
import json

max_patch_no=10
max_risk_no=30
max_event_no=70
max_events_in_risk=5

pr_loc="patch_mapping.json"
pr_mapping_array=[]
max_addict=int(max_risk_no/max_patch_no)
last_digit=1
for i in range(max_patch_no):
    singleset={}
    generated_risks=[]
    randomize_value=random.randint(1,max_addict)
    for j in range(last_digit,last_digit+randomize_value):
        generated_risks.append(j)
    
    last_digit+=randomize_value
    if i==int(max_patch_no-1):
        for k in range(last_digit,max_risk_no+1):
            generated_risks.append(k)
    singleset["patch"]=i+1
    singleset["risk"]=generated_risks
    pr_mapping_array.append(singleset)

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