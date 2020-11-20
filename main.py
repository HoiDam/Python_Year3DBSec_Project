import json
import os
import numpy as np
import random

# class web_app_ser:
#     def __init__(self,name="Web Application Server"):
#         self.activate=True
#         self.name=name
#         self.size="s"
        
#     def upgrade_size(self,size):
#         self.size=size

#     def deactivate(self):
#         self.activate=False

#     def print_detail(self):
#         print("\n~",self.name,"~")
#         print("Service : ", str(self.activate))
#         print("Size : ",self.size)

class database:
    def __init__(self,version,name="Database"):
        self.activate=True 
        self.name=name
        self.size="s"
        self.version=version
        self.tested_version=[]
        self.encryption="NA" 
        self.duty="all"       
            

    def add_test_ver(self,version):
        self.tested_version.append(version)

    def remove_test_ver(self,version):
        self.tested_version.pop(version)    
        
    def upgrade_size(self,size):
        self.size=size
    
    def patch(self,version):
        self.version=version

    def deactivate(self):
        self.activate=False
    
    def print_detail(self):
        print("\n~",self.name,"~")
        print("Service : ", str(self.activate))
        print("Size : ",self.size)
        print("Current Version : " ,self.version) 
        print("Tested Versions : " ,self.tested_version)
        print("Encryption : ",self.encryption)
        print("Duty : " ,self.duty)

def game_main(patch_mapping,risk_mapping):
    
    # print(patch_mapping)
    # print(risk_mapping)
    funds=1000 #initial funds
    round=1 #initial round
    total_round=30 #default total round
    current_risk_level=1 #risk level
    max_risk_level=len(risk_mapping) #max risk level
    found_risks=[]
    current_patch_level=1
    max_patch_level=len(patch_mapping) #max patch level
    ava_patches=[]
    end_game=False

    # waiting_task_array=[]

    options=[{"key":"e","notices":"Turn to go to next round."},{"key":"n","notices":"Show User Manual."}] #set options
    
    db=database("1")

    while round<=total_round and end_game==False: #whole game loop
        skip=False #cause new round no skip info
        

        while True: # round loop
            
            if skip==False:
                print("Rounds : ", round ,"/",total_round)
                print("Funds : ",funds)
                db.print_detail()
                print("\n~ General Information ~")
                found_risks=current_threat(current_risk_level,patch_mapping,int(db.version))
                print("Current found risks : ["+",".join(found_risks)+"]")
                ava_patches=current_ava_patches(current_patch_level,int(db.version))
                print("Current available versions : ["+",".join(ava_patches)+"]")
            skip=False    
                
            for i in range(len(options)):
                print("Enter \"{}\" to {}".format(options[i]["key"],options[i]["notices"]))   
            msg=str(input("Command :"))
            if msg=="e":
                break
            elif msg=="n":
                skip=show_userManual()
            elif msg=="1":
                skip=user_1_func(patch_mapping,current_patch_level)
            elif msg=="2":
                if db.size=="xl":
                    print("Current Size is the largest")
                    skip=True
                else:
                    while True:
                        wish_size=str(input("Which size you want to upgrade(Type exit to exit this choice) ?"))
                        
                        if wish_size=="m":
                            size_cost=1500
                        elif wish_size=="l":
                            size_cost=3000
                        elif wish_size=="xl":
                            size_cost=5000
                        elif wish_size=="exit":
                            break
                        else:
                            print("Invalid Input")
                            continue

                        if check_enough_fund(size_cost,funds)==True:
                            funds-=size_cost
                            db.size=wish_size #here
                            print("Upgrade success !")
                            break
            elif msg=="3":
                test_cost=1000
                while True:
                    wish_test=str(input("Which version you want to test(Type exit to exit this choice) ?"))
                    if wish_test in ava_patches:
                        if check_enough_fund(test_cost,funds)==True:
                            funds-=test_cost
                            db.tested_version.append(wish_test) #here
                            print("Tested success !")
                            break
                    elif wish_test=="exit":
                        break
                    else:
                        print("Invalid Input")
                        continue
            elif msg=="4":
                patch_cost=2000
                while True:
                    wish_patch=str(input("Which version you want to patch(Type exit to exit this choice) ?"))
                    if wish_patch in ava_patches:
                        if check_enough_fund(patch_cost,funds)==True:
                            funds-=patch_cost
                            if wish_patch in db.tested_version:
                                db.version=wish_patch #here
                            else:
                                
                                if randomize(50)==True:
                                    db.version=wish_patch #here
                                else:
                                    print("Upgrade fail") #here
                            break

                    elif wish_patch=="exit":
                        break
                    else:
                        print("Invalid Input")
                        continue

            else:
                skip=True
                print("Invalid Command. Please refer to user manual")


        if db.duty=="all":
            funds+=size_fund_func(db.size)
            funds+=round_fund_func(db.size,round,total_round)
        
        current_risk_level+=random.randint(1,2)
        if current_risk_level>max_risk_level:
            current_risk_level=max_risk_level

        current_patch_level+=random.randint(1,2)
        if current_patch_level>max_patch_level:
            current_patch_level=max_patch_level

        funds+=risk_round(found_risks,risk_mapping)

        round+=1


def show_userManual():
    options=[{"key":"1","notices":"Show which risks could be deal with your chosen version"},{"key":"2","notices":"Upgrade db"}]
    for i in range(len(options)):
        print("Enter \"{}\" to {}".format(options[i]["key"],options[i]["notices"]))
    return True

def randomize(percent):
    random_no=random.randint(1,100)
    if random_no<percent:
        return True
    else:
        return False

def risk_round(found_risks,rm):
    stacks=0
    for risk in found_risks:
        if randomize(10)==True:
            chosen=random.choice(rm[int(risk)-1]["events"])
            print("The event {} has triggered".format(chosen))
            print(str(stacks),"has been charged as punishment")
            stacks+=500
    return stacks


def current_threat(crl,pm,v): #show current risks
    version_risk_array=pm[v-1]["risk"]
    risk_array=[]
    for i in range(crl):
        risk_array.append(i+1)
    filtered_array = [str(item) for item in risk_array if item not in version_risk_array]   
    return filtered_array

def current_ava_patches(cpl,v):
    ava_patches=[]
    for i in range(cpl):
        if i>v:
            ava_patches.append(str(i))
    return ava_patches

def size_fund_func(size): #add fund for each round size
    if size=="s":
        return 250 
    elif size=="m":
        return 500 
    elif size=="l": #L 
        return 1000 
    elif size=="xl":
        return 2000 

def round_fund_func(size,round,total_round): #minus fund for each round size
    punishment_ratio=250
    if size=="s":
        size_value=1
    elif size=="m":
        size_value=2
    elif size=="l": #L 
        size_value=3
    elif size=="xl":
        size_value=4
    round_ratio=float(round/total_round)
    if round_ratio<0.25:
        size_value-=1
    elif round_ratio<0.5:
        size_value-=2
    elif round_ratio<0.75:
        size_value-=3
    elif round_ratio<=1:
        size_value-=4
    
    if size_value<0:
        return punishment_ratio*size_value
    else: return 0   

def check_enough_fund(cost,funds):
    if funds<cost:
        print("Not enough funds")
        return False
    else: return True

# def load_task_template(function,live_time):

def user_1_func(pm,available_query_max): #show patch risk mapping NOT TASK
    
    while True:
        msg=int(input("Which version you want to query ?"))
        if msg >=1 and msg<=int(available_query_max):
            break
        else:
            print("Invalid Input (You could not query the unexisting version)")
    print(pm[msg-1])
    return True

# def user_2_func(): # YES TASK
    # return 0

# def user_3_func(): # YES TASK
    # return 0



def game_end():
    
    print("Ended")




while True:
    print("Database Game\nEnter \" 1 \" Start\nEnter \" 2 \" Exit")
    msg=int(input())
    if msg==1:
        os.system('cls')
        with open('patch_mapping.json') as jf1:
            patch_mapping=json.load(jf1)
        with open('risk_mapping.json') as jf2:
            risk_mapping=json.load(jf2)
        game_main(patch_mapping,risk_mapping)
        game_end()
    elif msg==2:
        break
    


