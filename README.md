# Global-Minimum-Method--GMM-
 A method for solving Transportation Problem

Global Minimum's Algorithm
1. For every cell (i, j) in the transportation tableau calculate a cost c'ij = min(si, dj) x cij.
2. Select the cell (i, j) with the minimum c'ij.
3. Set xij = min(si, dj).
4. Cross out row i or column j and reduce the supply or demand of the non-crossed-out row or column by the value of xij.
5. Repeat steps 2, 3, and 4 until there is no cell to allocate

Source: Y. Harrath dan J. Kaabi, "New Heuristic to generate an initial basic feasible solution for the balanced transportation problem", International Journal of Industrial and System Engineering vol. 30, no. 2, pp. 193-204, 2018.
