import pandas as pd
import numpy as np
import datetime as dt

alldata = pd.read_csv('results.csv')

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

def createteam(teamname):
    atts,defs = getstrengths(teamname)
    newteam = team([teamname,atts,defs])
    return newteam
	
def createteams(teams):
    allteams = []
    for i in teams:
        allteams.append(createteam(i))
    return allteams

def calcstrength(results, team):
    homes = results[results.home_team == team]
    aways = results[results.away_team == team]
    gf = homes.home_score.sum() + aways.away_score.sum()
    ga = homes.away_score.sum() + aways.home_score.sum()
    frames = [homes,aways]
    allgames = pd.concat(frames)
    gp = len(allgames)
    return (gf / gp), (ga / gp)

def getstrengths(team):
	atts, defs = calcstrength(alldata[(alldata['date'].dt.year >= 2017) & (alldata['tournament'] != 'Friendly')],team)
	return atts,defs

def playallmatches(group):
    pool = tuple(itertools.combinations(group,2))
    for x in pool:
        playmatch(x[0],x[1])

    datadict = {'Team' : [str(x) for x in group],
                'P' : [x.gp for x in group],
                'GF' : [x.gf for x in group],
                'GA' : [x.ga for x in group],
                'Pts' : [x.ptd for x in group]}
    #print(datadict)
    table = pd.DataFrame(datadict)
    return table
    
def playmatch(team1,team2):
    t1xpg = team1.attstrength * team2.defstrength
    t2xpg = team2.attstrength * team1.defstrength
    t1probs = []
    t2probs = []
    for i in range(0,50):
        t1probs.append(ss.poisson.pmf(i,t1xpg))
        t2probs.append(ss.poisson.pmf(i,t2xpg))

    t1g = choice(range(50), 1, p=t1probs)[0]
    t2g = choice(range(50), 1, p=t2probs)[0]
    result = str(t1g) + "-" + str(t2g)
    #print('Result:',team1,result,team2)
    
    if t1g > t2g:
        team1.update(3,t1g,t2g)
        team2.update(0,t2g,t1g)
		return 1,0,0
    elif t2g  > t1g:
        team2.update(3,t2g,t1g)
        team1.update(0,t1g,t2g)
        return 0,1,0
    else:
        team1.update(1,t1g,t2g)
        team2.update(1,t2g,t1g)
        return 0,0,1

## Simulate group stages	
groupa = ['Uruguay','Russia','Egypt','Saudi Arabia']
groupb = ['Spain', 'Portugal','Iran','Morocco']
groupc = ['France','Denmark','Peru','Australia']
groupd = ['Croatia','Argentina','Nigeria','Iceland']
groupe = ['Brazil','Switzerland','Serbia','Costa Rica']
groupf = ['Sweden','Mexico','Korea Republic','Germany']
groupg = ['England','Belgium','Tunisia','Panama']
grouph = ['Colombia','Japan','Senegal','Poland']

allgroups = [groupa,groupb,groupc,groupd,groupe,groupf,groupg,grouph]
for g in allgroups:
    gp = createteams(g)
    table = playallmatches(gp)
    t = table.sort_values(by='Pts',ascending=False)
    print(t)

	
## Simulate any match
def simmatch(team1, team2,repeats):
    t1wins = 0
    t2wins = 0
    draws = 0
    for i in range(repeats):
        t1,t2,d = playmatch(createteam(team1),createteam(team2))
        t1wins += t1
        t2wins += t2
        draws += d
    print(team1,":",t1wins)
    print(team2,":",t2wins)
    print("Draws:",draws)
