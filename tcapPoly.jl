using SymPy
using Calculus
using ForwardDiff
using Optim
using Roots
using Polynomials
#using MultivariatePolynomials
using DynamicPolynomials
using PolynomialRoots


x0 = 100#initial capital
s0 = 1 #initial price
global u = 4 #up factor
global d = 0.5 #down factor
r = 0#interest rate
@polyvar y p#number of shares

μ = Sym("μ")
f(x) = log.(x)  #utility function
q = 1 - p
p̃ = (1 + r - d)/(u - d)
q̃ = 1 - p̃

#calculates terminal capital given of n periods when stock goes up i times
#n is number of periods
#i is number of times stock goes up
function terminalcap(n, i)
    tcap = (x0 - y)*(1+r)^(n) + u^(i) * d^(n-i) * y
    return tcap
end

#calculates expected value, n is number of periods
function expectedVal(n)
    eval = 0
    for i in 0:n
        tcap = (x0 - y)*(1+r)^n + u^i * d^(n-i)*y
        println(tcap)
        println(typeof(tcap))
        eval += p^i * q^(n - i) * binomial(BigInt(n), BigInt(i)) * f(tcap)
    end
    println(typeof(eval))
    return eval
end

#given a desired probability, calculate the optimal y
function pOptimalY(n, prob)
    eval = 0
    num = 0
    for i in 0:n
        tcap = (x0 - y)*(1+r)^n + u^i * d^(n-i)*y
        num = DynamicPolynomials.differentiate(tcap, y)
        eval += (prob)^i * (1-prob)^(n - i) * binomial(BigInt(n), BigInt(i)) * (num/tcap)
    end
    #println(typeof(eval))
    #println(numerator(eval))
    #println(eval)
    numer = numerator(eval)
    coeffs = [coefficient(numer, y^i) for i = 0 : maxdegree(numer)]
    roo = real(PolynomialRoots.roots(coeffs))
    #println(roo)
    filter!(x->x>0, roo)
    #println(roo)
    if isempty(roo)
        return 0
    end
    #println(roo)
    return findmin(roo)[1]
end


function getSwitch(n, min, max, steps)
    arr = zeros(steps + 1, 4)
    for i in 1:(steps + 1)
        println(i)
        arr[i, 1] = min + (i-1) * (max - min)/steps
        a = pOptimalY(1, arr[i, 1])
        b = pOptimalY(n, arr[i, 1])
        arr[i, 2] = a
        arr[i, 3] = b
        arr[i, 4] = b - a
    end
    println(arr)
    println(size(arr, 1) + 1)
    for i in 1:(size(arr, 1))
        row = arr[i, :]
        println(row)
        if i == 1
            continue
        elseif i == steps
            break
        elseif arr[i-1, 4] < 0 && arr[i, 4] > 0 && arr[i+1, 4] >= 0
            return arr[i, 1]
        #elseif arr[i-1, 4] > 0 && arr[i, 4] < 0 && arr[i+1, 4] <=0
            #println(arr[i, 1])
        end
    end
    return -1
end

println(getSwitch(10, p̃, 1, 100))

function rnmExpectedVal(n)
    eval = 0
    for i in 0:n
        eval += p̃^i * q̃^(n - i) * binomial(BigInt(n), BigInt(i)) * f(terminalcap(n, i))
    end
    return eval
end


#solve for y in terms of p for n, plug into n+1
#the goal is to solve for y and p in E[n] and E[n+1]
function getequipoints(n)
    g = diff(expectedVal(n), y)
    h = diff(expectedVal(n+1), y)
    out = solve([g, h], [y, p])
    return out
    #optimize(diff(g, x0)) #Sym type
end
#finds switch probability given expected value and number of periods
#=function findswitch(n, exp)
    g = diff(expectedval(n), y)
    h = diff(expectedval(n+1), y)
    out = solve([g - exp, h - exp], [y, p])
    return out
end=#
#println(typeof(expectedval(1)))

function constantRatio(rat)
    for i in 2:10
        global u = i
        global d = rat/i
        println(u)
        println(d)
        println(real.(getequipoints(1)[2]))
    end
end

#constantRatio(1/4)
#=println(typeof(lambdify(expectedval(1))))
g(y, p) = lambdify(expectedval(1))
vec = [rnmExpectedVal, p̃]
optimize(g(x), vec)=#

#tcap(n, i) = (x0 - y)*(1+r)^(n) + u^(i) * d^(n-i) * y
