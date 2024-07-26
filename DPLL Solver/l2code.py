
import argparse
import sys
import re
from collections import OrderedDict

class Tree:
    def __init__(self, children=None):
        self.children = children

    def recurse(self, fn, *args, **args1):
        for c in self.children:
            fn(c, *args, **args1)

    def checkLeaf(self):
        return False

class Binary(Tree):
    def __init__(self, left, right):
        super().__init__(children=[left, right])


class Unary(Tree):
    def __init__(self, operand):
        super().__init__(children=operand)


class Atom(Tree):
    def __init__(self, sym):
        super().__init__()
        self.symbol = sym

    def eval(self, truth_values):
        return truth_values[self.symbol]

    def checkLeaf(self):
        return True


class Biconditional(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.symbol = "<=>"

    def eval(self, val):
        if self.children[0].eval(val) == self.children[1].eval(val):
            return True
        return False


class Implicate(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.symbol = "=>"

    def eval(self, val):
        if self.children[0].eval(val) and not self.children[1].eval(val):
            return False
        return True


class Negate(Unary):
    def __init__(self, opr):
        super().__init__(opr)
        self.symbol = "!"

    def recurse(self, fn, *args, **args1):
        fn(self.children, *args, **args1)

    def eval(self, truth_values):
        return not self.children.eval(truth_values)


class Disjunct(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.symbol = dis

    def eval(self, val):
        return self.children[0].eval(val) or self.children[1].eval(val)


class Conjunct(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.symbol = "&"

    def eval(self, val):
        return self.children[0].eval(val) and self.children[1].eval(val)




def print_cnf(root):
    #print("CNF expressions: ")
    c = root.children

    if root.checkLeaf():
        print(root.symbol, end='')
    elif issubclass(type(root), Unary):
        print(root.symbol, end='')
        print_cnf(c)
    elif re.match("&", root.symbol):
        c0 = root.children[0]
        c1 = root.children[1]
        print_cnf(c0)
        print("\n", end='')
        print_cnf(c1)
    elif re.match(dis, root.symbol):
        c0 = root.children[0]
        c1 = root.children[1]
        print_cnf(c0)
        print("\t", end='')
        print_cnf(c1)

def eliminate_implication(tree, parent):
    if tree.checkLeaf():
        return
    elif imp == tree.symbol:
        current = tree
        eliminate_implication(current.children[0], current)
        eliminate_implication(current.children[1], current)
        child1 = current.children[0]
        child2 = current.children[1]
        parent.children[parent.children.index(current)] = Disjunct(Negate(child1), child2)
    else:
        tree.recurse(eliminate_implication, tree)


def negations_to_atoms(tree, p):
    if tree.checkLeaf():
        return
    elif "!" == tree.symbol:
        if tree.children.checkLeaf():
            return
        if "!" == tree.children.symbol:
            c = tree.children.children
            if type(p) is not Negate:
                p.children[p.children.index(tree)] = c
            tree = c
            if tree.checkLeaf():
                return
        else:
            if "&" == tree.children.symbol:
                c0 = tree.children.children[0]
                c1 = tree.children.children[1]
                new_tree = Disjunct(Negate(c0), Negate(c1))
                p.children[p.children.index(tree)] = new_tree
                tree = new_tree
            elif dis == tree.children.symbol:
                c0 = tree.children.children[0]
                c1 = tree.children.children[1]
                new_tree = Conjunct(Negate(c0), Negate(c1))
                p.children[p.children.index(tree)] = new_tree
                tree = new_tree
        tree.recurse(negations_to_atoms, tree)
    else:
        tree.recurse(negations_to_atoms, tree)


def DistriDisjunc(tree, parent):
    i = 0
    d = False
    if tree.checkLeaf():
        return
    elif tree.symbol == dis:
        tree.recurse(DistriDisjunc, tree)
        for c in tree.children:
            if re.match("&", c.symbol) and type(c) is not str:
                d = True
                break
            i = i + 1
        if d:
            new_tree = Conjunct(Disjunct(tree.children[1 - i], tree.children[i].children[0]), Disjunct(tree.children[1 - i], tree.children[i].children[1]))
            parent.children[parent.children.index(tree)] = new_tree
            tree = new_tree
    else:
        tree.recurse(DistriDisjunc, tree)

def create_tree(final_tok):
    tok = to_prefix(final_tok)[::-1]
    #print('tok after inftoPref', tok)
    def parse_prefix():
        n = None
        if symbol.match(tok[-1]):
            return Atom(tok.pop())
        elif operator.match(tok[-1]):
            op = tok.pop()
            if op == "!":
                n = Negate(parse_prefix())
            else:
                if op == "<=>":
                    n = Biconditional(parse_prefix(), parse_prefix())
                elif op == "=>":
                    n = Implicate(parse_prefix(), parse_prefix())
                elif op == "&":
                    n = Conjunct(parse_prefix(), parse_prefix())
                elif op == dis:
                    n = Disjunct(parse_prefix(), parse_prefix())
            return n
    return parse_prefix()

def to_cnf(exp):
    r = Tree([exp])
    c = r.children[0]
    inorder_traversal(c)
    print("\n")
    eliminate_biconditionals(c, r)
    verbose_mode("After eliminate_biconditionals():")
    inorder_traversal(c)
    print("\n")
    eliminate_implication(c, r)
    verbose_mode("After eliminate_implication():")
    inorder_traversal(c)
    print("\n")
    negations_to_atoms(c, r)
    verbose_mode("After negations_to_atoms():")
    inorder_traversal(c)
    print("\n")
    while not is_cnf(c):
        DistriDisjunc(c, r)
    verbose_mode("After Distributing:")
    inorder_traversal(c)
    print("\n")
    return c


def to_prefix(tokens):
    list_tokens = tokens[::-1]
    prefix = []
    operatorSt = []
    tempC = []
    tempC.append("")
    for tok in list_tokens:
        if symbol.match(tok):
            prefix.append(tok)
        elif not operatorSt and operator.match(tok) :
            operatorSt.append(tok)
        elif operatorSt:
            if rb.match(tok):
                operatorSt.append(tok)
            elif lb.match(tok):
                while operatorSt and not rb.match(operatorSt[-1]):
                    prefix.append(operatorSt.pop())
                if operatorSt:
                    operatorSt.pop()
            elif rb.match(operatorSt[-1]) or precedence[tok] >= precedence[operatorSt[-1]]:
                operatorSt.append(tok)
            else:
                while operatorSt and not rb.match(operatorSt[-1]) and precedence[tok] < precedence[operatorSt[-1]]:
                    prefix.append(operatorSt.pop())
                operatorSt.append(tok)
    while operatorSt:                           #pop remaining items from op stack
        prefix.append(operatorSt.pop())
    return prefix[::-1]


def eliminate_biconditionals(tree, parent):
    if tree.checkLeaf():
        return
    elif re.match("<=>", tree.symbol):
        eliminate_biconditionals(tree.children[0], tree)
        eliminate_biconditionals(tree.children[1], tree)
        parent.children[parent.children.index(tree)] = Conjunct(Implicate(tree.children[0], tree.children[1]), Implicate(tree.children[1], tree.children[0]))
    else:
        tree.recurse(eliminate_biconditionals, tree)

def is_cnf(n):
    ans = True
    if n.symbol == "!" and n.children.checkLeaf():
        return True
    if n.checkLeaf():
        return True
    else:
        if n.symbol == "!":
            return False
        for child in n.children:
            if not child.checkLeaf() and child.symbol == "&" and n.symbol == dis :
                return False
            ans = ans and is_cnf(child)
        return ans

def inorder_traversal(root, level = 0):
    if root.checkLeaf():
        verbose_mode(root.symbol, end=' ')
    elif issubclass(type(root), Unary) == True:             #Root has 1 child
        verbose_mode(root.symbol, end='')
        inorder_traversal(root.children, level=level + 1)
    elif issubclass(type(root), Binary):                                           #Root has 2 child
        if level != 0:
            verbose_mode("(", end='')
        inorder_traversal(root.children[0], level=level+1)
        verbose_mode(root.symbol, end=' ')
        inorder_traversal(root.children[1], level=level+1)
        if level != 0:
            verbose_mode(")", end='')
    else:
        if level != 0:
            verbose_mode("(", end='')
        inorder_traversal(root.children[0], level=level+1)
        verbose_mode(root.symbol, end=' ')
        inorder_traversal(root.children[1], level=level+1)
        if level != 0:
            verbose_mode(")", end='')        



def simplify(clauses, sym, val=True):
    removeList = []
    Lognot = f"!{sym}"
    if not val:
        sym = f"!{sym}"
        rep = sym.replace(f"{neg}", '')
        Lognot = rep
    for i in range(0, len(clauses)):
        if sym in clauses[i]:
            removeList.append(i)
        if Lognot in clauses[i]:
            clauses[i] = clauses[i].difference({Lognot})
    for l, i in enumerate(removeList):          #remove resolved clauses
        verbose_mode(f" {clauses[i - l]} satisfied")
        del clauses[i - l]
    verbose_mode(f"Clauses: {clauses}")
    return clauses

def disp_clauses(clauses):
    for cl in clauses:
        c = []
        for sym in cl:
            c.append(sym)
        verbose_mode(" ".join(c))


def tokenization(t):
    i = 0
    tok = []
    while i < len(t):
        if t[i] == '=' and t[i+1] == '>':
            tok.append(imp)
            i = i + 1
        elif t[i] == '<' and t[i+1] == '=' and t[i+2] == '>':
            tok.append(iff)
            i = i + 2
        elif operator.match(t[i]) or bracs.match(t[i]):
            tok.append(t[i])
        elif symbol.match(t[i]):
            temp = []
            while symbol.match(t[i]):
                temp.append(t[i])
                i = i + 1
            tok.append("".join(temp))
            continue
        i += 1
    return tok

def resolve_dpll(cnf):
    clauses = get_clauses(cnf)
    sD = OrderedDict()

    def getSymbols(cL):
        symbolsSet = set()
        for sym in [symbol for clause in cL for symbol in clause]:
            repNeg = sym.replace("!", '')
            symbolsSet.add(repNeg)
        return symbolsSet

    def dpll_solver(cL, sym):
        while True:
            if len(cL) == 0:
                return True, sym
            disp_clauses(cL)
            for c in cL:
                if len(c) == 0:
                    return False, OrderedDict()
            EC = search_easy_case(cL, sym)
            while EC:
                if "!" not in EC:
                    verbose_mode(f"easyCase: {EC} = True")
                    sym[EC] = True
                else:
                    verbose_mode(f"easyCase: {EC.replace(neg, '')} = False")
                    sym[EC.replace("!", '')] = False
                negRep = EC.replace("!", '')
                cL = simplify(cL, negRep, sym[negRep])
                verbose_mode(f"Truth values: {sym}")
                if len(cL) == 0:
                    return True, sym
                disp_clauses(cL)
                for c in cL:
                    if len(c) == 0:
                        verbose_mode(f"{EC} contradiction")
                        verbose_mode("fail| ", end='')
                        return False, OrderedDict()
                EC = search_easy_case(cL, sym)
            for atom1, v in sym.items():
                if v is None:
                    for guess in [True, False]:
                        verbose_mode(f"Hard case, Let: {atom1} = {guess}")
                        sym[atom1] = guess
                        verbose_mode(f"Truth values: {sym}")
                        answer, solution = dpll_solver(simplify(cL.copy(), atom1, guess),
                                                       sym.copy())
                        if answer:
                            return True, solution
                    if not answer:
                        return False, OrderedDict()
    for s in sorted(getSymbols(clauses)):
        sD[s] = None
    ans, Tval = dpll_solver(clauses, sD)
    if ans:
        for i, j in Tval.items():
            if Tval[i] is None:
                Tval[i] = False
                verbose_mode(f"unbound {i} = {Tval[i]}")
        for i, j in Tval.items():
            print(f"{i} = {Tval[i]}")
        return True
    return False

def get_clauses(exp):
    c = []
    def findliteral(n):
        if n.checkLeaf():
            return [n.symbol]
        elif n.symbol == neg and n.children.checkLeaf():
            return [f"{n.symbol}{n.children.symbol}"]
        else:
            return findliteral(n.children[0]) + findliteral(n.children[1])

    def clause_gen(item1):
        if item1.checkLeaf():
            return
        elif operator.match(item1.symbol):
            if item1.symbol == "&":
                for nodes1 in item1.children:
                    if nodes1.checkLeaf() or nodes1.symbol == dis:
                        c.append(nodes1)
            item1.recurse(clause_gen)

    clause_gen(exp)
    res = []
    for clause in c:
        res.append(set(findliteral(clause)))
    return res


def search_easy_case(cl, sym):
    lit = set([s for clause in cl for s in clause])
    for p in sym.keys():
        if f"!{p}" not in lit and p in lit :         #literal P present but !P absent
            verbose_mode(f"Easy case: {p} = pure literal")
            return p
        if p not in lit and f"!{p}" in lit:
            verbose_mode(f"Easy case: !{p} = pure literal")
            return f"!{p}"
    for c in cl:                    #Finding singletons ie.len = 1
        if len(c) == 1:
            verbose_mode(f"Easy case: {list(c)[0]} = singleton")
            return list(c)[0]
    return None                     # return null if no easy case found

def read_file(file):
    tkns = []
    with open(file) as Fcontents:
        for line in Fcontents.readlines():
            if line == '\n':
                continue
            tkns.append(f"({line.strip()})")
    final_tok = tokenization("&".join(tkns))
    #print('final_tok = ', final_tok)
    return final_tok

def verbose_mode(*arg, **arg1):
    if verbose:
        print(*arg, **arg1)

iff, imp, neg, con, dis = "<=>", "=>", "!", "&", "|"
verbose = False
precedence = {iff: 1, imp: 2, dis: 3, con: 4, neg: 5}
lb = re.compile(r"\(|\[|\{")
rb = re.compile(r"\)|\]|\}")
bracs = re.compile(r"\(|\[|\{|\)|\]|\}")
symbol = re.compile(r"([a-zA-Z0-9]|_)+")
operator = re.compile(f"<=>|=>|!|&|\\|")

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-mode', nargs=1, type=str, required=True)
    arg_parser.add_argument('-v', action='store_true', required=False)
    arg_parser.add_argument('file')
    args = arg_parser.parse_args(sys.argv[1:])
    mode = args.mode[0]
    verbose = args.v
    filename = args.file
    if mode == 'dpll':
        dis = ' '
        operator = re.compile(f"{imp}|{neg}|{con}|{dis}|{iff}")
        precedence = {iff: 1, imp: 2, dis: 3, con: 4, neg: 5}
    
    
    final_tok = read_file(filename)
    
    root = create_tree(final_tok)
    if mode in ['cnf', 'solver']:
        root = to_cnf(root)
        if mode == 'cnf':
            print_cnf(root)
            print()
    if mode in ['solver', 'dpll']:
        resolve_dpll(root)