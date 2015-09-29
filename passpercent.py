#import pylab
import matplotlib.pyplot as plt
#import re


fileinput = open('passpercentwithnames.txt')

lst_passespergame = []
lst_passpercent = []
annotations = []

for line in fileinput:
    data = line.split()
    position = data[0]
    passespergame = float(data[1])
    passpercent = float(data[2])
    lst_passespergame.append(passespergame)
    lst_passpercent.append(passpercent)
    if (passpercent <= 55 or passpercent >= 95 or passespergame >= 78):
        #player = re.split(r'\t+', line.rstrip('\t'))[1]
        player = data[-1]
        annotations.append([position.upper() + '-' + player, passespergame, passpercent])

plt.scatter(lst_passespergame, lst_passpercent)

for ann in annotations:
    #print ann[0], 'x=', ann[1], 'y=', ann[2]
    plt.annotate(ann[0], xy=(ann[1], ann[2]))
    
plt.xlabel('Passes per game')
plt.ylabel('Passing %')
plt.title('Passing % of EPL Players 2013-14')

plt.show()

