using SymPy
using Calculus
using ForwardDiff
using Optim
using Roots
using Polynomials
#using MultivariatePolynomials
using DynamicPolynomials
using PolynomialRoots
using Plots


x0 = 1#initial capital
s0 = 1 #initial price
global u = 2 #up factor
global d = 0.5 #down factor
r = 0.25#interest rate
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
        deriv = DynamicPolynomials.differentiate(tcap, y)
        eval += (prob)^i * (1-prob)^(n - i) * binomial(BigInt(n), BigInt(i)) * ( deriv /(tcap*tcap*tcap*tcap))
    end
    numer = numerator(eval)
    coeffs = [coefficient(numer, y^i) for i = 0 : maxdegree(numer)]
    roo = PolynomialRoots.roots(coeffs)

    badRoots = Set()

    for root in roo
        if imag(root) != 0
            push!(badRoots, root)
        else
            root = real(root)
            for i in 0:n
                if (((x0 - s0 * root) * ( (1+r)^n) + ( (u^i) * (d^(n-i)) * s0 *root))) <= 0
                    push!(badRoots, root)
                end
                break
            end
        end
    end
    roo = Set(real.(roo))
    goodRoots = setdiff(roo, badRoots)
    goodRoots = collect(goodRoots)
    goodRoots = sort!(goodRoots)

    tpls = zeros(BigFloat, 0, 2)
    for root in goodRoots
        tcap = 0
        for i in 0:n
            tcap +=  (prob)^i * (1-prob)^(n - i) * binomial(BigInt(n), BigInt(i)) * -1/3 *((x0 - s0 * root)*((1+r)^n) +((u^i) * (d^(n-i)) * s0 *root))^(-3)
        end
        v = [root tcap]
        tpls = vcat(v, tpls)
    end
    a = findmax(tpls)
    opy = tpls[(a[2])[1]]
    return opy
end


function getSwitch(n, min, max, steps)
    arr = zeros(steps + 1, 4)
    sw = zeros(0, 2)
    for i in 1:(steps + 1)
        println(i)
        arr[i, 1] = min + (i-1) * (max - min)/steps
        a = pOptimalY(1, arr[i, 1])
        b = pOptimalY(n, arr[i, 1])
        arr[i, 2] = a
        arr[i, 3] = b
        arr[i, 4] = b - a
    end
    for i in 1:(size(arr, 1))
        row = arr[i, :]
        println(row)
        if i == 1
            continue
        elseif i == steps
            break
        elseif arr[i-1, 4] < 0 && arr[i, 4] > 0
            println("decreasing to increasing: ", arr[i, 1])
        elseif arr[i-1, 4] > 0 && arr[i, 4] < 0
            println("increasing to decreasing: ", arr[i, 1])
        end
    end
    return sw
end

#println(getSwitch(15, 0.58, 0.6,  100))
#println(p̃)

#plots optimaly for s curves of constant p ∈ [min, max] for periods [1, n]
function graph(n, min, max, s)
    allY = zeros(0)
    probs = zeros(0)
    for i in 1:(s) #for a fixed probability
        println(i)
        global arr = zeros(s+1)
        prob = min + (i-1) * (max - min)/s
        for j in 1:n
            arr[j] = pOptimalY(j, arr[i, 1])
        end
        x = 1:n
        y = arr
        #println("arr", arr)
        allY = vcat([y], allY)
        prob = string(prob)
        probs = vcat(prob, probs)
        println("probs", probs)

    end
    display(plot(allY, title="optimalY vs n", label = probs, legend=:best))
    return arr
end

graph(10, p̃, 1, 10)

function varyingR(n)
    switch = zeros(0)
    for i in (d*100 + 1):(u*100 - 1)
        global r = i/1000 - 1
        println("r: ", r)
        z = getSwitch(n, p̃, 1, 100)
        println("z: ", z)
        append!(switch, z)
        println(switch)
    end
    return switch
end

function rnmExpectedVal(n)
    eval = 0
    for i in 0:n
        eval += p̃^i * q̃^(n - i) * binomial(BigInt(n), BigInt(i)) * f(terminalcap(n, i))
    end
    return eval
end



function constantRatio(rat)
    for i in 2:10
        global u = i
        global d = rat/i
        println(u)
        println(d)
        println(real.(getequipoints(1)[2]))
    end
end
