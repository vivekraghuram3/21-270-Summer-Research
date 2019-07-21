import numpy
import matplotlib.pyplot as plt
import math
import sympy
import fractions
from sympy import S

p = 0.68 # actual probability Heads
q = 0.32 # actual probability Tails
S = 1  # Initial cost of Stock
u = 2  # Up Factor
d = fractions.Fraction(1, 2)  # Down Factor
r = fractions.Fraction(1, 4)
X = 100  # initial capital

def nCr(n, r):
	return math.factorial(n)/(math.factorial(n-r)*math.factorial(r))


def findPoly(N):  # Assuming U(x) = ln(x), return a polynomial function for E(U(x))
	# Number of stocks
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
def getRoots(N): 
 # initial capital
	util = 0
	#yValues = testSymPy(N)
	y = sympy.symbols("y", real = True)
	expValPoly = findPoly(N)
	roots = (sympy.solveset(sympy.Eq(expValPoly, 0), y))
	roots = list(roots)
	boots = []
	print("before real filter", roots)
	for root in roots:
		if (sympy.re(root) == root):
			boots.append(sympy.re(root))
		#root = sympy.re(root)
		

	# for root in roots:
	#     if root.contains("I"):
	#         roots.remove(root)
	# for root in roots:
	#     root = float(root)
	#print("Allroots", boots)
	return boots

def getValidRoots(N): # return all valid roots

	util = 0

	allRoots = getRoots(N)

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
	return sorted(list(goodRoots))

def almostEqual(x, y):
	return abs(x - y) < 10**-8

def getExpectedUtil(N): #return E(U(x)) for each good root

	util = 0
	yValues = getValidRoots(N)

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
	print(terminalCaps)
	return sorted(terminalCaps)

def getValidUtilNY(N): # get Ny yValues
	validRoots = getValidRoots(N)
	for i in range(len(validRoots)):
		validRoots[i] *= N
	return validRoots

# print(getRoots(11))
# print("test", getValidRoots(15))
# print("exp",getExpectedUtil(11))
# print(getValidUtilNY(15))
for i in range(1,12):
	print("N="+str(i))
	plt.plot(i, getValidRoots(i), "o" ,label = str(i))
	#plt.plot(i, getExpectedUtil(i), "o" , label = str(i))
plt.xlabel('y')
plt.ylabel('E(u(x))')
plt.grid(True)
plt.legend(bbox_to_anchor = (.9, 1.15), loc='upper left', borderaxespad=0.)
plt.show()