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

def domine(y1, y2):
    #returns true if y1 is dominated by y2
    return (y1[0] >= y2[0] and y1[1] >= y2[1] and (y1[0] != y2[0] or y1[1] != y2[1]))

def naive(y):
    #this just compares pairwise all elements in y and
    #returns the non-dominated ones
    toreturn = []
    for i in range(len(y)):
        best = True
        for j in range(len(y)):
            if i != j and domine(y[i], y[j]):
                best = False
                break
        if best:
            toreturn = [y[i]] + toreturn
    return toreturn

def lexialgo(y):
    #first this sorts lexicographically 
    y.sort()
    #Now we're going to find the Pareto-optimal elements of y
    #Since y[0] is the lexicographic minimum, it certainly is one of the Pareto-
    #optimal points
    current_y = y[0]
    toreturn = [current_y]
    for i in range(1, len(y)):
        next_y = y[i]
        #For each other element, I compare that element to the current y
        #Since they're ordered lexicographically, they're in a growing order of
        #their first elements
        #Therefore, I just compare their second elements
        if current_y[1] > next_y[1]:
            toreturn = [next_y] + toreturn
            current_y = next_y
    return toreturn

def main():
    y = vecs(15, 1000)
    print y
    
    result = naive(y)
    print '\nNaive: ', str(result)

    result = lexialgo(y)
    print '\nLexiAlgo: ', str(result)

main()
