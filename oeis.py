# Hello and welcome to my python program! My name is Chris Shaw, and at time of writing I am a Masters by research student at UNSW in Sydney, Australia.
# This program computes the optimal link functions for repeat avoidance in double elimination tournaments.
# For more information on what the heck that means, check out my masters thesis! I'll be submitting it in Sept 2022.
# This integer sequence arose out of my research, and I'm very excited to upload my own original work to the OEIS!
# Most of my commenting is being done post-hoc, so it may be a bit all over the place... sorry!
# If you have any questions, I'd love to be contacted at chrisshawau@gmail.com

import math

oeis = [0] # Final output
round = 2 # Round tracker. I know that round is a builtin function in Python and highlights as syntax. It's a variable here. Sorry.
# error = 0 # Debugging variable
depth = 2 # Tracks the maximum possible length of the next term in the sequence. The algorithm is exponential so this variable is required to go beyond about 20 terms in any sort of reasonable time frame.
rewrite = True # Set true to write output to file.

if rewrite:
	outfile = open('oeis.txt','w')

# Assumes round1 > round2
# Returns true if link1 is a child of link2, false otherwise.
def ischild(round1,round2,link1,link2):
	rounddiff = round1-round2
	longlink2 = link2 * (2**rounddiff)
	linkdiff = link1 - longlink2
	return ((linkdiff >= 0) and (linkdiff < 2**rounddiff))

# Assumes round1 > round2
# Returns the round number where link1 and link2 will meet in losers bracket.
def nearestparent(round1,round2,link1,link2):
	rounddiff = round1-round2
	# longlink1 = link1 - (link1 % 2**rounddiff) # I removed this so long ago that I forget why it was here in the first place
	longlink2 = link2 * (2**rounddiff)
	parentround = 0
	while parentround <= round2:
		parent1 = link1 // 2**(round1-parentround)
		parent2 = longlink2 // 2**(round1-parentround)
		#print(round1,round2,link1,link2,longlink2,parent1,parent2) # Debugging statement
		if parent1 == parent2:
			parentround+=1
		else:
			break
	return parentround-1

# Assumes round1 > round2
# Computes the length of the repeat loop for two given link functions.
def distance(round1,round2,link1,link2):
	upperdist = round1-round2
	lowerdist = 0
	if ischild(round1,round2,link1,link2):
		lowerdist = 2*upperdist
	else:
		parentround = nearestparent(round1,round2,link1,link2)
		#print(round1,round2,link1,link2,parentround) # Debugging statement
		dist1 = round1 - parentround
		dist2 = round2 - parentround
		lowerdist = 2*(dist1+dist2-1)
	#print(round1,round2,link1,link2,upperdist,lowerdist) # Debugging statement
	return (upperdist + lowerdist)
	
# Converts integer to binary string
def linkbin(linkint, round):
	return bin(linkint)[2:].zfill(round)

# Round 0 and round 1 are not calculated. Initial conditions are required for calculating future rounds.
print(0, '')
print(1, 0)
if rewrite:
	outfile.write("0 \n")
	outfile.write("1 0\n")

try:
	while round <= 50: # Number of terms to calculate
		step = 2**(round-depth) # Greatly reduces number of link functions required to check
		conflicts = [] # Tracks estimated number of conflicts for each link function
		conflicterrors = [] # Tracks whether truncation errors were found in floating point arithmetic.
		for i in range(0,2**round,step):
			distances = [] # Tracks the length of the repeat loop to each other link function
			errorflag = False # Used to check for truncation errors in the floating point arithmetic
			for j in range(round-1):
				distances.append(distance(round,j+1,i,oeis[j]))
			total = 0
			for k in distances:
				check = total
				# if total > 0: # Old debugging section
					# curerror = int(math.log2(total)) + k
					# if curerror > error:
						# error = curerror
						# print("New error %d" % error)
				total += 1.0/(2**k) # Number of expected conflicts for each repeat loop is 1/2^(loop length)
				if total == check:
					errorflag = True
			total *= 2**round
			conflicts.append(total)
			conflicterrors.append(errorflag)
			#print(round, linkbin(i,round), total, errorflag)
		checkindex = conflicts.index(min(conflicts))
		oeis.append(step*conflicts.index(min(conflicts)))
		linkbinary = linkbin(oeis[-1], round)
		print(round, linkbinary, conflicterrors[checkindex])
		# for i in range(len(conflicts)): # Used to manually check for well-definedness
			# if conflicts[i] == conflicts[checkindex]:
				# print(linkbin(i*step, round))
		if rewrite:
			outfile.write(str(round) + ' ' + str(linkbinary) + '\n')
		#print(conflicts)
		round += 1
		if linkbinary[depth-1] == '1':
			depth += 1

except KeyboardInterrupt:
	pass

print(oeis)
if rewrite:
	outfile.write(str(oeis))
	outfile.close()

