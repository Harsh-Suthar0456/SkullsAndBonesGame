import random
import math
import numpy as np

name = "scriptblue"
Xg=0
Yg=0
Dx=0
Dy=0
Dp=""
ex_in_opp=4
starts=list()


def set_Dp():
    global Dp
    #print(Xg,Yg)
    if Dx==Xg-1 and Dy==Yg-1:
        Dp="br"
    elif Xg-1==Dx and Dy==0:
        Dp="tr"
    elif Dx==0 and Dy==Yg-1:
        Dp="bl"
    elif Dx==0 and Dy==0:
        Dp="tl"

def make_starts():
    global Dp,starts
    if Dp=="br":
        flag1=0
        x=Xg//2 -ex_in_opp
        y=Yg//2 -ex_in_opp
        for i in range(0,Xg+Yg):
            if flag1==0:
                if x!=Xg-1:
                    starts.append((x%Xg,Yg-1))
                x+=1
                flag1=1-flag1
            else:
                if y!=Yg-1:
                    starts.append((Xg-1,y%Yg))
                y+=1
                flag1=1-flag1
    elif Dp=="bl":
        flag1=0
        x=Xg//2 +ex_in_opp-1
        y=Yg//2 -ex_in_opp
        for i in range(0,Xg+Yg):
            if flag1==0:
                if x!=0:
                    starts.append((x%Xg,Yg-1))
                x-=1
                flag1=1-flag1
            else:
                if y!=Yg-1:
                    starts.append((0,y%Yg))
                y+=1
                flag1=1-flag1
    elif Dp=="tl":
        flag1=0
        x=Xg//2 +ex_in_opp-1
        y=Yg//2 +ex_in_opp-1
        for i in range(0,Xg+Yg):
            if flag1==0:
                if x!=0:
                    starts.append((x%Xg,0))
                x-=1
                flag1=1-flag1
            else:
                if y!=0:
                    starts.append((0,y%Yg))
                y-=1
                flag1=1-flag1
    elif Dp=="tr":
        flag1=0
        x=Xg//2 -ex_in_opp
        y=Yg//2 +ex_in_opp-1
        for i in range(0,Xg+Yg):
            if flag1==0:
                if x!=0:
                    starts.append((x%Xg,0))
                x+=1
                flag1=1-flag1
            else:
                if y!=0:
                    starts.append((Xg-1,y%Yg))
                y-=1
                flag1=1-flag1

def get_vertex(pirate):
    start_loc=pirate.getSignal().split(",")
    x=int(start_loc[0])
    y=int(start_loc[1])
    front_of_sl_x=0
    front_of_sl_y=0
    front_of_dp_x=0
    front_of_dp_y=0
    if x==Dx:
        front_of_sl_x=Xg-x-1
        front_of_sl_y=y
        front_of_dp_x=Xg-Dx-1
        front_of_dp_y=Dy
    elif y==Dy:
        front_of_sl_x=x
        front_of_sl_y=Yg-y-1
        front_of_dp_x=Dx
        front_of_dp_y=Yg-Dy-1
    signal=f"{x},{y},{front_of_sl_x},{front_of_sl_y},{front_of_dp_x},{front_of_dp_y},1"
    #print(signal,pirate.getID())
    pirate.setSignal(signal)


def give_move(pirate):
    vertices=pirate.getSignal().split(",")
    x=int(vertices[0])
    y=int(vertices[1])
    sl_x=int(vertices[2])
    sl_y=int(vertices[3])
    dp_x=int(vertices[4])
    dp_y=int(vertices[5])
    dir=int(vertices[6])
    print(x,y)
    #print(x,y,"yoyo",pirate.getID())
    #print(vertices,pirate.getID())
    if pirate.getPosition()[0]==x and pirate.getPosition()[1]==y:
        dir=2
    elif pirate.getPosition()[0]==sl_x and pirate.getPosition()[1]==sl_y:
        dir=3
    elif pirate.getPosition()[0]==dp_x and pirate.getPosition()[1]==dp_y:
        dir=4
    pirate.setSignal(f"{x},{y},{sl_x},{sl_y},{dp_x},{dp_y},{dir}")
    #print(f"{x},{y},{Dx},{Dy},{sl_x},{sl_y},{dp_x},{dp_y},{dir}")
    if dir==1:
        return moveTo(x,y,pirate)
    elif dir==2:
        return moveTo(sl_x,sl_y,pirate)
    elif dir==3:
        return moveTo(dp_x,dp_y,pirate)
    elif dir==4:
        return moveTo(Dx,Dy,pirate)
    

def moveTo(x, y, Pirate):
    if Pirate.getID()=='1':
        print(x,y,Pirate.getPosition())
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    # if random.randint(1, 2) == 1:
    #     return (position[0] > x) * 2 + 2
    # else:
    #     return (position[1] < y) * 2 + 1
    
def n_move(pirate):
    cx=pirate.getPosition()[0]
    cy=pirate.getPosition()[1]
    move_weight=np.array([0.0,0.0,0.0,0.0])
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]

    


def ActPirate(pirate):
    if pirate.getCurrentFrame()<=11:
        return 0
    elif pirate.getCurrentFrame()>=700:
        return random.randint(1,4)
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x= pirate.getPosition()[0]
    y=pirate.getPosition()[1]
    if x==Dx and y==Dy:
        iter_num=int(pirate.getTeamSignal())
        sigx=starts[iter_num%(Xg+Yg-2)][0]
        sigy=starts[iter_num%(Yg+Xg-2)][1]
        pirate.setSignal(f"{sigx},{sigy}")
        iter_num+=1
        pirate.setTeamSignal(f"{iter_num}")
        get_vertex(pirate)
    return give_move(pirate)


def ActTeam(team):
    if team.getCurrentFrame()==1:
        global Xg,Yg,Dx,Dy,Dp
        Xg=team.getDimensionX()
        Yg=team.getDimensionY()
        Dx=team.getDeployPoint()[0]
        Dy=team.getDeployPoint()[1]
        set_Dp()
        #print(Dp,Xg,Yg,Dx,Dy)
        #Dp="tl"
        make_starts()
        team.setTeamSignal("0")
        #print(starts)
    # l = team.trackPlayers()
    # s = team.getTeamSignal()

    # team.buildWalls(1)
    # team.buildWalls(2)
    # team.buildWalls(3)
    # # print(team.getTeamSignal())
    # # print(team.trackPlayers())
    # if s:
    #     island_no = int(s[0])
    #     signal = l[island_no - 1]
    #     if signal == "myCaptured":
    #         team.setTeamSignal("")