# TO DO Security level punishment + inspect risk 
import json
import os
import numpy as np
import random
import pandas as pd
from tabulate import tabulate # pretty print

class database:
    def __init__(self,version,duty,name="Database",size=1,encryption="N/A",hashing="N/A"):
        self.activate="Working"
        self.name=name
        self.size=size
        self.version=version
        self.encryption=encryption 
        self.duty=duty      
        self.hashing=hashing
            
    def print_detail(self):
        print("\n~",self.name,"~")
        print("Service : ", str(self.activate))
        print("Size : ",size_converter(self.size))
        print("Current Version : " ,self.version) 
        print("Encryption : ",self.encryption)
        print("Hashing for Password :",self.hashing)
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
    risk_detail_array=[] #show detail dangerous
    current_patch_level=1
    max_patch_level=len(patch_mapping) #max patch level
    ava_patches=[]
    tested_version=[]
    end_game=False
        
    waiting_task_array=[] #core array
    accident_array=[] #store accidents

    max_task_profit=4 # if there is 5 task no profit as whole db is repairing

    options=[{"key":"e","notices":"Turn to go to next round."},{"key":"n","notices":"Show User Manual."}] #set options
    task_alert="Task {} has been scheduled . {} rounds after will be done" #task template 
    split_counter=0 #to control user do not split more than 3

    db_array=[]
    db=database("1",["UserPII","OrderDetails","PartnerInfo"] )
    db_array.append(db)
    asset_dict={"dmz":"N/A","fw":"N/A"} # dmz firewall

    while round<=total_round: #whole game loop

        skip=False #cause new round no skip info
        if end_game==True or funds<0: #instant die
            return {"win":False,"rounds":round}

        round_ratio=round/total_round #INDICATE 0.xx~1
        for i in range(current_risk_level-len(risk_detail_array)):
            risk_detail_array.append(risk_detail_gen(round_ratio))
           

        print("\n-------\nRounds : ", round ,"/",total_round) #show current round
        waiting_task_array=scheduled_task_func(waiting_task_array,db_array,tested_version,asset_dict) #check scheduled
        while True: # round loop
            
            if skip==False:
                print("Funds : ",funds)
                for db in db_array:
                    db.print_detail()
                print("\n~ General Information ~")
                system_statb_level=ss_level_func(db_array,round_ratio)
                print(">> Whole System is {} <<".format(system_statb_level["comment"]))
                security_level=sec_level_func(found_risks,asset_dict,db_array)
                # print(security_level)
                sec_label=show_sec_level(security_level)
                print("External Security :",sec_label)
                found_risks=current_threat(current_risk_level,patch_mapping,int(db_array[0].version))
                print("Current found risks : ["+",".join(found_risks)+"]")
                ava_patches=current_ava_patches(current_patch_level,int(db_array[0].version))
                print("Current available versions : ["+",".join(ava_patches)+"]")
                print("Current tested versions : ["+",".join(tested_version)+"]" )
                print("Firewall :",asset_dict["fw"])
                if (asset_dict["fw"]=="Working"): #ensure
                    print("Demilitarized zone :",asset_dict["dmz"])
            skip=False    
                
            for i in range(len(options)):
                print("Enter \"{}\" to {}".format(options[i]["key"],options[i]["notices"]))   
            msg=str(input("Command :"))
            if msg=="e":
                break
            elif msg=="n":
                skip=show_userManual()
            elif msg=="1":
                skip=user_1_func(patch_mapping,ava_patches)
            elif msg=="2":
                skip=user_2_func(found_risks,risk_detail_array)
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
                            waiting_task_array.append(task) #success
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif wish_test=="0":
                        skip=True
                        break
                    else:
                        print("Invalid Input") 
            elif msg=="4":
                patch_cost=2000
                while True:
                    wish_patch=str(input("Which version you want to patch(Type 0 to exit this choice)?"))
                    if wish_patch in ava_patches:
                        wish_mode=str(input("Which mode you want to use for patching(Type 0 to exit this choice)?"))
                        if wish_mode=="0":
                            skip=True
                            break
                        elif wish_mode=="Auto":
                            livetime=2
                        elif wish_mode=="Manual":
                            livetime=3
                        else:
                            print("Invalid Input")
                            continue 
                        if check_dup_task(int(msg),wish_patch,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(patch_cost,funds)==True:
                            funds-=patch_cost
                            task={"function":int(msg),"parameter":wish_patch,"livetime":livetime,"func_name":"Patching"}
                            waiting_task_array.append(task) #success
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break

                    elif wish_patch=="0":
                        skip=True
                        break
                    else:
                        print("Invalid Input")                       
            elif msg=="5":
                split_cost=1500
                if split_counter>=2 :
                    print("No more duty could be split")
                    skip=True
                    break
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
                            waiting_task_array.append(task) #success
                            split_counter+=1
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif wish_split=="0":
                        break
                    else:
                        print("Invalid Input")
            elif msg=="6":
                encrypt_cost=1500
                while True:
                    wish_db=int(input("Which db you want to encrypt(Type 0 to exit this choice)?"))
                    if str(wish_db)=="0":
                        skip=True
                        break
                    elif wish_db>len(db_array) or wish_db<=0:
                        print("Invalid Input")
                        continue
                    elif db_array[int(wish_db)-1].encryption == "AES256":
                        print("Chosen Database has the highest encrypt level")
                        continue
                    wish_bits=str(input("Which encryption method you want to apply(Type 0 to exit this choice)?"))
                    if wish_bits=="0":
                        skip=True
                        break
                    elif wish_bits=="AES128":
                        livetime=1
                    elif wish_bits=="AES256":
                        livetime=2
                    else:
                        print("Invalid Input")
                        continue
                    if check_dup_task(int(msg),wish_bits,waiting_task_array,wish_db)==True: 
                        print("You have scheduled this task before!")
                        skip=True
                        break
                    if check_enough_fund(encrypt_cost,funds)==True:
                        funds-=encrypt_cost
                        task={"function":int(msg),"parameter":wish_bits,"livetime":livetime,"func_name":"Encrypting","db":wish_db}
                        waiting_task_array.append(task)
                        print("Database {} ".format(wish_db)+task_alert.format(task["func_name"],task["livetime"]))                            
                        break
            elif msg=="7":
                while True:
                    wish_db=int(input("Which db you want to upgrade(Type 0 to exit this choice)?"))
                    if str(wish_db)=="0":
                        skip=True
                        break
                    elif wish_db>len(db_array) or wish_db<=0:
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
                        task={"function":int(msg),"parameter":size_converter(wish_size),"livetime":int(2),"func_name":"Upgrading","db":int(wish_db)}
                        waiting_task_array.append(task)
                        print("Database {} ".format(wish_db)+task_alert.format(task["func_name"],task["livetime"]))                            
                        break                        
            elif msg=="8":
                hashing_cost=1500
                while True:
                    if db_array[0].hashing == "SHA2":
                        print("Chosen Database has the highest hashing level")
                        break
                    wish_bits=str(input("Which hashing method you want to apply(Type 0 to exit this choice)?"))
                    if wish_bits=="0":
                        skip=True
                        break
                    elif wish_bits=="MD5":
                        livetime=1
                    elif wish_bits=="SHA2":
                        livetime=2
                    else:
                        print("Invalid Input")
                        continue
                    if check_dup_task(int(msg),wish_bits,waiting_task_array,-1)==True: 
                        print("You have scheduled this task before!")
                        skip=True
                        break
                    if check_enough_fund(hashing_cost,funds)==True:
                        funds-=hashing_cost
                        task={"function":int(msg),"parameter":wish_bits,"livetime":livetime,"func_name":"Encrypting"}
                        waiting_task_array.append(task) #success
                        print("Database {} ".format(wish_db)+task_alert.format(task["func_name"],task["livetime"]))                            
                        break
            elif msg=="9":
                build_cost=3000
                while True:
                    ans=str(input("Are you sure to build firewall ?"))
                    if asset_dict["fw"]=="Working":
                        print("Firewall is working and built previously !")
                        skip=True
                        break
                    if ans=="y":
                        if check_dup_task(int(msg),ans,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(build_cost,funds)==True:
                            funds-=build_cost
                            task={"function":int(msg),"parameter":ans,"livetime":1,"func_name":"Firewall building"}
                            waiting_task_array.append(task) #success
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif ans=="n":
                        skip=True
                        break
                    else:
                        print("Invalid Input") 
            elif msg=="10":
                build_cost=1000
                while True:
                    ans=str(input("Are you sure to apply Demilitarized zone?"))
                    if asset_dict["fw"]=="N/A":
                        print("You have to build firewall first !")
                        skip=True
                        break
                    if asset_dict["dmz"]=="Working":
                        print("Demilitarized zone is working and applied previously !")
                        skip=True
                        break
                    if ans=="y":
                        if check_dup_task(int(msg),ans,waiting_task_array,-1)==True:
                            print("You have scheduled this task before!")
                            skip=True
                            break
                        if check_enough_fund(build_cost,funds)==True:
                            funds-=build_cost
                            task={"function":int(msg),"parameter":ans,"livetime":1,"func_name":"Firewall building"}
                            waiting_task_array.append(task) #success
                            print(task_alert.format(task["func_name"],task["livetime"]))
                            break
                    elif ans=="n":
                        skip=True
                        break
                    else:
                        print("Invalid Input") 
            else:
                skip=True
                print("Invalid Command. Please refer to user manual")

        print("\n~ End Round result ~")

        for db in db_array:
            if db.activate=="Working":
                times = len(db.duty)
                overload =4-len(waiting_task_array)
                if overload<0:overload=0
                profits=times*size_fund_func(size_converter(db.size))* (overload/max_task_profit) *system_statb_level["ratio"]        # no. duty * size_earning * task load * system stability
                funds+=profits
        print("Profits from Food Delievery app :+",profits)
        if overload<2:
            print("Alert! Too many scheduled tasks will cause the app could not work for a certain time.")  
        funds-=risk_round(found_risks,risk_mapping,sec_label,round_ratio,risk_detail_array)

        random_no=random.randint(0,1)
        current_risk_level+=random_no
        if current_risk_level>max_risk_level:
            current_risk_level=max_risk_level

        current_patch_level+=random_no
        if current_patch_level>max_patch_level:
            current_patch_level=max_patch_level
        round+=1
    return {"win":True,"rounds":30}

def show_userManual():
    options=[{"key":"1","notices":"Inspect Version Report"},{"key":"2","notices":"Inspect Risk Report"},{"key":"3","notices":"Test db version"},{"key":"4","notices":"Patch db"},{"key":"5","notices":"split db"},{"key":"6","notices":"encrypt db"},{"key":"7","notices":"Upgrade db"}]
    for i in range(len(options)):
        print("Enter \"{}\" to {}".format(options[i]["key"],options[i]["notices"]))
    return True

def randomize(percent):
    random_no=random.randint(1,100)
    if random_no<percent:
        return True
    else:
        return False

def size_converter(para):
    para=str(para)
    if para=="1":
        return "s"
    elif para=="2":
        return "m"
    elif para=="3":
        return "l"
    elif para=="4":
        return "xl"
    elif para=="s":
        return 1
    elif para=="m":
        return 2
    elif para=="l":
        return 3
    elif para=="xl":
        return 4

def risk_detail_gen(percentile): #risk dict make
    column_list=["av","ac","pr","cia","gs"]
    risk_dict={}
    dang_sum=0
    for i in range(len(column_list)-1):
        dang=risk_dang_gen(percentile)
        dang_sum+=dang
        risk_dict[column_list[i]]=dang
    risk_dict["gs"]=round(dang_sum/4)
    return risk_dict

def risk_dang_gen(percentile): #random risk dangerous
    base=100
    low=base*(1-percentile)
    medium=base*(1-percentile*percentile)
    high=base*(1-percentile*percentile*percentile)
    # print(low,medium,high)
    # if percentile<0.3:
    #     low=80
    #     medium=90
    #     high=100
    #     vh=101
    # elif percentile<0.6:
    #     low=40
    #     medium=70
    #     high=90
    #     vh=100
    # elif percentile<0.9:
    #     low=20
    #     medium=40
    #     high=75
    #     vh=100
    # else:
    #     low=0
    #     medium=30
    #     high=70
    #     vh=100
    random_no=float(random.randint(1,100))
    if random_no<low:
        return 1
    elif random_no<medium:
        return 2
    elif random_no<high:
        return 3
    else:
        return 4

def risk_round(found_risks,rm,sec_label,round_ratio,risk_detail_array): #punish when risk is on
    punishment_ratio=500
    punishment=0 #no triggered
    if sec_label=="Low":
        percentile=50*round_ratio
    elif sec_label=="Medium":
        percentile=30*round_ratio  
    elif sec_label=="High":
        percentile=15*round_ratio  
    elif sec_label=="Excellent":
        percentile=5*round_ratio   

    for risk in found_risks:
        gs=risk_detail_array[int(risk)-1]["gs"]
        if gs==1:
            another_percentile=5*round_ratio
        elif gs==2:
            another_percentile=15*round_ratio  
        elif gs==3:
            another_percentile=30*round_ratio  
        elif gs==4:
            another_percentile=50*round_ratio   
        
        if randomize(round(percentile+another_percentile))==True:
            chosen=random.choice(rm[int(risk)-1]["events"])
            punishment=gs*punishment_ratio
            print("The event {} has triggered".format(chosen))
            print(str(punishment),"has been charged as punishment")
            break
    return punishment

def scheduled_task_func(waiting_task_array,db_array,tested_version,asset_dict):
    trash_task_array=[] # prevent bug
    print("~ Your schedualed tasks ~")
    for task in waiting_task_array: ###do schedualed task
        task["livetime"]-=1
        if task["livetime"]==0:
            
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
                db_array.append(database(db_array[0].version,[task["parameter"]],name="Database "+str(len(db_array)+1)))
                print("Task : main database splited with seperate {} database !".format(task["parameter"]))
            if task["function"]==6:
                db_array[task["db"]-1].encryption=task["parameter"]
                print("Task : database {} encryption changed to {} !".format(task["db"],task["parameter"]))
            if task["function"]==7:
                db_array[task["db"]-1].size=task["parameter"] 
                print("Task : database {} upgraded to {} size !".format(task["db"],size_converter(task["parameter"])))
            if task["function"]==8:
                for db in db_array:
                    db.hashing=task["parameter"]
                print("Task : database {} hashing changed to {} !".format(task["db"],task["parameter"]))
            if task["function"]==9:
                asset_dict["fw"]="Working"
                print("Task : Firewall has been built ! ")
            if task["function"]==10:
                asset_dict["dmz"]="Working"
                print("Task : Firewall has been built ! ")
            trash_task_array.append(task)
        else:
            print("Task : {} {} has {} rounds remaining".format(task["func_name"],task["parameter"],task["livetime"]))
    print("~          ~            ~")
    waiting_task_array=[task for task in waiting_task_array if task not in trash_task_array]
    return waiting_task_array

def ss_level_func(db_array,round_ratio):
    size=0
    for db in db_array:
        size+=db.size
    sample=round_ratio*18
    if size <sample/4:
        ratio=0.3
        comment="Very unstable"
    elif size <sample/2:
        ratio=0.6
        comment="Unstable"
    else:
        ratio=1
        comment="Stable"
    return {"ratio":ratio,"comment":comment}


def sec_level_func(found_risks,asset_dict,db_array):
    total_score=0
    
    asset_score=0
    if asset_dict["fw"]=="working":
        asset_score=12.5
        if asset_dict["dmz"]=="working":
            asset_score*=2

    risk_sc_ratio= -25
    risk_score = (len(found_risks)-1) * risk_sc_ratio
    
    encrypt_score=0
    for db in db_array:
        if db.encryption=="AES128":
            encrypt_score+=6.25
        elif db.encryption=="AES256":
            encrypt_score+=12.5

    hashing_score=0
    if db_array[0].hashing=="MD5":
        hashing_score=6.25
    elif db_array[0].hashing=="MD5":
        hashing_score=12.5
    total_score=asset_score+risk_score+encrypt_score+hashing_score
    return total_score

def show_sec_level(security_level):
    if security_level<25:
        label="Low"
    elif security_level<50:
        label="Medium"
    elif security_level<75:
        label="High"
    elif security_level<100:
        label="Excellent"    
    return label
    
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

def user_1_func(pm,ava_patches): #show patch risk mapping NOT TASK
    
    if len(ava_patches)==0:
        print("No Patch Currently Found")
    else:
        row_data=[]
        headers=["Version Name","Able to deal with"]
        print("~     Version Report     ~")
        for i in range(int(ava_patches[0])-1,int(ava_patches[-1])):
            msg=[str(i+1),pm[i-1]["risk"]]
            row_data.append(msg)
        df=pd.DataFrame(data = row_data, columns= headers)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False)) #pretty print
    return True

def user_2_func(found_risks,risk_detail_array):
    
    if len(found_risks)==0:
        print("No Risk Currently Found")
    else:
        row_data=[]
        headers=["Risk Name","Attack Vector","Attack Complex","Privileges Required","CIA","General Score"]
        print("~     Risk Report     ~")
        for i in range(int(found_risks[0])-1,int(found_risks[-1])):
            msg=[str(i+1)]
            for key in risk_detail_array[i]:
                if risk_detail_array[i][key]==1:
                    msg.append("Low")
                elif risk_detail_array[i][key]==2:
                    msg.append("Medium")
                elif risk_detail_array[i][key]==3:
                    msg.append("High")
                elif risk_detail_array[i][key]==4:
                    msg.append("Very High")
            row_data.append(msg)
        df=pd.DataFrame(data = row_data, columns= headers)
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False)) #pretty print
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
    


