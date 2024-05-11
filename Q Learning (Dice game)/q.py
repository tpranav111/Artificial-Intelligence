import random
import argparse
import numpy as np
import math

def initialize_tables(L, ND):              #Initialize Win and Losses 3-D matrices
    return np.zeros((L+1, L+1, ND+1)), np.zeros((L+1, L+1, ND+1))

def printWinsandLosses(Wins, Losses):       #Func just to print Wins & Losses matrices
    print("WINS:")
    print(Wins)
    print("LOSSES:")
    print(Losses)

#Below function calculates Wd and Pd values across all the episodes and games: ie. for the whole of Wins and Losses array (NOt asked Hence, can be ignored)
'''
def calcDiceProb(Wins, Losses, n, M):
    w_list = [0] * (n+1)
    l_list = [0] * (n+1)
    T = 0

    for i in range(len(Wins)):
        for j in range(len(Wins[i])):
            for k in range(len(Wins[i][j])):
                w_list[k] += Wins[i][j][k]
                T += Wins[i][j][k]
    print('w_list = ', w_list)
    
    for i in range(len(Losses)):
        for j in range(len(Losses[i])):
            for k in range(len(Losses[i][j])):
                l_list[k] += Losses[i][j][k]
                T += Losses[i][j][k]
    print('l_list = ', l_list)

    #Calculating W_d
    Wd = [0] * (n+1)
    Wd_best = 0
    d_best = 0
    for i in range(len(Wd)):
        Wd[i] = w_list[i]/(w_list[i]+l_list[i])
        if(Wd[i] > Wd_best):
            Wd_best = Wd[i]
            d_best = i
    print('Wd = ', Wd)
    print('Wd_best = ', Wd_best)
    print('d_best = ', d_best)
    print('T = ', T)

    #Calculating P values: 
    P_best = ((T*Wd_best)+M) / ((T*Wd_best)+(n*M))
    print('P_best = ', P_best)

    s = 0
    for i in range(len(Wd)):
        if i!=0 and i!=d_best:
            s += Wd[i]
    print('s = ', s)

    P_other = []
    for i in range(len(Wd)):
        if i!=0 and i!=d_best:
            temp = ((1-P_best)*(T*Wd[i] + M))/(s*T + (n-1)*M)
            P_other.append(temp)
    print('P_other = ', P_other)

    P_final = []
    P_final.append(P_other)
    P_final.append(P_best)
    print('Final probability set: ', P_final)
'''
    
def play_game(NS, ND, H, L, Wins, Losses, M):
    scores = [0, 0]
    current_player = 0
    winner_player = 0
    temp0 = np.zeros((L+1, L+1, ND+1))                  #temp0 holds scores of player 1 and later assigned to Win/Loss tensors based on who wins
    temp1 = np.zeros((L+1, L+1, ND+1))                  ##temp1 holds scores of player 2 and later assigned to Win/Loss tensors based on who wins

    t0 = []
    t1 = []

    while True:
        dice_to_roll = max(1, random.randint(1, ND))
        roll_sum = sum(random.randint(1, NS) for _ in range(dice_to_roll))

        if(current_player == 0):
            temp0[scores[0], scores[1], dice_to_roll] +=1
            t0.append([scores[0], scores[1],dice_to_roll])
        elif (current_player == 1):
            temp1[scores[1], scores[0], dice_to_roll] +=1
            t1.append([scores[1], scores[0], dice_to_roll])
        
        scores[current_player] += roll_sum
        
        if scores[current_player] > H:
            #Losses[0, scores[0], dice_to_roll] += 1
            #Wins[scores[1], scores[0], dice_to_roll] += 1
            winner_player = (current_player + 1) % 2
            break
        elif L <= scores[current_player] <= H:
            #Wins[scores[0], scores[1], dice_to_roll] += 1
            winner_player = current_player
            break

        current_player = (current_player + 1) % 2

    #print(t0)
    if winner_player == 0:
        for m in range(len(t0)):
            s1,s2,d = t0[m]
            Wins[s1][s2][d] += 1
        for m in range(len(t1)):
            s1,s2,d = t1[m]
            Losses[s1][s2][d] += 1
    elif winner_player == 1:
        for m in range(len(t0)):
            s1,s2,d = t0[m]
            Losses[s1][s2][d] += 1
        for m in range(len(t1)):
            s1,s2,d = t1[m]
            Wins[s1][s2][d] += 1
    '''
    if winner_player == 0:
        #copy entries of temp0 to WIN[] & entries of temp1 to LOSS[]
        for i in range(len(temp0)):
            for j in range(len(temp0[i])):
                for k in range(len(temp0[i][j])):
                    Wins[i][j][k] += temp0[i][j][k]
        for i in range(len(temp1)):
            for j in range(len(temp1[i])):
                for k in range(len(temp1[i][j])):
                    Losses[i][j][k] += temp1[i][j][k]
    elif winner_player == 1:
        #copy entries of temp1 to WIN[] & entries of temp0 to LOSS[]
        for i in range(len(temp1)):
            for j in range(len(temp1[i])):
                for k in range(len(temp1[i][j])):
                    Wins[i][j][k] += temp1[i][j][k]
        for i in range(len(temp0)):
            for j in range(len(temp0[i])):
                for k in range(len(temp0[i][j])):
                    Losses[i][j][k] += temp0[i][j][k]
    '''
    return Wins, Losses

def train_model(NS, ND, H, L, G, M):
    if G < 1 or M < 0 or NS <= 1 or ND <= 1 or H < L:
        raise ValueError("Invalid parameters.")

    Wins, Losses = initialize_tables(L, ND)

    for _ in range(G):
        Wins, Losses = play_game(NS, ND, H, L, Wins, Losses, M)

    return Wins, Losses

def calculate_win_probabilities(Wins, Losses):
    probabilities = Wins / (Wins + Losses)
    return probabilities

def main():
    parser = argparse.ArgumentParser(description="Train a model to play a dice game.")
    parser.add_argument("-NS", type=int, help="Number of sides on each die")
    parser.add_argument("-ND", type=int, help="Max number of dice to choose from")
    parser.add_argument("-H", type=int, help="High winning score (inclusive)")
    parser.add_argument("-L", type=int, help="Low winning score (inclusive)")
    parser.add_argument("-G", type=int, help="Number of games to train against")
    parser.add_argument("-M", type=int, help="Exploitation vs. exploration parameter")
    parser.add_argument("-v", type=int, help="Verbose mode")
    args = parser.parse_args()
    verb = 0
    NS, ND, H, L, G, M = args.NS, args.ND, args.H, args.L, args.G, args.M
    verb = args.v
    try:
        Wins, Losses = train_model(NS, ND, H, L, G, M)
        #calcDiceProb(Wins, Losses, ND, M)

        #Calculating optimal dice table & corresponding values:
        res = [["" for _ in range(L+1)] for _ in range(L+1)]

        for i in range(len(Wins)):
            for j in range(len(Wins[i])):
                temp = -math.inf
                d_no = -1
                res[i][j] = "n/a"
                flag = 0

                Wd = [0] * (ND+1)
                Wd_best = -1
                d_best = -1
                T = 0

                for k in range(len(Wins[i][j])):
                    T += Wins[i][j][k] + Losses[i][j][k]
                    if( Wins[i][j][k]==0 and Losses[i][j][k]==0 ):
                        continue
                    Wd[k] = (Wins[i][j][k] / (Wins[i][j][k] + Losses[i][j][k]))     #calculating Wd for all 'k'/ND values across each game state/episode: [A,B,k]
                    if(Wd[k] > Wd_best):
                        Wd_best = Wd[k]
                        d_best = k
                    flag = 1
                if verb:
                    print('Wd/Wd_best/d_best = ', Wd, Wd_best, d_best)
                P_best = ((T*Wd_best)+M) / ((T*Wd_best)+(ND*M))
                if verb:
                    print('P_best = ', P_best)

                s = 0
                for i1 in range(len(Wd)):
                    if i1!=0 and i1!=d_best:
                        s += Wd[i1]
                if verb:
                    print('s = ', s)

                P_other = []
                #P_all = [0] * (ND+1)
                #P_all[d_best] = P_best
                
                for i2 in range(len(Wd)):
                    if i2!=0 and i2!=d_best:
                        temp = ((1-P_best)*(T*Wd[i2] + M))/(s*T + (ND-1)*M)
                        P_other.append(temp)
                        #P_all[i2] = temp
                if verb:
                    print('P_other = ', P_other)
                    #print('P_all', P_all)

                rand_d = max(1, random.randint(1, ND))                      #random.choices() to select dice based on these P_d probabilities
                if flag != 0:
                    res[i][j] = str(rand_d) + ":" + str(round(Wd[rand_d],3))
                if verb:
                    print('---------------------------------------------------------------------------------')
            res[i].pop()
        for i in range(L):
            print(i, end="          ")
        print('\n')
        for i in range(len(res)-1):
            print(str(i), end=" ")
            print(res[i])

    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
