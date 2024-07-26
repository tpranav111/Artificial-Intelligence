#AI LAB-3 : pat9991
import sys
import re
from collections import defaultdict
import node

verb = True
debug = True

def add_node(nName, node_list):
    if nName not in node_list:
        newNode = node.Node(nName)
        node_list[newNode.name] = newNode
    return node_list

def dispNode(NL = {}):
    for k,v in NL.items():
        #print('For node ', k, ' :')
        print('|name:', v.name, '|isChance:', v.isChance, '|isDesc:', v.isDecision, '|isTerm:', v.isTerminal,
            '|Val:', v.value, '|Rew:', v.rew, '|Edges:', v.edges, '|Prob:', v.prob, '|Pol:', v.cur_policy)

def getNextSetVal(nodes = {}, tolerance=0.01, df = 1.0):
    flag = 0
    ans = {}
    ans = dict(nodes)
    temp_dict = {}
    temp_dict1 = {}
    for k,v in nodes.items():
        temp_dict[nodes[k].name] = nodes[k].value
    for k,v in nodes.items():
        if v.isDecision:
            prob = v.prob[0]
            rem_prob = 0
            if (len(v.edges)-1) != 0:
                rem_prob = (1 - prob)/(len(v.edges)-1)
            sum = 0

            for e in v.edges:
                if e == v.cur_policy:
                    sum += prob*nodes[e].value
                else:
                    sum += rem_prob*nodes[e].value
            
            temp_dict1[v.name] = v.rew + (sum*df)
            '''
            for e in v.edges:
                if e!=v.cur_policy:
                    sum = sum + nodes[e].value
            sum = sum*rem_prob
            '''
            #print('sum = ', sum)
            #print ('desc=============',nodes[k].name, nodes[k].value, v.reward + (sum+(prob*nodes[v.cur_policy].value)))
            #temp_dict1[v.name] = v.reward + (sum+(prob*nodes[v.cur_policy].value))
            #print('nl1[v.name].value =', nl1[v.name].value)
        elif v.isTerminal:
            temp_dict1[v.name] = v.rew
        else:
            sum = 0
            for i in range(0, len(v.edges)):
                sum = sum + (v.prob[i] * nodes[v.edges[i]].value)
            #print ('chance=============', nodes[k].value, v.reward + sum)
            #print('sum = ', sum)
            temp_dict1[v.name] = v.rew + (sum*df)
    '''
    for k,v in ans.items():
        print('nl1 node:value = ', ans[k].name, ans[k].value)

    for k,v in nodes.items():
        print('nl node:value = ', nodes[k].name, nodes[k].value)
    
    for k,v in nl.items():
        print('abs(nl1[k].value - nl[k].value) = ', abs(ans[k].value - nodes[k].value) )
        if(abs(ans[k].value - nodes[k].value) > tolerance):
            flag = 1
            break
    '''
    '''
    for k1, v1 in temp_dict.items():
        print(k1,':',v1)

    for k1, v1 in temp_dict1.items():
        print(k1,':',v1)
    '''
    for k in temp_dict1.keys():
        #print('abs(nl1[k].value - nl[k].value) = ', abs(ans[k].value - temp_dict[k]) )
        if(abs(temp_dict1[k] - temp_dict[k]) > tolerance):
            flag = 1
            for key, val in ans.items():
                ans[key].value = temp_dict1[key]
            return ans, flag
    
    for key, val in ans.items():
        ans[key].value = temp_dict1[key]
        #print(ans[key].name, '::ans::', ans[key].value)
    return ans, flag
    for k,v in ans.items():
        #print('abs(nl1[k].value - nl[k].value) = ', abs(ans[k].value - temp_dict[k]) )
        if(abs(ans[k].value - temp_dict[k]) > tolerance):
            flag = 1
            break
    return ans, flag

def updatePolicy(NL, min_pol):           #consider case of self trans
    #print('min_pol = ', min_pol)
    nameList = NL.keys()
    for i in nameList:
        if NL[i].isDecision:
            prob = NL[i].prob[0]
            rem_prob = 0
            if len(NL[i].edges)-1 != 0:
                rem_prob = (1 - prob)/(len(NL[i].edges)-1)
            max = NL[i].value
            for e in NL[i].edges:
                sum = 0
                eM = e
                for e1 in NL[i].edges:
                    if e1 == eM:
                        sum += NL[eM].value*prob
                    else:
                        sum += NL[e1].value*rem_prob
                if min_pol == False:
                    if(max < sum):
                        max = sum
                        NL[i].cur_policy = eM
                elif (sum < max):
                    max = sum
                    NL[i].cur_policy = eM
                
    return NL


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mdp_solver.py <input_file> [-df discount_factor] [-tol tolerance] [-iter max_iterations] [-min True/False]")
        sys.exit(1)

    input_file = sys.argv[1]
    discount_factor = 1.0
    tolerance = 0.01
    max_iter = 100
    min_pol = False
    min_pol_var = "False"

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '-df':
            discount_factor = float(sys.argv[i + 1])
        elif sys.argv[i] == '-tol':
            tolerance = float(sys.argv[i + 1])
        elif sys.argv[i] == '-iter':
            max_iter = int(sys.argv[i + 1])
        elif sys.argv[i] == '-min':
            min_pol_var = sys.argv[i + 1]

    if min_pol_var == "True":
        min_pol = True
    else:
        min_pol = False
    #print(min_pol)

    input_file = open(input_file or "input.txt", "r")
    input_data = input_file.read()

    node_list = {}
    #Get initial/null node list in 'node_list = {}'
    D = input_data
    DS = D.split("\n")
    for i1, line in enumerate(DS):
        line = line.replace("[", " [ ")
        line = line.replace(":", " : ")
        line = line.replace(",", " ")
        line = line.replace("=", " = ")
        line = line.replace("%", " % ")
        line = line.replace("]", " ] ")
        line = line.strip().split()
        if (not line) or (line[0][0] == "#"):
            continue
        line = [float(ival) if ival.replace('.','',1).isdigit() == True else ival for ival in line]    
        l0 = line[0] 
        add_node(l0, node_list)
        newN = node_list[l0]
        if line[1] == "=":
            newN.rew = float(line[2])
        elif line[1] == "%":
            for pVal in line[2:]:
                newN.prob.append(pVal)
        elif line[1] == ":":
            for n1 in line[3:-1]:
                add_node(n1, node_list)
                newN.edges.append(n1)


    kys = node_list.keys()
    for key in kys:
        nd = node_list[key]
        nd.assign_node_type()
    '''
    for k, v in node_list.items():
        print(k, '->', v.print_node())
    '''
    #dispNode(node_list)     #'node_list' is dictionary = pair(key, value of Node object)

    new_NL = node_list
    nl = node_list.copy()
    #dispNode(new_NL)
    #print(node_list['Slow'])
    #for _ in range(0, max_iter):
    #nl, flag = getNextSetVal(nl.copy(), tolerance)
    #    for k,v in nl.items():
    #        print(nl[k].name, ':',nl[k].value)

    currPDict = {}
    count = 0
    while True:
        count = count +1 
        for c, d in nl.items():
            nl[c].value = 0
        for _ in range(0, max_iter):
            nl, flag = getNextSetVal(nl, tolerance, discount_factor)
            if flag == 0:
                break
        #dispNode(nl)

        currPDict = {}
        pflag = 0
        for ky, vl in nl.items():
            currPDict[ky] = nl[ky].cur_policy
        nl = updatePolicy(nl, min_pol)
        for a,b in nl.items():
            if nl[a].cur_policy != currPDict[a]:
                pflag = 1
                break    
        if pflag == 0:
            break

    for k1, v1 in nl.items():
        if v1.isDecision:
            print(v1.name, '->', v1.cur_policy)
    print('\n')
    for k1, v1 in nl.items():
            print(v1.name, '=', v1.value)