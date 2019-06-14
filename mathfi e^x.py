import numpy
import matplotlib.pyplot as plt
import math
import sympy
import fractions

def nCr(n, r):
    return math.factorial(n)/(math.factorial(n-r)*math.factorial(r))


def findExpectedUtility(N):  # Assuming U(x) = (-1\mu)e^(-mu x), return a polynomial function for E(U(x))
    # Number of stocks
    y = sympy.symbols("y", real=True)  # Number of shares of each stock
    p = fractions.Fraction(2, 3)  # actual probability Heads
    q = fractions.Fraction(1, 3)  # actual probability Tails
    S = 1  # Initial cost of Stock
    u = 2  # Up Factor
    d = fractions.Fraction(1, 2)  # Down Factor
    r = fractions.Fraction(1, 4)
    X = 100  # initial capital
    mu = 2.5
    poly = 0

    firstTerm = (-1/mu)* ((math.e)**(-1*mu*(1+r)*u*X))
    secondTerm = (  (    (1-p) * (math.e)**(-1*mu*(d-1-r)*S*y)  )  + p*(math.e)**(-1*mu*S*y*(u-1-r))   )**(N-1)
    thirdTerm = (  (  (  (1-p)*(math.e)**(-1*mu*(d-1-r)*S*y)  ) *(-1*mu*(d-1-r)*S)) + ((p*((math.e)**(-1*mu*S*y*(u-1-r)))) * (-1*mu*S*(u-1-r)))  )

    poly += (firstTerm * secondTerm* thirdTerm)
    
    return poly


#return all y roots
def getRoots(N): 
    p = fractions.Fraction(2, 3)  # actual probability Heads
    q = fractions.Fraction(1, 3)  # actual probability Tails
    S = 1  # Initial cost of Stock
    u = 2  # Up Factor
    d = fractions.Fraction(1, 2)  # Down Factor
    r = fractions.Fraction(1, 4)
    X = 100  # initial capital
    util = 0
    #yValues = testSymPy(N)
    y = sympy.symbols("y", real = True)
    expValPoly = findExpectedUtility(N)
    roots = (sympy.solveset(sympy.Eq(expValPoly, 0), y))
    roots = list(roots)
    print("Allroots", roots)
    return roots

def getValidRoots(N): # return all valid roots
    p = fractions.Fraction(2, 3)  # actual probability Heads
    q = fractions.Fraction(1, 3)  # actual probability Tails
    S = 1  # Initial cost of Stock
    u = 2  # Up Factor
    d = fractions.Fraction(1, 2)  # Down Factor
    r = fractions.Fraction(1, 4)
    X = 100  # initial capital
    util = 0

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
    p = fractions.Fraction(2, 3)  # actual probability Heads
    q = fractions.Fraction(1, 3)  # actual probability Tails
    S = 1  # Initial cost of Stock
    u = 2  # Up Factor
    d = fractions.Fraction(1, 2)  # Down Factor
    r = fractions.Fraction(1, 4)
    X = 100  # initial capital
    util = 0
    mu = 2.5
    yValues = getValidRoots(N)

    terminalExpectedValue = []
    for val in yValues:
        print("root testing", val)
        one = (-1/mu) * (math.e)**(-1*mu*(1+r)*val*X)
        two = (((math.e)**(-1*mu*(d-1-r)*S*val)) * ( (1-p) + p*((math.e)**(-1*mu*(u-d)*S*val) )))**N
        util += (one * two)
    terminalExpectedValue.append(util)
    print("util",  util)
    util = 0
    return sorted(terminalExpectedValue)

def getValidUtilNY(N): # get Ny yValues
	validRoots = getValidRoots(N)
	for i in range(len(validRoots)):
		validRoots[i] *= N
	return validRoots

#print(getRoots(32))
print(getValidRoots(10))
print(getExpectedUtil(10))
print(getValidUtilNY(15))
for i in range(1,100):
 	print("N="+str(i))
 	#plt.plot(i, getValidUtilNY(i), "o" ,label = str(i))
 	plt.plot(i, getExpectedUtil(i), "o" , label = str(i))
plt.xlabel('y')
plt.ylabel('E(u(x))')
plt.grid(True)
plt.legend(bbox_to_anchor = (.9, 1.15), loc='upper left', borderaxespad=0.)
plt.show()
print(findExpectedUtility(3))
print("ValidRoots", getValidRoots(10))
