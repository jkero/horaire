import numpy as np

emp = np.array([[0],[1],[2]])
tac = np.array([[0],[1]])

print("\ndot  emp dot * tac")
print(emp * tac)

tac.transpose()
print("-------")

print(emp * tac)