import numpy
import matplotlib.pyplot as plt
import math
import sympy
import fractions
from sympy import S
import copy

#p = 0.02 # actual probability Heads

def nCr(n, r):
	return math.factorial(n)/(math.factorial(n-r)*math.factorial(r))


def findPoly(N,p):  # Assuming U(x) = ln(x), return a polynomial function for E(U(x))
	q = 1-p # actual probability Tails
	S = 1  # Initial cost of Stock
	u = 2  # Up Factor
	d = fractions.Fraction(1, 2)  # Down Factor
	r = fractions.Fraction(1, 4)
	X = 100  # initial capital

	y = sympy.symbols("y", real=True)  # Number of shares of each stock

	poly = 0

	for i in range(0, N+1):
		prob = (p**i) * (q**(N-i))
		binom = nCr(N, i)
		numerator = (-1*S*((1+r)**N)) + (u**i)*(d**(N-i))*S
		denominator = ((X-S*y)*((1+r)**N) + ((u**i)*(d**(N-i))*S*y) )
		poly += prob * binom * (numerator/denominator)
	
	return poly


#return all y roots
def getRoots(N,p): 
	q = 1-p # actual probability Tails
	S = 1  # Initial cost of Stock
	u = 2  # Up Factor
	d = fractions.Fraction(1, 2)  # Down Factor
	r = fractions.Fraction(1, 4)
	X = 100  # initial capital

	util = 0
	#yValues = testSymPy(N)
	y = sympy.symbols("y", real = True)
	expValPoly = findPoly(N,p)
	roots = (sympy.solveset(sympy.Eq(expValPoly, 0), y))
	roots = list(roots)
	boots = []
	print("before real filter", roots)
	for root in roots:
		if (sympy.re(root) == root):
			boots.append(sympy.re(root))

	return boots

def getValidRoots(N,p): # return all valid roots
	q = 1-p # actual probability Tails
	S = 1  # Initial cost of Stock
	u = 2  # Up Factor
	d = fractions.Fraction(1, 2)  # Down Factor
	r = fractions.Fraction(1, 4)
	X = 100  # initial capital

	util = 0

	allRoots = getRoots(N,p)
	rootsCopy = copy.deepcopy(allRoots)

	badRoots = set()
	for root in allRoots:
		for i in range(0, N+1):
			#print(root, i, (((X-S*root)*((1+r)**N)+((u**i)*(d**(N-i))*S*root)))  )

			if almostEqual(0,((X-S*root)*((1+r)**N)+((u**i)*(d**(N-i))*S*root))) == True:
				continue
			elif (((X-S*root)*((1+r)**N)+((u**i)*(d**(N-i))*S*root))) <= 0:
				badRoots.add(root)

	print("bad",badRoots)
	allRoots = set(allRoots)

	goodRoots = allRoots.difference(badRoots)

	print("goodRoots",sorted(list(goodRoots)))
	posRoots = []
	if list(goodRoots) == []:
		for root in rootsCopy:
			if root > 0:
				posRoots.append(root)
		return [posRoots[0]]
	return sorted(list(goodRoots))

def almostEqual(x, y):
	return abs(x - y) < 10**-8

def getExpectedUtil(N,p): #return E(U(x)) for each good root
	q = 1-p # actual probability Tails
	S = 1  # Initial cost of Stock
	u = 2  # Up Factor
	d = fractions.Fraction(1, 2)  # Down Factor
	r = fractions.Fraction(1, 4)
	X = 100  # initial capital

	util = 0
	yValues = getValidRoots(N,p)

	terminalCaps = []
	for val in yValues:
		for i in range(0, N+1):
			#print(val)
			if (X-S*N*val)*(1+r) + S*d*N*val + S*(u-d)*val*i <= 0:
				util += 0
			else:
				util += (p**i)*(q**(N-i)) * nCr(N, i) * math.log(((X-S*val)*((1+r)**N)+((u**i)*(d**(N-i))*S)))
		terminalCaps.append(util)
		util = 0
	#print(terminalCaps)
	return sorted(terminalCaps)

def getValidUtilNY(N,p): # get Ny yValues
	q = 1-p # actual probability Tails
	S = 1  # Initial cost of Stock
	u = 2  # Up Factor
	d = fractions.Fraction(1, 2)  # Down Factor
	r = fractions.Fraction(1, 4)
	X = 100  # initial capital

	validRoots = getValidRoots(N,p)
	for i in range(len(validRoots)):
		validRoots[i] *= N
	return validRoots
yCoord = []
print("here",getValidRoots(10,0.82))
# print("here",getValidRoots(1,0.52)[0])
# print("test", getValidRoots(15))
# print("exp",getExpectedUtil(11))
# print(getValidUtilNY(15))
def graph():
	for j in range(1,100):
		print("p=",j/100)
		for i in range(1,11):
			print("N="+str(i))
			global yCoord

			yCoord.append(getValidRoots(i, j/100)[0])

		#print("ycoord", yCoord)
		plt.plot([i for i in range(1,len(yCoord)+1)], yCoord, label = str(j/100))
		yCoord = []

		#plt.plot(i, getExpectedUtil(i), "o" , label = str(i))
	plt.xlabel('N (period-number)')
	plt.ylabel('Optimal y-value')
	plt.grid(True)
	plt.legend(bbox_to_anchor = (1.0, 1.15), loc='upper left', borderaxespad=0.)
	plt.show()
graph()
