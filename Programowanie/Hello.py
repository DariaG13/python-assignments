#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

print("Hello world!")

x=np.linspace(0,2*np.pi,100)
y=np.sin(x)
plt.plot(x,y)
plt.show()