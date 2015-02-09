import bitarray

class Hasher:
	def __init__(self):	
		#set the initialization vector (I used 256 bits of pi in the neighborhood of the 2-quadrillionth bit)
		self.IV = bitarray.bitarray('0000111001101100000100101001010010101110110101000000010000000011111101010110110100101101011101100100000000100110001001100101101111001010100110000101000100011101000011111100111111111010101000010000111101001101001010001011000110111011010100111001001010111000')
		self.input = bitarray.bitarray()
		self.paddedInput = bitarray.bitarray()
		self.finalHash = self.IV
		self.nextPiece = bitarray.bitarray()
		
		#create the rules for the various cellular automata to be used; each is chosen because it is a class 3 cellular automata, which appears to maintain a chaotic state
		#these can be declared as static (or class) variables, but for my purposes I don't think it matters
		self.rule18  = [0,0,0,1,0,0,1,0]
		self.rule22  = [0,0,0,1,0,1,1,0]
		self.rule30  = [0,0,0,1,1,1,1,0]
		self.rule45  = [0,0,1,0,1,1,0,1]
		self.rule54  = [0,0,1,1,0,1,1,0]
		self.rule60  = [0,0,1,1,1,1,0,0]
		self.rule90  = [0,1,0,1,1,0,1,0]
		self.rule105 = [0,1,1,0,1,0,0,1]
		self.rule106 = [0,1,1,0,1,0,1,0]
		self.rule129 = [1,0,0,0,0,0,0,1]
		self.rule137 = [1,0,0,0,1,0,0,1]
		self.rule146 = [1,0,0,1,0,0,1,0]
		self.rule150 = [1,0,0,1,0,1,1,0]
		self.rule161 = [1,0,1,0,0,0,0,1]
		
		
		#initialize some bitarrays that contain the modified cube roots of square numbers; these bit strings are created from the ehx representation of the first 64 digits of each cube root
		#each cube root is modified so that the very first and very last bit is always 1
		#these modifications are done so that it is more likely that there are no swaths of ones and zeros at the beginning or end of each 256-bit block before it gets processed by the cellular automaton
		#these can also be declared as static (or class) variables, but, again, for my purposes I don't think it matters
		
		#modified cube root of 2
		self.cbrt2 = bitarray.bitarray('1001001001011001100100100001000001001001100010010100100001110011000101100100011101100010000100000110000001110010011110000010001010000011010100000101011100000010010100010100011001000111000000010101000001111001100000000000100000011001011101010001000100100001')
		#modified cube root of 3
		self.cbrt3 = bitarray.bitarray('1001010001000010001001001001010101110000001100000111010000001000001110000010001100100001011000111000001100010000011110000000000100001001010110001000001110010001100001101001001001010011001010011001001101010000010101110111010101000110010000010110000110010101')
		#modified cube root of 5
		self.cbrt5 = bitarray.bitarray('1001011100001001100101110101100101000110011001110110011010010110100110001001001101010011000100001000100001110010010101000011100001100000000100001001100001101000000001010101000100010000010101000011000001010100100100100100001110000010100001100001011100000111')
		#modified cube root of 7
		self.cbrt7 = bitarray.bitarray('1001100100010010100100110001000110000010011101110010001110001001000100000001000110011001000100010110100000111001010101001000011101100000001010000010100001100010010000111001000001010000001101000101100001110101011101100110001000010000011001000111011001000001')
		#modified cube root of 11
		self.cbrt11 = bitarray.bitarray('1010001000100011100110000000000010010000010101101001001100010101010100100001000101100101001101100011001101110110011100100010000101010111000110010110010100011000011010011001000100101000000010010110100100100011000001010101011010011001001101000101100000001001')
		#modified cube root of 13
		self.cbrt13 = bitarray.bitarray('1010001101010001001100110100011010000111011100100000011101010111010010001001010100000000000000010110001100111001100101010110100100010100010100100110100100010101100001000001100110000011010001100010000101110101000100000101000001000000001001010100001100010001')
		#modified cube root of 17
		self.cbrt17 = bitarray.bitarray('1010010101110001001010000001010110010000011001011000001000110101001101010101010001010011000110000111001000001000011100111001011100100110000100010110010000100111100100000001011000110010010001010100011010010110001001011001100001001000000000100010001101110111')
		#modified cube root of 19
		self.cbrt19 = bitarray.bitarray('1010011001101000010000000001011001001000011100100001100101000100100001100111001100111001011000100111001101110001100101110000100000110000001100110101000010010101100001111000010101101001000110000011000100000001100001100101011001100100001000010011010110000111')
		#modified cube root of 23
		self.cbrt23 = bitarray.bitarray('1010100001000011100001100110100101111001100001010001010101100101010001110111011010010101010000111001010000000000100101011000011001010001100001010010011101100100000101100101000101110010011100110111000001001000000100000100011001010011010000100101001000110001')
		
		
	def askForInput(self):
		string = raw_input("Please enter a string: ")  #ask the user for a string
		self.input.frombytes(string)
		
	def takeInput(self, string):
		self.input.frombytes(string)
	
	def padInput(self):
		enteredBits = self.input
		stringLength = len(enteredBits)
		
		lengthInBinary = bin(stringLength)[2:]
		lengthLength = len(lengthInBinary)
		
		lengthBits = bitarray.bitarray(lengthInBinary)
		
		totalLength = stringLength + lengthLength
		
		#sanity-checking printout
		#print "The entered string, " + string + ", is " + str(stringLength) + " bits long."
		#print "This size is " + str(lengthLength) + " bits long. The total length would be " + str(totalLength) + " bits long."

		moduloo = (totalLength +1) % 256

		if moduloo != 0:
			lengthDifference = 256 - moduloo
			#more sanity checking printouts
			#print "This total length is not a multiple of 256. The difference is " + str(lengthDifference) + "."
			#print enteredBits
			enteredBits.append(True)

			for num in range(0,lengthDifference):
				enteredBits.append(False)

		else: #no need for this else branch really, but why not have it?
			enteredBits.append(True)
				
		enteredBits += lengthBits
		self.paddedInput = enteredBits
	
	def hash(self):
		self.padInput()
		length = len(self.paddedInput) #first we see how big the string is
		
		startPoint = 0		#where to start, increase by 256 (our block size) for each iteration
		endPoint = 256		#where to end for this iteration; increase by 256 for each iteration
		
		while endPoint <= length: #have we the whole thing?
		
			self.nextPiece = self.paddedInput[startPoint:endPoint]	#get the next 256-bit block to be processed
			
			prevParity = self.finalHash.count(True) #count the number of ones in the part of the hash that has already been processed; this will be used to choose what cube root to use for the next part
			prevParity = prevParity % 9 #there are 9 cube roots to choose from, and this gives a result from 0 to 8
			
			#next we XOR the piece we wish to process with a cube root, which is chosen depending on the parity of the result of the previous hashing work
			#since at the start of every hash this is always IV, we always choose the same cube root the first time
			if prevParity == 0:
				self.nextPiece ^= self.cbrt2
			elif prevParity == 1:
				self.nextPiece ^= self.cbrt3
			elif prevParity == 2:
				self.nextPiece ^= self.cbrt5
			elif prevParity == 3:
				self.nextPiece ^= self.cbrt7
			elif prevParity == 4:
				self.nextPiece ^= self.cbrt11
			elif prevParity == 5:
				self.nextPiece ^= self.cbrt13
			elif prevParity == 6:
				self.nextPiece ^= self.cbrt17
			elif prevParity == 7:
				self.nextPiece ^= self.cbrt19
			elif prevParity == 8:
				self.nextPiece ^= self.cbrt23
			else:
				print "Oops"
			
			currParity = self.nextPiece.count(True) #get the parity of the thing we just got from the XOR; this will determine which cellular automaton to use
			currParity = currParity % 14 #there are 14 automata to chose from; this will give a result from 0 to 13
			
			for num in range (0,3): #this used to 5, but there seemed to be many more hash collisions; seems that there is a greater chance of convergence the more you do it
				self.automato(currParity)
			
			self.finalHash ^= self.nextPiece
			
			startPoint+=256
			endPoint+=256
			
	def automato(self, parity): #think function does the processing of the 256-bit block with a specific cellular automaton, depending on the value of parity		
		
		#here we are just choosing which rule to use, based on parity
		#this seems very backwards and weird now that I look at it, but such is life
		if parity == 0:
			rule2use = self.rule18
		elif parity == 1:
			rule2use = self.rule22
		elif parity == 2:
			rule2use = self.rule30
		elif parity == 3:
			rule2use = self.rule45
		elif parity == 4:
			rule2use = self.rule54
		elif parity == 5:
			rule2use = self.rule60
		elif parity == 6:
			rule2use = self.rule90
		elif parity == 7:
			rule2use = self.rule105
		elif parity == 8:
			rule2use = self.rule106
		elif parity == 9:
			rule2use = self.rule129
		elif parity == 10:
			rule2use = self.rule137
		elif parity == 11:
			rule2use = self.rule146
		elif parity == 12:
			rule2use = self.rule150
		elif parity == 13:
			rule2use = self.rule161
		else:
			print "Oops"
			
		#now we are going to do the processing in the cellular automaton			
		#the neighborhood for each cell is of size three (the cell in the middle and the ones to the left or right)
		#in the cases of the very end and very beginning (edge cases), we simply wrap around to the other side, like in Pac-man
		#since we know the block is always 256-bits, we can do the special processing that we want
		
		for num in range(0,256):
			result = 0
			
			#these next three lines calculate the state of the cell we are currently on; 
			#this is used in conjunction with the Wolfram code (the matrix of 8 values) 
			#of each cellular automaton to determing what state the cell should be in next
			result += 4*int(self.nextPiece[(num-1) % 256])
			result += 2*int(self.nextPiece[num])
			result += int(self.nextPiece[(num+1) % 256])
			
			self.nextPiece[num] = rule2use[result]	#this line changes the state of the cell to its new state


# ###############################################################################
# ###########	The following was a program I used to test my work	 ############
# ###############################################################################

	#this is a a test program that would take a user input, output the hash, output the hash as ASCII characters, and then print out the length of the hash
	
# thing = Hasher()
# thing.askForInput()
# thing.hash()
# print "This is the final hash " + str(thing.finalHash)
# print '\n'

# print thing.finalHash.tobytes()
# print "The final hash is " + str(len(thing.finalHash.tobytes())) + " characters long."


	