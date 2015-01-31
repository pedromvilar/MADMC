import numpy as np
import sys
import time

def vecs(n, m):
    #Returns a list of n random 2-vectors with mean m and stdev m/4
    if m <= 0:
        return 0
    rand = np.random.normal(m + 0.0, m/4.0, 2*n)
    toreturn = []
    for i in range(0,n):
        toreturn = [[rand[2*i], rand[2*i + 1]]] + toreturn
    return toreturn

def lexialgo(y):
    #first this sorts lexicographically 
    y.sort()
    #Now we're going to find the Pareto-optimal elements of y
    #Since y[0] is the lexicographic minimum, it certainly is one of the Pareto-optimal points
    current_y = y[0]
    toreturn = [current_y]
    for i in range(1, len(y)):
        next_y = y[i]
        #For each other element, I compare that element to the current y
        #Since they're ordered lexicographically, they're in a growing order of their first elements
        #Therefore, I just compare their second elements
        if current_y[1] > next_y[1]:
            toreturn = [next_y] + toreturn
            current_y = next_y
    return toreturn

def P(y, k):
    #To avoid stack overflows, instead of doing this recursively, well do this
    #linearly
    #(since we need to calculate all elements of the pareto-optimal array anyway)
    to_add = []
    n = len(y)
    #We start by filling the size-0 line with (0,0)s
    for i in range(n):
        to_add = [[[0,0]]] + to_add
    p_mat = [to_add]
    #Now we can start filling the positive-size lines
    for j in range(1, k + 1):
        to_add = []
        for i in range(n):
            if i + 1 < j:
                #If the number of objects available is less than the problem size
                #we just add the empty set to that instance of the problem
                to_add += [[]]
            else:
                #Otherwise, we use the recurrence relation. We start with
                #P(i-1, j-1)
                new_p = []
                for l in range(len(p_mat[j-1][i-1])):
                    #(This part only serves to keep track of which objects we've
                    #added so far)
                    elements = p_mat[j-1][i-1][l][2 : len(p_mat[j-1][i-1][l])]
                    #Each element of the pareto-optimal set is a tuple whose two
                    #first components are
                    #the cost of that element, and the others are the objects
                    #that make that element up
                    new_p += [[p_mat[j-1][i-1][l][0] + y[i][0], p_mat[j-1][i-1][l][1] + y[i][1], i] + elements]
                if i > 0:
                    #Here we add P(i-1, j)
                    new_p += to_add[i-1]
                #And here we find the pareto-optimal elements of the
                #above-defined set
                to_add += [lexialgo(new_p)]
        #Finally, we add that line to the pareto-optimal matrix
        p_mat += [to_add]
    #And we return the final solution, a list of the pareto-optimal results
    return p_mat[k][n-1]

def f(y, alpha):
    #y is a vector in R2, alpha is the interval
    #The function f(y) is max{y1 * a + y2 * (1 - a) : a in alpha)
    #Since f is a linear function of a, when the first element of
    #y is greater than the second, the value of a that maximises
    #this function is the greatest value; and vice-versa
    if y[0] > y[1]:
        a = alpha[1]
    else:
        a = alpha[0]
    return a * y[0] + (1 - a) * y[1]

def q8(y, alpha):
    #Given a bunch of vectors y and an interval alpha, this finds
    #the minimax point
    current_best = 0
    current_f = f(y[0], alpha)
    for i in range(1, len(y)):
        new_f = f(y[i], alpha)
        if new_f < current_f:
            current_f = new_f
            current_best = i
    return y[current_best]

def main():
    # Input is 1. n, 2. m, 3. k, and optionally 4. verbosity
    if len(sys.argv) < 6:
        print "Error: too few arguments. The correct arguments are given by python part3.py n m k amin amax v where:"
        print " - n is the number of vectors/objects to generate"
        print " - m is the mean of the normal distribution for these vectors"
        print " - k is the number of objects to be chosen from the list"
        print " - amin and amax are the boundaries of the interval I"
        print " - v is an optional argument that determines verbosity (0 is only result, 1 includes objects, 2 includes the pareto-optimal set, 3 includes all objects generated"
        return 0
    n = int(sys.argv[1])
    m = float(sys.argv[2])
    if m <= 0:
        print "Error: m must be a positive number."
        return 0
    k = int(sys.argv[3])
    amin = float(sys.argv[4])
    if amin >= 1:
        print "Error: amin must be less than 1"
        return 0
    amax = float(sys.argv[5])
    if amax <= 0:
        print "Error: amax must be greater than 0"
        return 0
    if amax < amin:
        print "Error: amax must be greater than or equal to amin"
        return 0
    alpha = [amin, amax]
    if len(sys.argv) > 6:
        verbosity = int(sys.argv[6])
    else:
        verbosity = 0
        
    # Generate the vectors
    y = vecs(n, m)
    if verbosity > 2:
        print "The objects generated were:"
        for i in range(len(y)):
            print str(i), ". (", str(y[i][0]), ",", str(y[i][1]), ")"

    #Get the results
    results = P(y, k)
    if verbosity > 1:
        print "The Pareto-optimal set was:"
        for i in range(len(results)):
            print "(", str(results[i][0]), ",", str(results[i][1]), ")"

    # Get the minimax
    best = q8(results, alpha)
    cost = f(best, alpha)
    print "The optimal choice was (", str(best[0]), ",", str(best[1]), ") with a cost of ", str(cost), "."

    if verbosity > 0:
        print "The objects that comprise the optimal choice are:"
        for i in range(len(best) - 2):
            this_one = y[best[i+2]]
            print "(", str(this_one[0]), ",", str(this_one[1]), ")"

main()
