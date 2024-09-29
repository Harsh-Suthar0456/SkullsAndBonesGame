import random
import math
import numpy as np
import time

name = "ex=5"
Xg=0
Yg=0
Dx=0
Dy=0
Dp=""
ex_in_opp=(Xg//10) +1
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
    while((len(starts))<=(Xg+Yg-2)):
        starts.append((Xg-Dx-1,Yg-Dy-1))

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
    if int(vertices[6])>=5:
        return plan_b(pirate)
    x=int(vertices[0])
    y=int(vertices[1])
    sl_x=int(vertices[2])
    sl_y=int(vertices[3])
    dp_x=int(vertices[4])
    dp_y=int(vertices[5])
    dir=int(vertices[6])
    #print(x,y)
    #print(x,y,"yoyo",pirate.getID())
    #print(vertices,pirate.getID())
    if pirate.getPosition()[0]==x and pirate.getPosition()[1]==y:
        dir=2
    elif pirate.getPosition()[0]==sl_x and pirate.getPosition()[1]==sl_y:
        dir=5
    # elif pirate.getPosition()[0]==dp_x and pirate.getPosition()[1]==dp_y:
    #     dir=4
    pirate.setSignal(f"{x},{y},{sl_x},{sl_y},{dp_x},{dp_y},{dir}")
    #print(f"{x},{y},{Dx},{Dy},{sl_x},{sl_y},{dp_x},{dp_y},{dir}")
    if dir==1:
        return moveTo(x,y,pirate)
    elif dir==2:
        return moveTo(sl_x,sl_y,pirate)
    elif dir>=5:
        return plan_b(pirate)
    elif dir==4:
        return moveTo(Dx,Dy,pirate)
    

def moveTo(x, y, Pirate):
    # if Pirate.getID()=='1':
    #     print(x,y,Pirate.getPosition())
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1
    
def fa_vertex(pirate):
    start_loc=pirate.getSignal().split(",")
    x=int(start_loc[0])
    y=int(start_loc[1])
    x1=0
    y1=0
    x2=0
    y2=0
    front_of_sl_x=0
    front_of_sl_y=0
    front_of_dp_x=0
    front_of_dp_y=0
    xm=1
    ym=1
    if(Dx==0):
        xm=-1
    if Dy==0:
        ym=-1
    shift=(int(pirate.getID())-1)//2 
    if x==Dx:
        x1=Dx-xm*shift
        y1=Dy
        x2=x-xm*shift
        y2=y
        front_of_sl_x=Xg-x-1
        front_of_sl_y=y
        front_of_dp_x=Xg-Dx-1
        front_of_dp_y=Dy
    elif y==Dy:
        y1=Dy-ym*shift
        x1=Dx
        y2=y-ym*shift
        x2=x
        front_of_sl_x=x
        front_of_sl_y=Yg-y-1
        front_of_dp_x=Dx
        front_of_dp_y=Yg-Dy-1
    signal=f"{x1},{y1},{x2},{y2},{front_of_sl_x},{front_of_sl_y},1"
    pirate.setSignal(signal)
    #print(signal,pirate.getID())

def fa_move(pirate):
    vertices=pirate.getSignal().split(",")
    if int(vertices[6])>=5:
        return plan_b(pirate)
    x1=int(vertices[0])
    y1=int(vertices[1])
    x2=int(vertices[2])
    y2=int(vertices[3])
    x3=int(vertices[4])
    y3=int(vertices[5])
    dir=int(vertices[6])
    if pirate.getPosition()[0]==x1 and pirate.getPosition()[1]==y1:
        dir=2
    elif pirate.getPosition()[0]==x2 and pirate.getPosition()[1]==y2:
        dir=3
    elif pirate.getPosition()[0]==x3 and pirate.getPosition()[1]==y3:
        dir=5
    pirate.setSignal(f"{x1},{y1},{x2},{y2},{x3},{y3},{dir}")
    #print(f"{x},{y},{Dx},{Dy},{sl_x},{sl_y},{dp_x},{dp_y},{dir}")
    if dir==1:
        return moveTo(x1,y1,pirate)
    elif dir==2:
        return moveTo(x2,y2,pirate)
    elif dir==3:
        return moveTo(x3,y3,pirate)
    elif dir>=5:
        return plan_b(pirate)

def plan_b(pirate):
    # print("batak")
    # return random.randint(1,4)
    a=pirate.getPosition()[0]
    b=pirate.getPosition()[1]
    xm=1
    ym=1
    if Dp=="bl" or Dp=="br":
        ym=-1
    if Dp=="tr" or Dp=="br":
        xm=-1
    signal=pirate.getSignal().split(",")
    if pirate.getPosition()== (Xg-1,Yg-1) or pirate.getPosition()== (Xg-1,0) or pirate.getPosition()== (0,Yg-1) or pirate.getPosition()== (0,0):
        signal[6]="41"
        sig=",".join(signal)
        pirate.setSignal(sig)
    if int(signal[-1])==41 :
        #print(pirate.getPosition(),"41 ka loop")
        return moveTo(Dx,Dy,pirate)
    dir=int(signal[6])
    if dir==5:
        signal[6]='6'
        if pirate.investigate_right()[0]=='wall' or pirate.investigate_left()[0]=='wall':
                signal[0]=str(Xg-1-a)
                signal[1]=str(b+ym)
                signal[2]=str(signal[0])
                signal[3]=str(int(signal[1])+ym)
                signal[4]=str(a)
                signal[5]=str(signal[3])
                pirate.setSignal(",".join(signal))
                return moveTo(a,b+ym,pirate)
        elif pirate.investigate_up()[0]=='wall' or pirate.investigate_down()[0]=='wall':
                signal[0]=str(a+xm)
                signal[1]=str(Yg-1-b)
                signal[2]=str(a+xm+xm)
                signal[3]=str(Yg-1-b)
                signal[4]=str(a+xm+xm)
                signal[5]=str(b)
                pirate.setSignal(",".join(signal))
                # print(pirate.getPosition())
                # print(signal)
                return moveTo(a+xm,b,pirate)
    x1=int(signal[0])
    y1=int(signal[1])
    x2=int(signal[2])
    y2=int(signal[3])
    x3=int(signal[4])
    y3=int(signal[5])
    if pirate.getPosition()[0]==x1 and pirate.getPosition()[1]==y1:
        dir=7
    elif pirate.getPosition()[0]==x2 and pirate.getPosition()[1]==y2:
        dir=8
    elif pirate.getPosition()[0]==x3 and pirate.getPosition()[1]==y3:
        dir=5
    signal[6]=str(dir)
    pirate.setSignal(",".join(signal))
    if dir==6:
        return moveTo(x1,y1,pirate)
    elif dir==7:
        return moveTo(x2,y2,pirate)
    elif dir==8:
        return moveTo(x3,y3,pirate)
    elif dir==9:
        return 0


def ActPirate(pirate):
    global ex_in_opp
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x= pirate.getPosition()[0]
    y=pirate.getPosition()[1]
    if pirate.getCurrentFrame()>5*Xg:
        return goIsland(pirate)
    if x==Dx and y==Dy:
        store=pirate.getTeamSignal().split(",")
        #print(type(store))
        iter_num=int(store[0])
        sigx=starts[min(iter_num%(Xg+Yg-2),len(starts)-1)][0]
        sigy=starts[min(iter_num%(Yg+Xg-2),len(starts)-1)][1]
        pirate.setSignal(f"{sigx},{sigy}")
        iter_num+=1
        store[0]=f"{iter_num}"
        output=",".join(store)
        pirate.setTeamSignal(output)
        ##
        id=int(pirate.getID())
        if id>2 and id<= 2*(ex_in_opp+1):
            fa_vertex(pirate)
        else:
            get_vertex(pirate)
    id=int(pirate.getID())
    #print(ex_in_opp,"exinopp")
    checkIsland(pirate)
    if id>2 and id<=2*(ex_in_opp+1):
        return fa_move(pirate)
    else:
        return give_move(pirate)
    
def moveAway(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return random.randint(1, 4)
    if random.randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1

def circleAround(x, y, radius, Pirate):
    position = Pirate.getPosition()
    rx = position[0]
    ry = position[1]
    pos = [[x + i, y + radius] for i in range(-1 * radius, radius + 1)]
    pos.extend([[x + radius, y + i] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x + i, y - radius] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x - radius, y + i] for i in range(-1 * radius + 1, radius)])
    if [rx, ry] not in pos:
        if rx in [x + i for i in range(-1 * radius, radius + 1)] and ry in [
            y + i for i in range(-1 * radius, radius + 1)
        ]:
            return moveAway(x, y, Pirate)
        else:
            return moveTo(x, y, Pirate)
    else:
        index = pos.index([rx, ry])
        clock=random.randint(1,2)
        return moveTo(
            pos[(index + (clock * 2) - 1) % len(pos)][0],
            pos[(index + (clock * 2) - 1) % len(pos)][1],
            Pirate,
        )
    
def goIsland(pirate):
    stri=pirate.getTeamSignal().split(',')
    whichisland=int(stri[9])
    ix=int(stri[1+2*whichisland])
    iy=int(stri[2+2*whichisland])
    if int(stri[7])==0 and pirate.getPosition()[0]==ix and pirate.getPosition()[1]==iy:
        stri[7]=-1
    if int(stri[7])==0:
        stri[7]=str(stri[7])
        kk=",".join(stri)
        pirate.setTeamSignal(kk)
        #print("a")
        return moveTo(ix,iy,pirate)
    elif int(stri[7])=="-1":
        if random.randint(1,2)==1:
            stri[7]=str(stri[7])
            kk=",".join(stri)
            pirate.setTeamSignal(kk)
            #print("b")
            return moveTo(ix,iy,pirate)
        else:
            stri[7]=str(stri[7])
            kk=",".join(stri)
            pirate.setTeamSignal(kk)
            #print("c")
            return circleAround(ix,iy,1,pirate)
    else :
        if int(stri[8])>=105 and int(stri[7])==1:
            px=pirate.getPosition()[0]
            py=pirate.getPosition()[1]
            if abs(px+py-ix-iy)==1:
                stri[7]=str(2)
            kk=",".join(stri)
            pirate.setTeamSignal(kk)
            return moveTo(ix,iy,pirate)
        elif int(stri[8])>=105 and int(stri[7])==2:
            return circleAround(ix,iy,2,pirate)
        else:
            return circleAround(ix,iy,1,pirate)
    


def checkIsland(pirate):
    if pirate.getCurrentFrame()>=1501:
        up = pirate.investigate_up()[0]
        down = pirate.investigate_down()[0]
        left = pirate.investigate_left()[0]
        right = pirate.investigate_right()[0]
        x, y = pirate.getPosition()
        pirate.setSignal("")
        s = pirate.trackPlayers()
        
        if (
            (up == "island1" and s[0] != "myCaptured")
            or (up == "island2" and s[1] != "myCaptured")
            or (up == "island3" and s[2] != "myCaptured")
        ):
            s = up[-1] + str(x) + "," + str(y - 1)
            pirate.setTeamSignal(s)

        if (
            (down == "island1" and s[0] != "myCaptured")
            or (down == "island2" and s[1] != "myCaptured")
            or (down == "island3" and s[2] != "myCaptured")
        ):
            s = down[-1] + str(x) + "," + str(y + 1)
            pirate.setTeamSignal(s)

        if (
            (left == "island1" and s[0] != "myCaptured")
            or (left == "island2" and s[1] != "myCaptured")
            or (left == "island3" and s[2] != "myCaptured")
        ):
            s = left[-1] + str(x - 1) + "," + str(y)
            pirate.setTeamSignal(s)

        if (
            (right == "island1" and s[0] != "myCaptured")
            or (right == "island2" and s[1] != "myCaptured")
            or (right == "island3" and s[2] != "myCaptured")
        ):
            s = right[-1] + str(x + 1) + "," + str(y)
            pirate.setTeamSignal(s)

        
        if pirate.getTeamSignal() != "":
            s = pirate.getTeamSignal()
            l = s.split(",")
            x = int(l[0][1:])
            y = int(l[1])
        
            return moveTo(x, y, pirate)

        else:
            return random.randint(1, 4)
########################################################################
    stri=pirate.getTeamSignal().split(',')
    for hg in range(0,10):
        stri[hg]=int(stri[hg])
    if -1 in stri:
        isl=0
        ix=0
        up = pirate.investigate_up()
        if up[0] == "island1":
            ix=1
            isl+=8
        down = pirate.investigate_down()
        if down[0] == "island1":
            ix=1
            isl+=4
        left = pirate.investigate_left()
        if left[0] == "island1":
            isl+=2
        right = pirate.investigate_right()
        if right[0] == "island1":
            isl+=1
        if up[0] == "island2":
            ix=2
            isl+=8
        down = pirate.investigate_down()
        if down[0] == "island2":
            ix=2
            isl+=4
        left = pirate.investigate_left()
        if left[0] == "island2":
            isl+=2
        right = pirate.investigate_right()
        if right[0] == "island2":
            isl+=1
        if up[0] == "island3":
            ix=3
            isl+=8
        down = pirate.investigate_down()
        if down[0] == "island3":
            ix=3
            isl+=4
        left = pirate.investigate_left()
        if left[0] == "island3":
            isl+=2
        right = pirate.investigate_right()
        if right[0] == "island3":
            isl+=1
        cord=[-45,-45]
        if isl==14:
            cord=[pirate.getPosition()[0]-1,pirate.getPosition()[1]]
        if isl==13:
            cord=[pirate.getPosition()[0]+1,pirate.getPosition()[1]]
        if isl==7:
            cord=[pirate.getPosition()[0],pirate.getPosition()[1]+1]
        if isl==11:
            cord=[pirate.getPosition()[0],pirate.getPosition()[1]-1]
        if cord==[-45,-45]:
            return
        stri[ix*2-1]=cord[0]
        stri[ix*2]=cord[1]
        for hg in range(0,10):
            stri[hg]=str(stri[hg])
        kk=",".join(stri)
        pirate.setTeamSignal(kk)

def ActTeam(team):
    #time.sleep(0.1)
    #print(team.getCurrentFrame())
    if team.getCurrentFrame==1500:
        team.getTeamSignal==""
    if team.getCurrentFrame>1500:
        l = team.trackPlayers()
        s = team.getTeamSignal()
        team.buildWalls(1)
        team.buildWalls(2)
        team.buildWalls(3)
        # print(team.getTeamSignal())
        # print(team.trackPlayers())
        if s:
            island_no = int(s[0])
            signal = l[island_no - 1]
            if signal == "myCaptured":
                team.setTeamSignal("")
######################################################
    if team.getCurrentFrame()==1:
        global Xg,Yg,Dx,Dy,Dp,ex_in_opp,starts
        starts.clear()
        Xg=team.getDimensionX()
        Yg=team.getDimensionY()
        Dx=team.getDeployPoint()[0]
        Dy=team.getDeployPoint()[1]
        ex_in_opp=Xg//10 +1
        set_Dp()
        #print(Dp,Xg,Yg,Dx,Dy)
        #Dp="tl"
        make_starts()
        #print(starts)
        team.setTeamSignal("0,-1,-1,-1,-1,-1,-1,0,0,0")
    stri=team.getTeamSignal().split(',')
    if team.getCurrentFrame()>150:
        if team.trackPlayers()[int(stri[9])]=="myCapturing":
            stri[8]=int(stri[8])+1
        else:
            stri[8]=0
    if int(stri[8])==7:
        stri[7]=1
    if int(stri[8])==107 or int(stri[8])==20:
        team.buildWalls(int(stri[9])+1)
    if int(stri[8])==110:

        stri[9]=str((int(stri[9])+1)%3)
        stri[7]=str(0)
        stri[8]=str(0)
    stri[7]=str(stri[7])
    stri[8]=str(stri[8])
    kk=",".join(stri)
    team.setTeamSignal(kk)

    
    
        



    
    # if team.getCurrentFrame()==46:
    #     abcd=1
    #     input(abcd)
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