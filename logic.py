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
