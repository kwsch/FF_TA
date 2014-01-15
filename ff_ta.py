# FF_TA Generator By Kaphotics

# **************************************************** #

# Class Mod Value Retrieve-Table
CLASSMV = {
	#   HP MP AT DE MA RE SP OFFSET
	0: [ 3, 0, 7, 9, 7, 9,11, 9],	# Animist
	1: [11, 0, 7, 9, 7, 9,11, 6],	# Morpher
	2: [ 3, 0, 9, 7, 9, 7,13, 3], 	# Assassin
	3: [ 3, 0, 9, 7, 9, 7,13, 3],	# Ninja
	}
	
CLASSES = {
	0: 'Animist',
	1: 'Morpher',
	2: 'Assassin',
	3: 'Ninja',
	}
	
# **************************************************** #

# Class Verification
	
def verifyclass(classstr,f):
	vv = 0
	if classstr == 'Animist':
		if ((rv[f+1])%100)>9 and ((rv[f+2])%90)>9 and ((rv[f+3])%80)>9 and ((rv[f+4])%70)>13 and ((rv[f+5])%56)>13 and ((rv[f+6])%42)>13 and ((rv[f+7])%28)>13 and ((rv[f+8])%14)<14:
			vv = 1
	elif classstr == 'Morpher':
		if ((rv[f+1])%100)>9 and ((rv[f+2])%90)>9 and ((rv[f+3])%80)>9 and ((rv[f+4])%70)>13 and ((rv[f+5])%56)<14:
			vv = 1
	elif classstr == 'Assassin':
		if ((rv[f+1])%100)>9 and ((rv[f+2])%90)<10:
			vv = 1
	elif classstr == 'Ninja':
		if ((rv[f+1])%100)>7 and ((rv[f+2])%92)<8:
			vv = 1
	else:
		raw_input('Bad ClassSTR')
	return vv

# **************************************************** #

def getinput():
	# Obtain Input Data:
	print "Please Enter your Current Seed in 8 Hex Digit format:"
	seed = int(raw_input(" \-> Seed = 0x"),16)
	
	print "\nPlease Enter The Class Number"
	print "   0 - Animist\n   1 - Morpher\n   2 - Assassin\n   3 - Ninja\n"
	cv = int(raw_input("Class = "))
	
	print "\nPlease Enter The Minimum Desired NetGain"
	netgain = int(raw_input("NetGain = "))
	
	print "\nSearch how many frames forward?"
	srange = int(raw_input("Frames = ").replace(',', ''))+1
	
	global cm
	global classstr
	cm = CLASSMV.get(cv)
	classstr = CLASSES.get(cv)
	
	global text_file 
	text_file = open("FFTA %08X @ %s %d.txt" % (seed,classstr,netgain), "w")
	return (seed,cv,netgain,srange)
	

def operate(seed,cv,netgain,srange,rf):
	# Prepare Variables
	
	# Prepare Text File for Output

	# Populate Random Values, keep Tables
	global rv 
	global rs
	(rv,rs) = populate(seed,srange+500)
	
	# Offset from Frame # to start Stat Calls
	o = cm[7]	
	
	# Loop For Results
	for f in range(1,srange):
	
		global finalseed
		finalf = f
		finalseed = rs[f]
		
		if verifyclass(classstr,f) == 1:
			hpv = ( rv[f+o+2+4*0]%cm[0] + rv[f+o+3+4*0]%cm[0] - rv[f+o+0+4*0]%cm[0] - rv[f+o+1+4*0]%cm[0] )/2
			mpv = 0
			atv = ( rv[f+o+2+4*2]%cm[2] + rv[f+o+3+4*2]%cm[2] - rv[f+o+0+4*2]%cm[2] - rv[f+o+1+4*2]%cm[2] )/2
			dev = ( rv[f+o+2+4*3]%cm[3] + rv[f+o+3+4*3]%cm[3] - rv[f+o+0+4*3]%cm[3] - rv[f+o+1+4*3]%cm[3] )/2
			mav = ( rv[f+o+2+4*4]%cm[4] + rv[f+o+3+4*4]%cm[4] - rv[f+o+0+4*4]%cm[4] - rv[f+o+1+4*4]%cm[4] )/2
			rev = ( rv[f+o+2+4*5]%cm[5] + rv[f+o+3+4*5]%cm[5] - rv[f+o+0+4*5]%cm[5] - rv[f+o+1+4*5]%cm[5] )/2
			spv = ( rv[f+o+2+4*6]%cm[6] + rv[f+o+3+4*6]%cm[6] - rv[f+o+0+4*6]%cm[6] - rv[f+o+1+4*6]%cm[6] )/2
			rawgain = hpv+mpv+atv+dev+mav+rev+spv
			if rawgain >= netgain:
				string = "%d - %08X - %s - %d | HP: %2d | MP: %2d | AT: %2d | DF: %2d | MA: %2d | RE: %2d | SP: %2d" % (f+rf,rs[f],classstr,rawgain,hpv,mpv,atv,dev,mav,rev,spv)
				print string
				text_file.write(string + '\n')
		

	
	return

# **************************************************** #	

# Advance the RNG
def randf(seed):	
	newseed = seed # hehe
	newseed *= 0x41C64E6D
	newseed += 0x00003039
	newseed &= 0xFFFFFFFF
	return newseed # nice
	
# **************************************************** #
	
# Populate frame list
def populate(seed,srange):	
	cseed = seed
	rv,rs = [seed],[seed]
	srange = srange+50
	for frame in range(srange):
		cseed = randf(cseed)
		rv.append((cseed>>16)&0x7FFF)
		rs.append(cseed)
	return (rv,rs)
	
# **************************************************** #

# Execute Script:
go=1
while go==1:
	(seed,cv,netgain,srange)=getinput()
	original_range,rf = srange,0
	while srange > 1000000: # If Searching more than 1 million
		operate(seed,cv,netgain,1000001,rf)	# Operate for Only a million, then return
		seed = rs[1000000]
		srange -= 1000001
		rf += 1000000
		print "%d - Looping!" % rf
		
	operate(seed,cv,netgain,srange,rf)
	finalseed = rs[srange]
	
	print "Final Seed: %08X | Frames Iterated: %d" % (finalseed,original_range)
	text_file.close()
	if raw_input("\nResults exported.\nSearch Another? (y/n): ") != "y":
		go=0

# Notify For Completion
raw_input("\nDone. Press Enter to Exit.")
