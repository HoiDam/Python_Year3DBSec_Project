import json
import os
import numpy as np
import random

class database:
    def __init__(self,show,version,duty,name="Database",size="s",encryption="N/A"):
        self.show=show
        self.activate="Working"
        self.name=name
        self.size=size
        self.version=version
        self.encryption=encryption 
        self.duty=duty      
            
    def print_detail(self):
        print("\n~",self.name,"~")
        print("Service : ", str(self.activate))
        print("Size : ",self.size)
        print("Current Version : " ,self.version) 
        print("Encryption : ",self.encryption)
        print("Duty : " ,self.duty)

def game_main(patch_mapping,risk_mapping):
    
    # print(patch_mapping)
    # print(risk_mapping)
    funds=10000 #initial funds
    round=1 #initial round
    total_round=30 #default total round
    current_risk_level=1 #risk level
    max_risk_level=len(risk_mapping) #max risk level
    found_risks=[]
    current_patch_level=1
    max_patch_level=len(patch_mapping) #max patch level
    ava_patches=[]
    tested_version=[]
    end_game=False

    waiting_task_array=[]

    options=[{"key":"e","notices":"Turn to go to next round."},{"key":"n","notices":"Show User Manual."}] #set options
    task_alert="Task {} has been scheduled . {} rounds after will be done" #task template 
    
    db_array=[]
    db=database(True,"1",["UserPII","OrderDetails","PartnerInfo"] )
    db_array.append(db)

    while round<=total_round: #whole game loop

        skip=False #cause new round no skip info
        if end_game==True or funds<0: #instant die
            return {"win":False,"rounds":round}

        print("\n-------\nRounds : ", round ,"/",total_round) #show current round
        print("~ Your schedualed tasks ~")
        for task in waiting_task_array: ###do schedualed task
            task["livetime"]-=1
            if task["livetime"]==0:
                if task["function"]==2:
                    db_array[task["db"]-1].size=task["parameter"] 
                    print("Task : database {} upgraded to {} size !".format(task["db"],task["parameter"]))
                if task["function"]==3:
                    tested_version.append(task["parameter"])
                    print("Task : version {} tested success !".format(task["parameter"]))
                if task["function"]==4:
                    if task["parameter"] in tested_version:
                        for db in db_array:
                            db.version=task["parameter"]
                        print("Task : version {} patched success !".format(task["parameter"]))
                    else:
                        if randomize(50)==True:
                            for db in db_array:
                                db.version=task["parameter"]
                            print("Task : version {} patched success !".format(task["parameter"]))
                        else:
                            print("Task : version {} patched FAILED !".format(task["parameter"]))
                if task["function"]==5:
                    db_array[0].duty.remove(task["parameter"])
                    db_array[0].name="Database 1"
                    db_array.append(database(True,db_array[0].version,[task["parameter"]],name="Database "+str(len(db_array)+1)))
                    print("Task : main database splited with seperate {} database !".format(task["parameter"]))
                waiting_task_array.remove(task)
            else:
                print("Task : {} {} has {} rounds remaining".format(task["func_name"],task["parameter"],task["livetime"]))
        print("~          ~            ~")
                

        while True: # round loop
            
            if skip==False:
                print("Funds : ",funds)
                for db in db_array:
                    if db.show==True:
                        db.print_detail()
                print("\n~ General Information ~")
                found_risks=current_threat(current_risk_level,patch_mapping,int(db_array[0].version))
                print("Current found risks : ["+",".join(found_risks)+"]")
                ava_patches=current_ava_patches(current_patch_level,int(db_array[0].version))
                print("Current available versions : ["+",".join(ava_patches)+"]")
                print("Current tested versions : ["+",".join(tested_version)+"]" )
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
                while True:
                    wish_db=int(input("Which db you want to upgrade(Type 0 to exit this choice)?"))
                    if wish_db=="0":
                        break
                    elif wish_db>len(db_array) or int(wish_db)<=0:
                        print("Invalid Input")
                        continue
                    if db_array[int(wish_db)-1].size=="xl":
                        print("Current Size is the largest")
                        continue
                   
                    wish_size=str(input("Which size you want to upgrade(Type 0 to exit this choice)?"))
                    if wish_size=="m":
                        size_cost=1500
                        
                    elif wish_size=="l":
                        size_cost=3000
                        
                    elif wish_size=="xl":
                        size_cost=5000
                        
                    elif wish_size=="0":
                        break
                    else:
                        print("Invalid Input")
                        continue
                    if check_dup_task(int(msg),wish_size,waiting_task_array,wish_db)==True: 
                        print("You have scheduled this task before!")
                        skip=True
                        break
                    if check_enough_fund(size_cost,funds)==True:
                        funds-=size_cost
                        task={"function":int(msg),"parameter":wish_size,"livetime":int(2),"func_name":"Upgrading","db":int(wish_db)}
                        waiting_task_array.append(task)
                        print("Database {} ".format(wish_db)+task_alert.format(task["func_name"],task["livetime"]))                            
                        break
            elif msg=="3":
                test_cost=1000
                while True:
                    wish_test=str(input("Which version you want to test(Type 0 to exit this choice) ?"))
                    if wish_test in ava_patches:
                        if check_dup_task(int(msg),wish_test,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(test_cost,funds)==True:
                            funds-=test_cost
                            task={"function":int(msg),"parameter":wish_test,"livetime":int(1),"func_name":"Testing"}
                            waiting_task_array.append(task)
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif wish_test=="0":
                        break
                    else:
                        print("Invalid Input") 
            elif msg=="4":
                patch_cost=2000
                while True:
                    wish_patch=str(input("Which version you want to patch(Type 0 to exit this choice)?"))
                    if wish_patch in ava_patches:
                        if check_dup_task(int(msg),wish_patch,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(patch_cost,funds)==True:
                            funds-=patch_cost
                            task={"function":int(msg),"parameter":wish_patch,"livetime":int(2),"func_name":"Patching"}
                            waiting_task_array.append(task)
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break

                    elif wish_patch=="0":
                        break
                    else:
                        print("Invalid Input")                       
            elif msg=="5":
                split_cost=1500
                if len(db_array)==3:
                    print("No more duty could be split")
                    skip=True
                while True:
                    wish_split=str(input("Which duty you want to split(Type 0 to exit this choice) ?"))
                    if wish_split in db_array[0].duty:
                        if check_dup_task(int(msg),wish_split,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(split_cost,funds)==True:
                            funds-=split_cost
                            task={"function":int(msg),"parameter":wish_split,"livetime":int(1),"func_name":"spliting"}
                            waiting_task_array.append(task)
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif wish_split=="0":
                        break
                    else:
                        print("Invalid Input")
                        
            else:
                skip=True
                print("Invalid Command. Please refer to user manual")


        for db in db_array:
            if db.activate=="Working":
                times = len(db.duty)
                funds+=times*size_fund_func(db.size)
            funds+=times*round_fund_func(db.size,round,total_round)
        
        current_risk_level+=random.randint(1,2)
        if current_risk_level>max_risk_level:
            current_risk_level=max_risk_level

        current_patch_level+=random.randint(1,2)
        if current_patch_level>max_patch_level:
            current_patch_level=max_patch_level

        funds+=risk_round(found_risks,risk_mapping)

        round+=1
    return {"win":True,"rounds":30}

def show_userManual():
    options=[{"key":"1","notices":"Show which risks could be deal with your chosen version"},{"key":"2","notices":"Upgrade db"},{"key":"3","notices":"Test db version"},{"key":"4","notices":"Patch db"}]
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
    punishment_ratio=100
    for risk in found_risks:
        if randomize(10)==True:
            chosen=random.choice(rm[int(risk)-1]["events"])
            random_times=random.randint(1,10)
            punishment=random_times*punishment_ratio
            print("The event {} has triggered".format(chosen))
            print(str(punishment),"has been charged as punishment")
            stacks+=punishment
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
        return 100 
    elif size=="m":
        return 300 
    elif size=="l": #L 
        return 700 
    elif size=="xl":
        return 1000 

def round_fund_func(size,round,total_round): #minus fund for each round size
    punishment_ratio=100
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

def check_dup_task(function,parameter,wta,db): #check duplicate scheduled task
    if db==-1:
        for task in wta:  
            if task["function"]==function and task["parameter"]==parameter:
                return True # duplicated found
        return False
    else:
        for task in wta:  
            if task["function"]==function and task["parameter"]==parameter and task["db"]==db:
                return True # duplicated found
        return False

def user_1_func(pm,available_query_max): #show patch risk mapping NOT TASK
    
    while True:
        msg=int(input("Which version you want to query?"))
        if msg >=1 and msg<=int(available_query_max):
            break
        else:
            print("Invalid Input (You could not query the unexisting version)")
    print(pm[msg-1])
    return True




def game_end(win,rounds):
    if win==True:
        print("Congrats You Won !")
    else : print ("You lose at {} round . Better luck next time !".format(rounds))




while True:
    print("Database Game\nEnter \" 1 \" Start\nEnter \" 2 \" Exit")
    msg=int(input())
    if msg==1:
        os.system('cls')
        with open('patch_mapping.json') as jf1:
            patch_mapping=json.load(jf1)
        with open('risk_mapping.json') as jf2:
            risk_mapping=json.load(jf2)
        stats=game_main(patch_mapping,risk_mapping)
        game_end(stats["win"],stats["rounds"])
    elif msg==2:
        break
    


