# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("a= ", a)
print("b= ", b)
print("\ninner:", np.inner(a, b))
print("dot:", np.dot(a, b))

# Matrices as ndarray objects
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6, 7], [8, 9, 10]])
print("a", type(a))
print(a)
print("\nb", type(b))
print(b)

# Matrices as matrix objects
c = np.matrix([[1, 2], [3, 4]])
d = np.matrix([[5, 6, 7], [8, 9, 10]])
print("\nc", type(c))
print(c)
print("\nd", type(d))
print(d)
print("\ndot product of two ndarray objects a * b")
print(np.dot(a, b))
print("\ndot product of two matrix objects c * d")
print(np.dot(c, d))