#Pranav Thorat pat9991

import sys
import argparse
import json
import random

class HillClimbingSolver:
    def __init__(self, problem_type, size, count):
        self.problem_type = problem_type
        self.size = size
        self.count = count
        self.ini_state_nQ = 1
        self.ini_state_KS = 1
    
    def calcRemainingVal(self, bag):    #Returns: T - sum of values of items in the bag currently
        sum = 0
        for i in range(len(bag)):
            sum = sum + (bag[i]*values[i])
        return T - sum

    def getItemNames(self, lst):        #Returns Item names ('A','B',etc.) based on its equivalent 0/1 array
        alphabet_list = [chr(ord('A') + i) for i in range(26)]
        new_alpha = []
        for i in range(len(lst)):
            if lst[i] == 1:
                new_alpha.append(alphabet_list[i])
        return new_alpha
    
    def checkAll0(self, l):
        for i in range(len(l)):
            if l[i] == 1:
                return 1
        return 0
    def initialize_state(self):
        if self.problem_type == 'queens':
            if(self.ini_state_nQ == 1):
                self.ini_state_nQ = 0
                if opt_verb:
                    print('Starting with: ',list(i for i in range(self.size)))
                return list(i for i in range(self.size))
            unique_integers = list(range(self.size))
            random.shuffle(unique_integers)
            if opt_verb:
                print('Choose: ',unique_integers, ' = ', self.evaluate_queens(unique_integers))
            self.count = self.count+1
            #print('count = ',self.count)
            return unique_integers
        elif self.problem_type == 'knapsack':
            if(self.ini_state_KS == 1):
                self.ini_state_KS = 0
                
                if(len(Start) == 0):
                    print('Start = ', self.getItemNames([0 for _ in range(self.size)]),' = ',self.evaluate())
                    return [0 for _ in range(self.size)]
                
                l = []
                
                l = [0 for _ in range(self.size)]
                j = 0
                for i in range(self.size):
                    if i==(ord(Start[j])-65):
                        l[i] = 1
                        j = j+1
                        if(j == len(Start)):
                            break
                    else:
                        l[i] = 0
                if opt_verb:
                    print('Start: ', self.getItemNames(l), "=", self.evaluate(l))
                return l
                    
            self.count = self.count+1
            
            l = [random.randint(0, 1) for _ in range(self.size)]
            if self.checkAll0(l) == 1:
                if opt_verb:
                    print('Choose: ',self.getItemNames(l)," = ",self.evaluate(l))
                    print(self.getItemNames(l), ' = ', self.calcRemainingVal(l))
                return l
            else:
                return self.initialize_state()
            

    def evaluate(self, state):
        if self.problem_type == 'queens':
            return self.evaluate_queens(state)
        elif self.problem_type == 'knapsack':
            return self.evaluate_knapsack(state)

    def evaluate_queens(self, state):
        conflicts = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if state[i] == state[j] or abs(i - j) == abs(state[i] - state[j]):
                    conflicts += 1
        return -conflicts  # Negative value because we want to maximize

    def evaluate_knapsack(self, state):
        total_value = sum(state[i] * values[i] for i in range(self.size))
        total_weight = sum(state[i] * weights[i] for i in range(self.size))
        if total_weight > capacity or total_value < T:
            return ((total_weight-capacity) + (T-total_value))*(-1)
            # Penalize if weight exceeds capacity or if current total value is < target value T
        else:
            return total_value

    def hill_climbing(self, max_restarts=10):
        current_state = self.initialize_state()
        current_value = self.evaluate(current_state)
        num_restarts = 0
        num_side = 0
        sideways_chosen = False
        #while num_restarts < max_restarts:
        while 1:
            neighbors = self.generate_neighbors(current_state)
            next_state, next_value = self.choose_best_neighbor(neighbors)

            if sideways_chosen == True and next_value > current_value:
                num_side = 0 #If the previous state was taken by a sideways movement, and still if the next neighbor is better in terms of error
                #ie. we are going downhill, safe to reset the num_sideways counter. 
                sideways_chosen = False

            if next_value <= current_value:
                if next_value == current_value:
                    sideways_moves = [neighbor for neighbor in neighbors if self.evaluate(neighbor) == current_value]
                    
                    if sideways_moves and num_side < max_S:
                        if opt_verb:
                            print('%% Moving Sideways %%')#, sideways_moves)
                        num_side = num_side + 1
                        sideways_chosen = True
                        next_state = random.choice(sideways_moves)
                        next_value = current_value
                        if opt_verb:
                            print('Sideway state: ',next_state)
                    else:
                        
                        #In case all sideways motion limit is exhausted!
                        current_state = self.initialize_state()
                        current_value = self.evaluate(current_state)
                        if num_restarts > max_restarts:
                            break
                        continue
                else:
                    # Local maximum reached: Restart!
                    if opt_verb:
                        print('%% RESTARTING SEARCH %%')
                    num_restarts += 1
                    current_state = self.initialize_state()
                    current_value = self.evaluate(current_state)
                    if num_restarts > max_restarts:
                        break
                    continue

            current_state = next_state
            current_value = next_value

            if opt_verb and problem_type=='knapsack':
                print('Choose = ', self.getItemNames(current_state), ' = ',self.evaluate(current_state))
            if opt_verb and problem_type=='queens':
                print('Choose = ', (current_state), ' = ',self.evaluate(current_state))
            if self.is_solution(current_state):
                return current_state

        return None

    def generate_neighbors(self, state):    #Generate neighbors primarily by swapping
        if self.problem_type == 'queens':
            neighbors = []
            for i in range(self.size):
                for j in range(i, self.size):
                    if(state[i] != state[j]):
                        neighbor = list(state)
                        temp = neighbor[i]
                        neighbor[i] = neighbor[j]
                        neighbor[j] = temp
                        neighbors.append(neighbor)
                        if opt_verb:
                            print('N', neighbor, '=', self.evaluate_queens(neighbor))
            return neighbors
        elif self.problem_type == 'knapsack':
            
            cc = 0
            neighbors = []
            state_temp = state
            for i in range(self.size):
                for j in range(i+1, self.size):
                    if(state[i] != state[j]):
                        neighbor = list(state)
                        temp = neighbor[i]
                        neighbor[i] = neighbor[j]
                        neighbor[j] = temp
                        neighbors.append(neighbor)
                        if opt_verb:
                            print(self.getItemNames(neighbor),"=", self.evaluate(neighbor))
            state1 = state
            for i in range(self.size):
                if state1[i] == 0:
                    state1[i] = 1
                    for i in range(self.size):
                        for j in range(i+1, self.size):
                            if(state1[i] != state1[j]):
                                neighbor = list(state1)
                                temp = neighbor[i]
                                neighbor[i] = neighbor[j]
                                neighbor[j] = temp
                                neighbors.append(neighbor)
                                if opt_verb:
                                    #print('N2=', neighbor, '=', self.evaluate(neighbor))
                                    print(self.getItemNames(neighbor),"=", self.evaluate(neighbor))
                                #print(self.getItemNames(neighbor))
                    break
            return neighbors

    def choose_best_neighbor(self, neighbors):
        best_neighbor = None
        best_value = float('-inf')
        for neighbor in neighbors:
            value = self.evaluate(neighbor)
            if value > best_value:
                best_neighbor = neighbor
                best_value = value
        return best_neighbor, best_value

    def is_solution(self, state):
        if self.problem_type == 'queens':
            return self.evaluate(state) == 0
        elif self.problem_type == 'knapsack':
            #print('in is_soln = ', state, ' =', self.evaluate(state), ' ',sum(state[i] * weights[i] for i in range(self.size)))
            return (self.evaluate(state) >= T) and ((sum(state[i] * weights[i] for i in range(self.size))) <= M)

parser = argparse.ArgumentParser()

parser.add_argument('--file', type=str, required=False)
parser.add_argument('--R', type=str, required=False, default=0)
parser.add_argument('--type', type=str, required=True)
parser.add_argument('--S', type=str, required=False, default=0)
parser.add_argument('--opt_verb', type=str, required=False, default=False)
parser.add_argument('--nQ', type=str, required=False, default=8)
args = parser.parse_args()

problem_type = args.type
opt_verb = args.opt_verb

if problem_type!="queens" and problem_type!="knapsack":
    print("Invalid input! type should be queens or knapsack")
    sys.exit()
'''
if((args.R).isnumeric() == False):
    print("Max restarts allowed R: should be a number!")
    sys.exit()

if((args.S).isnumeric() == False):
    print("Max sideways movement allowed S: should be a number!")
    sys.exit()
'''
try:
    max_R = int(args.R)
except ValueError:
    print ("Provided R value cannot be converted to an integer")
    sys.exit()

#max_R = int(args.R)
try:
    max_S = int(args.S)
except ValueError:
    print ("Provided S value cannot be converted to an integer")
    sys.exit()



if problem_type == 'knapsack':
    try:
        f = open(args.file, "r")
    except OSError:
        print ("Could not open/read file:", args.file)
        print("Check if file exists and is in the right path")
        sys.exit()

    cont = f.read()
    if opt_verb:
        print('Contents of file: ', cont)

    data = json.loads(cont)

    T = data["T"]
    M = data["M"]
    Start = data["Start"]
    Items = data["Items"]
    weights = []
    values = []

    for i in range (len(Items)):
        weights.append(Items[i]["W"])
        values.append(Items[i]["V"])

    capacity = M

    solver = HillClimbingSolver(problem_type, len(weights), 0)
    solution = solver.hill_climbing(max_R)
    #print('wts = ', weights)
    #print('values = ', values)
    if solution:
        print("Found solution for knapsack:", solver.getItemNames(solution))
        print("Discovered solution's value = ", (sum(solution[i] * values[i] for i in range(len(solution)))))
        print("Discovered solution's weight = ", (sum(solution[i] * weights[i] for i in range(len(solution)))))
    else:
        print("Failed to find solution for knapsack")

elif problem_type == 'queens':
    board_size = int(args.nQ)
    solver = HillClimbingSolver(problem_type, board_size, 0)
    solution = solver.hill_climbing(max_R)

    if solution:
        print("Found solution for N-queens:", solution, ' Conflicts= ', solver.evaluate_queens(solution))
    else:
        print("Failed to find solution for N-queens")

#---------------------------------------------------------------------------------------------------------------