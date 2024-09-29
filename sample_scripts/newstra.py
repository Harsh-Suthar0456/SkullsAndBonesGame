import random
import math
import numpy as np

name = "scriptblue"
map_explore=np.zeros((1,1,2))


def moveTo(x, y, Pirate):
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
    
def n_move(pirate):
    cx=pirate.getPosition()[0]
    cy=pirate.getPosition()[1]
    move_weight=np.array([0.0,0.0,0.0,0.0])
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]

    num_of_friend=0
    if pirate.investigate_up()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_down()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_right()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_left()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_ne()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_nw()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_se()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_sw()[1]=="friend":
        num_of_friend+=1
    if pirate.investigate_current()[1]=="friend":
        num_of_friend+=1
    ##################for crowd control
    if (int(pirate.getID()) not in range(1,11)) and num_of_friend>=3:
        cprob=np.array([0.0,0.0,0.0,0.0])
        denom=1.0*(pirate.getDimensionX()+pirate.getDimensionY()-2)
        cprob[0]=1.0*(cy)/denom
        cprob[1]=1.0*(pirate.getDimensionX()-cx-1)/denom
        cprob[2]=1.0*(pirate.getDimensionY()-cy-1)/denom
        cprob[3]=1.0*(cx)/denom
        crowd_p=random.random()
        for u in range(0,4):
            if(crowd_p<cprob[u]):
                return u+1
            else :
                crowd_p-=cprob[u]
        return 0

    # if up=="wall":
    #     move_weight[0]=10**6
    # elif map_explore[cx,cy-1,1]==0:
    #     map_explore[cx,cy-1,0]=10
    #     map_explore[cx,cy-1,1]=1
    #     return 1
    # else :
    #     move_weight[0]=map_explore[cx,cy-1,0]

    # if right=="wall":
    #     move_weight[1]=10**6
    # elif map_explore[cx+1,cy,1]==0:
    #     map_explore[cx+1,cy,0]=10
    #     map_explore[cx+1,cy,1]=1
    #     return 2
    # else :
    #     move_weight[1]=map_explore[cx+1,cy,0]

    # if down=="wall":
    #     move_weight[2]=10**6
    # elif map_explore[cx,cy+1,1]==0:
    #     map_explore[cx,cy+1,0]=10
    #     map_explore[cx,cy+1,1]=1
    #     return 3
    # else :
    #     move_weight[2]=map_explore[cx,cy+1,0]

    # if left=="wall":
    #     move_weight[3]=10**6
    # elif map_explore[cx-1,cy,1]==0:
    #     map_explore[cx-1,cy,0]=10
    #     map_explore[cx-1,cy,1]=1
    #     return 4
    # else :
    #     move_weight[3]=map_explore[cx-1,cy,0]

    freedom=np.array([0.0,0.0,0.0,0.0])
    fsum=0
    if up=="wall":
        move_weight[0]=10**6
    elif map_explore[cx,cy-1,1]==0:
        freedom[0]=1.0
        fsum+=1.0
    else :
        move_weight[0]=map_explore[cx,cy-1,0]

    if right=="wall":
        move_weight[1]=10**6
    elif map_explore[cx+1,cy,1]==0:
        freedom[1]=1.0
        fsum+=1.0
    else :
        move_weight[1]=map_explore[cx+1,cy,0]

    if down=="wall":
        move_weight[2]=10**6
    elif map_explore[cx,cy+1,1]==0:
        freedom[2]=1.0
        fsum+=1.0
    else :
        move_weight[2]=map_explore[cx,cy+1,0]

    if left=="wall":
        move_weight[3]=10**6
    elif map_explore[cx-1,cy,1]==0:
        freedom[3]=1.0
        fsum+=1.0
    else :
        move_weight[3]=map_explore[cx-1,cy,0]
    
    if fsum!=0:
        for g in range(0,4):
            freedom[g]=1.0*freedom[g]/fsum
        eqprob=random.random()
        for u in range(0,4):
            if(eqprob<freedom[u]):
                return u+1
            else :
                eqprob-=freedom[u]
        return 0



    
    sum=0
    prob=np.array([0.00,0.00,0.00,0.00])
    for g in range(0,4):
        pr=1.0
        for o in range(0,4):
            if g!=o:
                pr*=move_weight[o]
        prob[g]=pr
        sum+=pr
    for g in range(0,4):
        prob[g]=1.0*prob[g]/sum

    p=random.random()
    for u in range(0,4):
        if(p<prob[u]):
            return u+1
        else :
            p-=prob[u]
    return 0
    # mi=move_weight[0]
    # h=0
    # for u in range(1,4):
    #     if(move_weight[u]<mi):
    #         mi=move_weight[u]
    #         h=u
    # return h+1


def ActPirate(pirate):
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

    #map_explore[pirate.getPosition()[0],pirate.getPosition()[1],0]=50
    #map_explore[pirate.getPosition()[0],pirate.getPosition()[1],1]=1

    # if pirate.getTeamSignal() != "":
    #     s = pirate.getTeamSignal()
    #     l = s.split(",")
    #     x = int(l[0][1:])
    #     y = int(l[1])
    
    #     return moveTo(x, y, pirate)
    # if pirate.getCurrentFrame()<500 :
    #     return random.randint(1,4) 
    # else:
    if pirate.getCurrentFrame()<500:
        noj=n_move(pirate)
        if noj==1:
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]-1,0]=10
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]-1,1]=1
        elif noj==2:
            map_explore[pirate.getPosition()[0]+1,pirate.getPosition()[1],0]=10
            map_explore[pirate.getPosition()[0]+1,pirate.getPosition()[1],1]=1
        elif noj==3:
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]+1,0]=10
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]+1,1]=1
        elif noj==4:
            map_explore[pirate.getPosition()[0]-1,pirate.getPosition()[1],0]=10
            map_explore[pirate.getPosition()[0]-1,pirate.getPosition()[1],1]=1
        return noj
    else:
        if pirate.getTeamSignal() != "":
            s = pirate.getTeamSignal()
            l = s.split(",")
            x = int(l[0][1:])
            y = int(l[1])
            return moveTo(x, y, pirate)
        else :
            noj=n_move(pirate)
        if noj==1:
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]-1,0]=10
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]-1,1]=1
        elif noj==2:
            map_explore[pirate.getPosition()[0]+1,pirate.getPosition()[1],0]=10
            map_explore[pirate.getPosition()[0]+1,pirate.getPosition()[1],1]=1
        elif noj==3:
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]+1,0]=10
            map_explore[pirate.getPosition()[0],pirate.getPosition()[1]+1,1]=1
        elif noj==4:
            map_explore[pirate.getPosition()[0]-1,pirate.getPosition()[1],0]=10
            map_explore[pirate.getPosition()[0]-1,pirate.getPosition()[1],1]=1
        return noj



def ActTeam(team):
    #print(team.getCurrentFrame())
    if team.getCurrentFrame()==1 :
        map_explore.resize(team.getDimensionX(),team.getDimensionY(),2)
        
    for g in range(0,team.getDimensionX()):
        for o in range(0,team.getDimensionY()):
            map_explore[g,o,0]=max(1,map_explore[g,o,0]-1)
    
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