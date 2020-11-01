class web_app_ser:
    def __init__(self,name="Web Application Server"):
        self.activate=True
        self.name=name
        self.size="small"
        
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
        self.size="small"
        self.version="12c"
        self.pns=False              #Primary + Secondary
        self.available_version=[] 
        self.tested_version=[]
        self.risk=[]
            
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
        print("Primary and Secondary Method : " ,self.pns)            
        print("Available Versions : " ,self.available_version)
        print("Tested Versions : " ,self.tested_version)
        print("Risks : " ,self.risk)


def game_main():
    funds=1000
    round=1
    total_round=30 #default total round
    game_time=1 #indicate risk
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
        
        round+=1

def game_end():
    print("Ended")

while True:
    print("Database Game\nEnter \" 1 \" Start\nEnter \" 2 \" Exit")
    msg=int(input())
    if msg==1:
        game_main()
        game_end()
    elif msg==2:
        break
    

    
