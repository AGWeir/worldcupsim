from random import randint
import scipy.stats as ss
import itertools
from prettytable import PrettyTable
from numpy.random import choice
import csv

class team:
    def __init__(self, country):
        self.name = country[0]
        self.gp = 0
        self.ptd = 0
        self.gf = 0
        self.ga = 0
        self.attstrength = country[1]
        self.defstrength = country[2]
        
    def __repr__(self):
        return str(self.name)
    
    def update(self,np,gf,ga):
        #add pts, gf, ga post match
        self.gp = self.gp + 1
        self.ptd = self.ptd + np
        self.gf = self.gf + gf
        self.ga = self.ga + ga
    
def playallmatches(group):
    pool = tuple(itertools.combinations(group,2))
    for x in pool:
        playmatch(x[0],x[1])
        
    t = PrettyTable(['Team','P','GF','GA','Pts'])
    for x in group:
        t.add_row([str(x),x.gp,x.gf,x.ga,x.ptd])
    
    t.sortby = 'Pts'
    t.reversesort = True
    print(t)
    
def playmatch(team1,team2):
    t1xpg = team1.attstrength * team2.defstrength * 1.18
    t2xpg = team2.attstrength * team1.defstrength * 1.18
    
    t1probs = []
    t2probs = []
    scores = []
    for i in range(0,25):
        t1probs.append(ss.poisson.pmf(i,t1xpg))
        t2probs.append(ss.poisson.pmf(i,t2xpg))

    t1g = choice(range(25), 1, p=t1probs)[0]
    t2g = choice(range(25), 1, p=t2probs)[0]
    result = str(t1g) + "-" + str(t2g)
    print('Result:',team1,result,team2)
    
    if t1g > t2g:
        team1.update(3,t1g,t2g)
        team2.update(0,t2g,t1g)
    elif t2g  > t1g:
        team2.update(3,t2g,t1g)
        team1.update(0,t1g,t2g)
    else:
        team1.update(1,t1g,t2g)
        team2.update(1,t2g,t1g)
        
groupa = [team(x) for x in[['Belgium',1.92,0.41],
                    ['England',1.17,0.55],
                    ['Tunisia',1.22,0.81],
                    ['Panama',0.55,1.17]]]

playallmatches(groupa)
