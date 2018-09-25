import random

def tip_gen():
	# Create random number to show a random advice
	advice = random.randint(1,12)

	# Read advices from file.
	file = open("/home/shiomar/Desktop/SAT/1_Source/5_Tips/Tip.txt", "r")
	lines=file.readlines()
	return lines[advice-1]