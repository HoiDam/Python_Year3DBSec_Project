import json
import os
class web_app_ser:
    def __init__(self,name="Web Application Server"):
        self.activate=True
        self.name=name
        self.size="s"
        
    def upgrade_size(self,size):
        self.size=size

    def deactivate(self):
        self.activate=False

    def print_detail(self):
        print("\n~",self.name,"~")
        print("Service : ", str(self.activate))
        print("Size : ",self.size)

class database:
    def __init__(self,name="Database"):
        self.activate=True 
        self.name=name
        self.size="s"
        self.version="12c"
        self.available_version=[] 
        self.tested_version=[]
        self.risk=[]
        self.encryption="NA" 
        self.duty="all"       
            
    def add_ava_ver(self,version):
        self.available_version.append(version)

    def add_test_ver(self,version):
        self.tested_version.append(version)

    def add_risk(self,risk):
        self.risk.append(risk)

    def remove_ava_ver(self,version):
        self.available_version.pop(version)    

    def remove_test_ver(self,version):
        self.tested_version.pop(version)    

    def remove_risk(self,risk):
        self.risk.pop(risk)       
        
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
        print("Available Versions : " ,self.available_version)
        print("Tested Versions : " ,self.tested_version)
        print("Risks : " ,self.risk)
        print("Encryption : ",self.encryption)
        print("Duty : " ,self.duty)

def game_main(patch_mapping,risk_mapping):
    
    # print(patch_mapping)
    # print(risk_mapping)
    funds=1000
    round=1
    total_round=30 #default total round
    was=web_app_ser()
    db=database()

    while round<=total_round:
        while True:
            print("Rounds : ", round ,"/",total_round)
            print("Funds : ",funds)
            was.print_detail()
            db.print_detail()
            print("Enter \"End\" Turn to go to next round.")
            msg=str(input())
            if msg=="End":
                break
        


        funds+=size_fund_func(db.size)
        funds+=round_fund_func(db.size,round,total_round)
        round+=1
        os.system('cls')

def size_fund_func(size):
    if size=="s":
        return 250 
    elif size=="m":
        return 500 
    elif size=="l": #L 
        return 1000 
    elif size=="xl":
        return 2000 

def round_fund_func(size,round,total_round):
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


def game_end():
    
    print("Ended")













while True:
    print("Database Game\nEnter \" 1 \" Start\nEnter \" 2 \" Exit")
    msg=int(input())
    if msg==1:
        with open('patch_mapping.json') as jf1:
            patch_mapping=json.load(jf1)
        with open('risk_mapping.json') as jf2:
            risk_mapping=json.load(jf2)
        game_main(patch_mapping,risk_mapping)
        game_end()
    elif msg==2:
        break
    


