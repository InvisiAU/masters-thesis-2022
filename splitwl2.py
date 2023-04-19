matchfile = open('../Other data files/Melee matches2.csv','r')
winnerfile = open('../other data files/Melee winners3.csv','w')
loserfile = open('../Other data files/Melee losers3.csv','w')

matchfile.readline()

match = matchfile.readline()
winnerfile.write('ID,MatchID,EventID,Date,Characters,Matchup')
loserfile.write('ID,MatchID,EventID,Date,Characters,Matchup')

testchars = ["Fox","Marth","Falco","CaptainFalcon","Peach","Jigglypuff","Sheik"]
testchars2 = ["Pichu", "Mewtwo"]

i = 0
while match:
	match = match.split(',')
	if match[3] and match[4]:
		winnerchars = match[5][1:-1]
		loserchars = match[6][1:-1]
		if winnerchars and loserchars:
			winnerchars = winnerchars.split(';')
			loserchars = loserchars.split(';')
			if len(winnerchars + loserchars) == 2:
				if winnerchars[0] in testchars and loserchars[0] in testchars:
					winnerfile.write('\n' + ','.join([match[3],match[0],match[1],match[2],winnerchars[0],(winnerchars[0]+';'+loserchars[0])]))
					loserfile.write('\n' + ','.join([match[4],match[0],match[1],match[2],loserchars[0],(loserchars[0]+';'+winnerchars[0])]))
				elif (winnerchars[0] not in testchars2) and (loserchars[0] not in testchars2):
					winnerfile.write('\n' + ','.join([match[3],match[0],match[1],match[2],winnerchars[0],'']))
					loserfile.write('\n' + ','.join([match[4],match[0],match[1],match[2],loserchars[0],'']))
				else:
					winnerfile.write('\n' + ','.join([match[3],match[0],match[1],match[2],'','']))
					loserfile.write('\n' + ','.join([match[4],match[0],match[1],match[2],'','']))
			else:
				winnerfile.write('\n' + ','.join([match[3],match[0],match[1],match[2],'','']))
				loserfile.write('\n' + ','.join([match[4],match[0],match[1],match[2],'','']))
		else:
			winnerfile.write('\n' + ','.join([match[3],match[0],match[1],match[2],'','']))
			loserfile.write('\n' + ','.join([match[4],match[0],match[1],match[2],'','']))
		i+=1
	match = matchfile.readline()
print(i)