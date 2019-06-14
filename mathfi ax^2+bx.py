import numpy
import matplotlib.pyplot as plt
import math
import sympy
import fractions

y = sympy.symbols("y")  # Number of shares of each stock
p = 2/3  # actual probability Heads
q = 1/3 # actual probability Tails
S = 1  # Initial cost of Stock
u = 2  # Up Factor
d = 1/2  # Down Factor
r = 1/4
X = 100  # initial capital
poly = 0

a = -0.1
b = 100

def nCr(n, r):
    return math.factorial(n)/(math.factorial(n-r)*math.factorial(r))


def findExpectedUtility(N):  # Assuming U(x) = ax^2 + bx, return a polynomial function for E(U(x))
    # Number of stocks
    poly = 0

    for i in range(0, N+1):
        prob = (p**i) * (q**(N-i))
        binom = nCr(N, i)
        termCaps = ((X-S*N*y)*(1+r)+S*d*N*y + S*(u-d)*i*y)
        derivative = (-1 * S * N*(1+r) +S*d*N + S*(u-d)*i)
        poly += ( derivative * (2*a*termCaps + b))
    print(poly)
    return poly


#return all y roots
def getRoots(N): 

    util = 0
    poly = 0
    #yValues = testSymPy(N)
    y = sympy.symbols("y")
    expValPoly = findExpectedUtility(N)
    roots = (sympy.solveset(sympy.Eq(expValPoly, 0), y))
    roots = list(roots)
    #print("Allroots", roots)
    return roots

def getValidRoots(N): # return all valid roots

    util = 0
    poly = 0
    allRoots = getRoots(N)

    badRoots = set()
    for root in allRoots:
        for i in range(0, N+1):
           # print(root, i, ((X-S*N*root)*(1+r) + S*d*N*root + S*(u-d)*root*i)  )
            a = ((X-S*N*root)*(1+r) + S*d*N*root + S*(u-d)*root*i)
            if almostEqual(0,((X-S*N*root)*(1+r) + S*d*N*root + S*(u-d)*root*i)) == True:
            	continue
            elif ((X-S*N*root)*(1+r) + S*d*N*root + S*(u-d)*root*i) <= 0:
                badRoots.add(root)
    allRoots = set(allRoots)

    goodRoots = allRoots.difference(badRoots)

    #print("goodRoots",goodRoots)
    return sorted(list(goodRoots))

def almostEqual(x, y):
    return abs(x - y) < 10**-8

def getExpectedUtil(N): #return E(U(x)) for each good root

    util = 0
    poly = 0
    yValues = getRoots(N)

    terminalCaps = []
    for val in yValues:
        for i in range(0, N+1):
        	#print(val)
        	if (X-S*N*val)*(1+r) + S*d*N*val + S*(u-d)*val*i <= 0:
        		util += 0
        	else:
        		util += (p**i)*(q**(N-i)) * nCr(N, i) * a*((X-S*N*val)*(1+r)\
                 + S*d*N*val + S*(u-d)*val*i)**2 + b* ((X-S*N*val)*(1+r) + S*d*N*val + S*(u-d)*val*i)
        terminalCaps.append(util)
        util = 0
    return sorted(terminalCaps)

def getValidUtilNY(N): # get Ny yValues
	validRoots = getValidRoots(N)
	for i in range(len(validRoots)):
		validRoots[i] *= N
	return validRoots

#print(getRoots(32))
print(getRoots(10))
print(getExpectedUtil(10))
#print(getValidUtilNY(15))
# for i in range(1,15):
# 	print("N="+str(i))
# 	plt.plot(i, getValidUtilNY(i), "o" ,label = str(i))
   #plt.plot(i, getExpectedUtil(i), "o" , label = str(i))
# plt.xlabel('y')
# plt.ylabel('E(u(x))')
# plt.grid(True)
# #plt.legend(bbox_to_anchor = (.9, 1.15), loc='upper left', borderaxespad=0.)
# plt.show()
