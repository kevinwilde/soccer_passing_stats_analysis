NUM_STATS = 7
NUM_PLAYERS = 0

def loadStats(filename):
    inputFile = open(filename)
    playerstats = []
    count = 0
    for line in inputFile:
        arr = line.split()
        if True: #(arr[NUM_STATS] == 'm'):
            playerstats.append(arr[0:NUM_STATS + 1])
            playerstats[count].append(' '.join(arr[NUM_STATS + 1:])) #name
            count += 1
    global NUM_PLAYERS
    NUM_PLAYERS = count
    for i in range(NUM_PLAYERS):
        for j in range(NUM_STATS):
            playerstats[i][j] = float(playerstats[i][j])
    return playerstats

def calcAveAndStDev(playerstats):
    import numpy
    avesAndStDevs = []
    for i in range(NUM_STATS):
        lst = []
        for j in range(NUM_PLAYERS):
            lst.append(playerstats[j][i])
        ave = sum(lst)/NUM_PLAYERS
        stdev = numpy.std(lst)
        avesAndStDevs.append([ave, stdev])
    return avesAndStDevs

def convertToZ(playerstats):
    zscores = []
    avesAndStDevs = calcAveAndStDev(playerstats)
    for i in range(NUM_PLAYERS):
        playerZscores = []
        for j in range(NUM_STATS):            
            playerZscores.append((playerstats[i][j] - avesAndStDevs[j][0]) / avesAndStDevs[j][1])
        zscores.append(playerZscores)
    return zscores


def diffBetweenPlayers(player1, player2):
    diff = 0
    for i in range(NUM_STATS):
        diff += (player1[i]-player2[i])
    return diff


def clusterAve(cluster, playerdict):
    #cluster is a list
    ave = [0] * NUM_STATS
    for i in range(NUM_STATS):
        total = 0
        for playerID in cluster:
            total += playerdict[playerID][i]
        ave[i] = total/len(cluster)
    best = 999
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
        centroidChoice = random.randint(0, NUM_PLAYERS)
        centroids.append(centroidChoice)
        clusters.append([centroidChoice])
##    print centroids
##    print clusters
##    temp = raw_input()
    movers = 200
    while movers >= maxMovers:
        movers = 0
        for player in range(len(statdict)):
            diffs = []
            for centroid in centroids:
                diffs.append(abs(diffBetweenPlayers(statdict[player], statdict[centroid])))
####                print diffs
            minDiffIndex = diffs.index(min(diffs))
####            print minDiffIndex
            if player not in clusters[minDiffIndex]:
                movers += 1
                for i in range(k):
                    if i != minDiffIndex:
                        if player in clusters[i]:
                            clusters[i].remove(player)
                            break
####                print minDiffIndex
                clusters[minDiffIndex].append(player)
##        print clusters
##        temp = raw_input()
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
        
    
def displayClusters(clusters, playerstats):
    for i in range(len(clusters)):
        print 'Cluster #' + str(i+1) + ':'
        for playerID in clusters[i]:
            print playerstats[playerID][NUM_STATS + 1] + ',',
        print
        print

playerstats = loadStats('PlayerStats.txt')          # 'book1.txt'
zdict = convertToZ(playerstats)
displayClusters(makeClusters(5, 1, zdict), playerstats)     #loadPlayerDisplay('playerdisplay.txt'))
