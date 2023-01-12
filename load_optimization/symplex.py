from scipy.optimize import linprog

class Simplex():
    def __init__(self) -> None:
        pass


    def optimize(self, c, A_eq, b_eq, bounds, integrality):
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs', integrality=integrality)

        print("Maximizing value : ", res.fun)
        print("Optimal solution : ", res.x)
        print("\n")

        return res.x