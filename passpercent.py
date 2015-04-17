import pylab
import matplotlib
fileinput = open('passpercent.txt')
lst = []
for line in fileinput:
    lst.append(float(line))
matplotlib.pyplot.scatter(range(1, 201), lst)
pylab.show()
