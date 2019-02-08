from csp import *
import math
import time

"""Input: a dictionary with keys every cell index (e.g. if n = 6, 0,1,2,...,35)
   and values a list of all the clique neighbors indexes,
   plus value and operation in clique as 2 last items."""

#1x1
kenken1 = {}
kenken1[0] = [1,'+']

#2x2
kenken2 = {}
kenken2[0] = [1,3,'+']
kenken2[1] = [0,3,'+']
kenken2[2] = [3,3,'+']
kenken2[3] = [2,3,'+']

#3x3
kenken3 = {}
kenken3[0] = [3,3,'+']
kenken3[3] = [0,3,'+']
kenken3[1] = [4,5,'+']
kenken3[4] = [1,5,'+']
kenken3[2] = [1,'+']
kenken3[5] = [8,5,'+']
kenken3[8] = [5,5,'+']
kenken3[6] = [7,4,'+']
kenken3[7] = [6,4,'+']

#4x4
kenken4 = {}
kenken4[0] = [1,8,'*']
kenken4[1] = [0,8,'*']
kenken4[2] = [3,4,'+']
kenken4[3] = [2,4,'+']
kenken4[4] = [5,9,10,'+']
kenken4[5] = [4,9,10,'+']
kenken4[9] = [4,5,10,'+']
kenken4[6] = [7,10,4,'*']
kenken4[7] = [6,10,4,'*']
kenken4[10] = [6,7,4,'*']
kenken4[8] = [1,'+']
kenken4[11] = [14,15,11,'+']
kenken4[14] = [11,15,11,'+']
kenken4[15] = [11,14,11,'+']
kenken4[12] = [13,3,'+']
kenken4[13] = [12,3,'+']

#5x5
kenken5 = {}
kenken5[0] = [5,3,'+']
kenken5[1] = [3,'+']
kenken5[2] = [3,4,9,12,13,14,19,22,23,24,33,'+']
kenken5[3] = [2,4,9,12,13,14,19,22,23,24,33,'+']
kenken5[4] = [2,3,9,12,13,14,19,22,23,24,33,'+']
kenken5[5] = [0,3,'+']
kenken5[6] = [7,8,10,11,15,3000,'*']
kenken5[7] = [6,8,10,11,15,3000,'*']
kenken5[8] = [6,7,10,11,15,3000,'*']
kenken5[9] = [2,3,4,12,13,14,19,22,23,24,33,'+']
kenken5[10] = [6,7,8,11,15,3000,'*']
kenken5[11] = [6,7,8,10,15,3000,'*']
kenken5[12] = [2,3,4,9,13,14,19,22,23,24,33,'+']
kenken5[13] = [2,3,4,9,12,14,19,22,23,24,33,'+']
kenken5[14] = [2,3,4,9,12,13,19,22,23,24,33,'+']
kenken5[15] = [6,7,8,10,11,3000,'*']
kenken5[16] = [17,3,'-']
kenken5[17] = [16,3,'-']
kenken5[18] = [3,'+']
kenken5[19] = [2,3,4,9,12,13,14,22,23,24,33,'+']
kenken5[20] = [21,3,'/']
kenken5[21] = [20,3,'/']
kenken5[22] = [2,3,4,9,12,13,14,19,23,24,33,'+']
kenken5[23] = [2,3,4,9,12,13,14,19,22,24,33,'+']
kenken5[24] = [2,3,4,9,12,13,14,19,22,23,33,'+']



#6x6
kenken6 = {}
kenken6[0] = [6,11,'+']
kenken6[6] = [0,11,'+']
kenken6[1] = [2,2,'/']
kenken6[2] = [1,2,'/']
kenken6[3] = [9,20,'*']
kenken6[9] = [3,20,'*']
kenken6[4] = [5,11,17,6,'*']
kenken6[5] = [4,11,17,6,'*']
kenken6[11] = [5,4,17,6,'*']
kenken6[17] = [5,11,4,6,'*']
kenken6[7] = [8,3,'-']
kenken6[8] = [7,3,'-']
kenken6[10] = [16,3,'/']
kenken6[16] = [10,3,'/']
kenken6[12] = [13,18,19,240,'*']
kenken6[13] = [12,18,19,240,'*']
kenken6[18] = [13,12,19,240,'*']
kenken6[19] = [13,18,12,240,'*']
kenken6[14] = [15,6,'*']
kenken6[15] = [14,6,'*']
kenken6[20] = [26,6,'*']
kenken6[26] = [20,6,'*']
kenken6[21] = [27,28,7,'+']
kenken6[27] = [21,28,7,'+']
kenken6[28] = [21,27,7,'+']
kenken6[22] = [23,30,'*']
kenken6[23] = [22,30,'*']
kenken6[24] = [25,6,'*']
kenken6[25] = [24,6,'*']
kenken6[29] = [35,9,'+']
kenken6[35] = [29,9,'+']
kenken6[30] = [31,32,8,'+']
kenken6[31] = [30,32,8,'+']
kenken6[32] = [30,31,8,'+']
kenken6[33] = [34,2,'/']
kenken6[34] = [33,2,'/']

class Kenken(CSP):

    # variables, domains and neighbors used for csp problem
    variables = []
    domains = {}
    neighbors = {}

    # used for measurements and comparison
    constraint_times_called = 0

    # variable used in constraints function
    assigned = {}

    def __init__(self,grid):
        self.kenken = grid                              # input dictionary grid
        self.n = int(math.sqrt(len(grid)))              # dimension of grid
        self.nn = self.n*self.n                         # number of variables

        self.variables = list(x for x in range(self.nn))            # variables = [0,1,...,n-1]
        for i in self.variables:
            self.domains[i] = list(x+1 for x in range(self.n))      # every variable takes value in [1,n]
        for i in range(self.nn):
            self.neighbors[i] = self.set_neighbors(i)               # setting neighbors. 1)row 2)column 3)clique

        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.kenkenconstraints)

    def set_neighbors(self,index):

        "Generally neighbors are: 1. same column, 2. same row, 3. same clique"

        l = []

        # same column
        k = index-self.n
        while(k >= 0):
            l.append(k)
            k = k-self.n
        k = index+self.n
        while(k < self.nn):
            l.append(k)
            k = k+self.n

        # same row
        k = index-1
        while((int(k/self.n) == int(index/self.n)) and k >= 0):
            l.append(k)
            k = k-1
        k = index+1
        while((int(k/self.n) == int(index/self.n)) and k < self.nn):
            l.append(k)
            k = k+1

        # add clique neighbors
        for x in (self.kenken).get(index)[:-2]:
            if x not in l:  # if already in dont push it again
                l.append(x)

        return l

    # overload display function
    def display(self, assignment):
        print(assignment)
        output = "\n" + self.n*"----------------" + "\n"
        for i in range(self.n):
            output += "|\t"
            for j in range(self.n):
                output += str(assignment.get(i*self.n+j,'.'))+ "\t|\t"
            output += "\n" + self.n*"----------------" + "\n"
        print(output)

    def kenkenconstraints(self,A,a,B,b):

        self.constraint_times_called += 1

        # get current assignments. (used when clique members are more than 2)
        assigned = self.infer_assignment()

        # clique info, from input dictionary (meaning of every item at the beginning of the file)
        cl = (self.kenken).get(A)
        comps = [x for x in cl[:-2]]
        op = cl[-1]
        val = cl[-2]

        # (same column or same row) and (same clique)
        if ((int(A%self.n) == int(B%self.n)) or (int(A/self.n) == int(B/self.n))) and (B in comps):
            # cant have same value in same column or row
            if a == b:
                return False
            else:
                # here we need to be more careful
                if op == '+' or op == '*':
                    return self.add_multiply(A,a,B,b,comps,op,val)
                elif op == '-':
                    if (a - b == val) or (b - a == val):
                        return True
                    else:
                        return False
                elif op == '/':
                    if (a / b == val) or (b / a == val):
                        return True
                    else:
                        return False
        # same column or same row only
        elif (int(A%self.n) == int(B%self.n)) or (int(A/self.n) == int(B/self.n)):
            if a == b:
                return False
            else:
                return True
        # same clique only
        elif B in comps:
            if op == '+' or op == '*':
                return self.add_multiply(A,a,B,b,comps,op,val)
            elif op == '-':
                if (a - b == val) or (b - a == val):
                    return True
                else:
                    return False
            elif op == '/':
                if (a / b == val) or (b / a == val):
                    return True
                else:
                    return False
        return True

    # function used to handle a more complex situation in adding or multiplying
    def add_multiply(self,A,a,B,b,comps,op,val):

        # check if all other clique variables are assigned
        assigned = self.infer_assignment()

        # see how many are assigned and how many are left to assign
        assigned_counter = 0    # number of assigned clique members
        partial_val = 0         # current assigned value
        if op == '+':
            partial_val = 0
            for x in comps:
                if x in assigned and x != B:
                    assigned_counter += 1
                    partial_val += assigned.get(x)
        else:
            partial_val = 1
            for x in comps:
                if x in assigned and x != B:
                    assigned_counter += 1
                    partial_val *= assigned.get(x)

        # all assigned, but only these 2 left
        if assigned_counter == (len(comps)-1):
            if op == '+':
                if partial_val + a + b == val:
                    return True
                else:
                    return False
            else:
                if partial_val * a * b == val:
                    return True
                else:
                    return False
        # more than one variable remains unassigned
        # here we need to ensure that we are lower than the wanted value
        else:
            if op == '+':
                if partial_val + a + b < val:
                    return True
                else:
                    return False
            else:
                if partial_val * a * b < val:
                    return True
                else:
                    return False

        return True


# list of kenken dictionaries
testGrids = [kenken2,kenken3,kenken4,kenken5,kenken6]

for i in range(len(testGrids)):

    test = testGrids[i]

    print("Size = ", i+2)

    #  BT
    start = time.time()
    a = Kenken(test)
    solved = backtracking_search(a) is not None
    #a.display(a.infer_assignment())
    stop = time.time()
    print("\tBT Time: ", stop - start, "Solved? ", solved, " with ", a.nassigns, "assignments", "and ", a.constraint_times_called, "times constraint was called")

    """#  BT + MRV
    start = time.time()
    b = Kenken(test)
    solved = backtracking_search(b, select_unassigned_variable=mrv) is not None
    #b.display(b.infer_assignment())
    stop = time.time()
    print("\tBT + MRV Time: ", stop - start, "Solved? ", solved, " with ", b.nassigns, "assignments", "and ", b.constraint_times_called, "times constraint was called")"""

    #  BT + FC
    start = time.time()
    c = Kenken(test)
    solved = backtracking_search(c, inference=forward_checking) is not None
    #c.display(c.infer_assignment())
    stop = time.time()
    print("\tBT + FC Time: ", stop - start, "Solved? ", solved, " with ", c.nassigns, "assignments", "and ", c.constraint_times_called, "times constraint was called")

    #  BT + FC + MRV
    start = time.time()
    d = Kenken(test)
    solved = backtracking_search(d, select_unassigned_variable=mrv, inference=forward_checking) is not None
    #d.display(d.infer_assignment())
    stop = time.time()
    print("\tBT + FC + MRV Time: ", stop - start, "Solved? ", solved, " with ", d.nassigns, "assignments", "and ", d.constraint_times_called, "times constraint was called")

    #  BT + MAC
    start = time.time()
    e = Kenken(test)
    solved = backtracking_search(e, inference=mac) is not None
    #e.display(e.infer_assignment())
    stop = time.time()
    print("\tBT + MAC Time: ", stop - start, "Solved? ", solved, " with ", e.nassigns, "assignments", "and ", e.constraint_times_called, "times constraint was called")

    """#  min conflicts
    start = time.time()
    e = Kenken(test)
    min_conflicts(e)
    stop = time.time()
    print("\tMINCONFLICTS Time: ", stop - start, "Solved? ", solved, " with ", e.nassigns, "assignments", "and ", e.constraint_times_called, "times constraint was called")"""
