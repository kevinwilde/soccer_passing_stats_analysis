stats = 'book1.txt'

def loadStats(filename):
    inputFile = open(filename)
    playerstats = {}
    count = 1
    for line in inputFile:
        newline = line.split()
        playerstats[newline[0] + str(count)] = (newline[1:])
        count += 1
    for item in playerstats:
        for i in range(7):
            playerstats[item][i] = float(playerstats[item][i])
    return playerstats


def convertToZ(statdict):
    zscores = {}
    for item in statdict:
        zscores[item] = [0, 0, 0, 0, 0, 0, 0]
        #Assists
        zscores[item][0] = (statdict[item][0] - 0.23)/0.58206
##        zscores[item][0] = (statdict[item][0] - 0.23)/100000.0

        #Key Passes per Game
        zscores[item][1] = (statdict[item][1] - 0.821)/0.848859
##        zscores[item][1] = (statdict[item][1] - 0.821)/100000.0

        #Avg number of passes per game
        zscores[item][2] = (statdict[item][2] - 39.9785)/17.75915
##        zscores[item][2] = (statdict[item][2] - 39.9785)/100000.0

        #Pass percentage
        zscores[item][3] = (statdict[item][3] - 80.7045)/10.41959
##        zscores[item][3] = (statdict[item][3] - 39.9785)/100000.0
        
        #accurate crosses per game
        zscores[item][4] = (statdict[item][4] - 0.3495)/0.566927
##        zscores[item][4] = (statdict[item][4] - 0.3495)/100000.0

        #accurate long balls per game
        zscores[item][5] = (statdict[item][5] - 2.4635)/2.347225
##        zscores[item][5] = (statdict[item][5] - 2.4635)/100000.0

        #accurate through balls per game
        zscores[item][6] = (statdict[item][6] - 0.058)/0.196287
##        zscores[item][6] = (statdict[item][6] - 0.058)/100000.0
    return zscores


def diffBetweenPlayers(player1, player2):
    diff = 0
    for i in range(7):
        diff += (player1[i]-player2[i])
    return diff

def clusterAve(cluster, playerdict):
    #cluster is a list
    ave = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        total = 0
        for player in cluster:
            total+= playerdict[player][i]
        ave[i] = total/len(cluster)
    best = 100
    for player in cluster:
        playerdiff = diffBetweenPlayers(playerdict[player], ave)
        if playerdiff < best:
            best = playerdiff
            aveplayer = player
    return aveplayer

    
def makeClusters(k, maxMovers, statdict):
    import random
    centroids = []
    clusters = []
    for i in range(k):
        centroidChoice = random.choice(statdict.keys())
        centroids.append(centroidChoice)
        clusters.append([centroidChoice])
##    print centroids
####    print clusters
    movers = 200
    while movers >= maxMovers:
        movers = 0
        for player in statdict:
            diffs = []
            for centroid in centroids:
                diffs.append(abs(diffBetweenPlayers(statdict[player], statdict[centroid])))
####                print diffs
            minDiffIndex = diffs.index(min(diffs))
####            print minDiffIndex
            if player not in clusters[minDiffIndex]:
                movers += 1
                for i in range(k):
                    if i!= minDiffIndex:
                        if player in clusters[i]:
                            clusters[i].remove(player)
####                print minDiffIndex
                clusters[minDiffIndex].append(player)
####        print clusters
        for x in range(k):
            centroids[x] = clusterAve(clusters[x], statdict)
##        print centroids
##    print '============================================================'
    return clusters

def loadPlayerDisplay(fileName):
    inputfile = open(fileName)
    d = {}
    count = 0
    for line in inputfile:
        count += 1
        newline = line.split()
        d[newline[0] + str(count)] = ' '.join(newline[1:])
    return d
        
    
def displayClusters(clusters, playerdict):
    for i in range(len(clusters)):
        print 'Cluster #' + str(i+1) + ':'
        for item in clusters[i]:
            print playerdict[item] + ',',
        print
        print
    
zdict = convertToZ(loadStats(stats))
##print zdict
displayClusters(makeClusters(5, 1, zdict), loadPlayerDisplay('playerdisplay.txt'))
