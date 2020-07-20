import numpy as np
from Setup import Transportation

class GlobalMinimum:

    def __init__(self, trans):

        self.trans = trans
        self.table = trans.table.copy()
        self.alloc = []

    def allocation(self, x, y):
        
        mins = min([self.table[x, -1], self.table[-1, y]])
        self.alloc.append([self.table[x, 0], self.table[0, y], mins])
        
        if self.table[x, -1] < self.table[-1, y]:
            #delete row and supply x then change value of demand y
            self.table = np.delete(self.table, x, 0)
            self.table[-1, y] -= mins
            
        elif self.table[x, -1] > self.table[-1, y]:
            #delete column and demand y then change value of supply x
            self.table = np.delete(self.table, y, 1)
            self.table[x, -1] -= mins
            
        else:
            #delete row and supply x, column and demand y
            self.table = np.delete(self.table, x, 0)
            self.table = np.delete(self.table, y, 1)

    def solve(self, show_iter=False):

        #multiply cost with it's minimum supply / demand
        n, m = [i - 2 for i in self.table.shape]
        supply = self.table[1:-1, -1]
        demand = self.table[-1, 1:-1]
        for i in range(n):
            for j in range(m):
                mins = min([supply[i], demand[j]])
                self.table[i + 1, j + 1] *= mins

        if show_iter:
            self.trans.print_frame(self.table)

        while self.table.shape != (2, 2):


            cost = self.table[1:-1, 1:-1]

            #finding index of minimum cost
            x, y = np.argwhere(cost == np.min(cost))[0]
            
            #allocated row x to column y or vice versa
            self.allocation(x + 1, y + 1)

            #print table
            if show_iter:
                self.trans.print_frame(self.table)
            
        return np.array(self.alloc, dtype=object)


if __name__ == "__main__":

    #example 1 balance problem
    cost = np.array([[15, 4, 6, 15],
                    [5, 2, 15, 4],
                    [6, 5, 3, 14]])
    supply = np.array([70, 47, 33])
    demand = np.array([52, 78, 15, 5])

    #example 2 unbalance problem
    cost = np.array([[ 6,  1, 9, 3],
                    [11,  5, 2, 8],
                    [10, 12, 4, 7]])
    supply = np.array([70, 55, 70])
    demand = np.array([85, 35, 50, 45])

    #initialize transportation problem
    trans = Transportation(cost, supply, demand)

    #setup transportation table.
    #minimize=True for minimization problem, change to False for maximization, default=True.
    #ignore this if problem is minimization and already balance
    trans.setup_table(minimize=True)

    #initialize global minimum method with table that has been prepared before.
    GM = GlobalMinimum(trans)

    #solve problem and return allocation lists which consist n of (Ri, Cj, v)
    #Ri and Cj is table index where cost is allocated and v it's allocated value.
    #(R0, C1, 3) means 3 cost is allocated at Row 0 and Column 1.
    #show_iter=True will showing table changes per iteration, default=False.
    allocation = GM.solve(show_iter=False)

    #print out allocation table in the form of pandas DataFrame.
    #(doesn't work well if problem has large dimension).
    trans.print_table(allocation)

#Result from example problem above
'''
example 1 balance problem
            C0     C1     C2    C3 Supply
R0      15(52)  4(18)      6    15     70
R1           5  2(42)     15  4(5)     47
R2           6  5(18)  3(15)    14     33
Demand      52     78     15     5    150

TOTAL COST: 1091

example 2 unbalance problem
            C0     C1     C2     C3 Supply
R0           6  1(35)      9  3(35)     70
R1       11(5)      5  2(50)      8     55
R2      10(60)     12      4  7(10)     70
Dummy    0(20)      0      0      0     20
Demand      85     35     50     45    195

TOTAL COST: 965
'''
