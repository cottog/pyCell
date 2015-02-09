import os
from pyCell import Hasher

print "Hello"
quit = False 

#the printouts of each of these tests should be sufficient to explain their intent

print "Would you like to test if a string is always hashed to the same result? Enter 1."
print "Would you like to test if different strings produce collisions? Enter 2."
print "Would you like to see the difference flipping a single bit in the input makes? Enter 3."
print "Alternatively, enter 0 to quit."

while quit == False:

	answer = raw_input('>')

	if answer == '0':
		quit = True
		print "Quitting!"
	elif answer == '1':
		print "The intention of this block of code is to test if a hash of the same string, which is arbitrary, will always give the same result."
		print "It will hash the same string 10000 times, checking each time to make sure the result is the same."
		print "It shouldn't take much more than a minute to do 10000 iterations. Only 10000 are being done because anything more would be beyond overkill. This is overkill."
		thing2 = Hasher()
		stringo = os.urandom(10)
		thing2.takeInput(stringo)
		thing2.hash() 
		stri = thing2.finalHash.tobytes()
		count = 0
		for n in range (0, 10000):
			if n > 0 and n % 100 == 0:
				print "\r [" + "=" *(n/100) + " " * ((10000-n)/100) + "]" + str(n/100) + "%" , 
			thing2 = Hasher()
			thing2.takeInput(stringo)
			thing2.hash() 
			str2 = thing2.finalHash.tobytes()
			if str2 != stri:
				count += 1
		else:
			print "\r [" + "=" *(n/100) + " " * ((10000-n)/100) + "]" + str(n/100) + "%" 
			
		print "There are " + str(count) + " mismatched results."
	elif answer == '2':
		print "The intention of this block of code is to produce 10000 random strings and see if any of them produce a hash that has a collision with any other string."
		print "For simplicity's sake, these strings are only 512 bits long. Only 10000 are being checked because each new hash must be compared to every old hash, which is a lot of hash."
		
		listing = []
		stringlist = []
		count = 0
		for n in range (0,10000):
			if n > 0 and n % 100 == 0:
				print "\r [" + "=" *(n/100) + " " * ((10000-n)/100) + "]" + str(n/100) + "%" , 
		
			stringo = os.urandom(64)
			
			if stringo not in stringlist:
				stringlist.append(stringo)
			
			thing2 = Hasher()
			thing2.takeInput(stringo)
			thing2.hash()
			if thing2.finalHash.tobytes() not in listing:
				listing.append(thing2.finalHash.tobytes())
			else:
				count += 1
					
		else:
			print "\r [" + "=" *(n/100) + " " * ((10000-n)/100) + "]" + str(n/100) + "%" 
		
		print "There were " + str(count) + " hash collisions. This may be OK. There were " + str(10000 - len(stringlist)) + " identical strings."
				
	
	elif answer == '3':
			print "Please enter two strings that differ by a single bit. Like \"far\" and \"fas\"."
			print "This test will see how many bits differ between the hashes of these two strings."
			print "The effects of flipping single bit on a hash is an important metric, for reasons this program cannot explain."
			thing1 = Hasher()
			thing2 = Hasher()
			
			thing1.askForInput()
			thing2.askForInput()
			
			thing1.hash()
			thing2.hash()
			
			count = 1
			
			for n in range(0,256):
				if thing1.finalHash[n] != thing2.finalHash[n]:
					count += 1
			
			print "Flipping one bit produced a hash that is " + str((count/256.0) * 100) + " % different." 
	
	else:
		print "Please enter 0, 1, 2, or 3!"
