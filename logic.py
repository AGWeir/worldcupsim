from random import randint
import itertools
from prettytable import PrettyTable
import operator

class team:
    def __init__(self, country):
        self.name = country
        self.gp = 0
        self.ptd = 0
        self.gf = 0
        self.ga = 0
        
    def __repr__(self):
        return str(self.name)
    
    def update(self,np,gf,ga):
        #add pts, gf, ga post match
        self.gp = self.gp + 1
        self.ptd = self.ptd + np
        self.gf = self.gf + gf
        self.ga = self.ga + ga
        
def createteams(teams):
    #accepts list of teams as strings
    return [team(x) for x in teams]

def playmatch(team1,team2):
    t1g = randint(0,5)
    t2g = randint(0,5)
    print('Result:',team1,t1g,"-",t2g,team2)
    if t1g > t2g:
        team1.update(3,t1g,t2g)
        team2.update(0,t2g,t1g)
    elif t2g  > t1g:
        team2.update(3,t2g,t1g)
        team1.update(0,t1g,t2g)
    else:
        team1.update(1,t1g,t2g)
        team2.update(1,t2g,t1g)
    
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
    
groupa = [team(x) for x in ['England','Wales','Scotland','Northern Ireland']]

playallmatches(groupa)
