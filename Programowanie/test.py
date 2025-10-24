#!usr/bin/env python

import matplotlib.pyplot as plt

x=[n for n in range (1,11)]
y=[2*n for n in x]
z=[3*n for n in x]

plt.scatter(x, y)
plt.scatter(x, z)
plt.show()