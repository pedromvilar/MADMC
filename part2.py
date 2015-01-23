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

def main():
    if len(sys.argv) < 5:
        print "Error: too few arguments. The correct arguments are given by python part2.py n_min n_max step m filename where:"
        print " - n_min is the minimum number of vectors to generate"
        print " - n_max is the maximum"
        print " - step is the step between each simulation"
        print " - m is the mean of the vectors"
        print " - filename is an optional argument that defines the name of the output file (default is 'part2.txt')"
        return 0
    n_min = int(sys.argv[1])
    if n_min <= 0:
        print "Error: n_min must be a positive integer"
        return 0
    n_max = int(sys.argv[2])
    if n_max <= 0:
        print "Error: n_max must be a positive integer"
        return 0
    if n_max < n_min:
        print "Error: n_max must be greater than n_min"
        return 0
    step = int(sys.argv[3])
    if step <= 0:
        print "Error: step must be a positive integer"
        return 0
    if (n_max - n_min) % step != 0:
        print "Error: step must divide n_max - n_min"
        return 0
    m = float(sys.argv[4])
    if m <= 0:
        print "Error: m must be positive"
        return 0
    if len(sys.argv) < 6:
        filename = 'part2.txt'
    else:
        filename = str(sys.argv[5])
    f = open(filename, 'w')
    max_i = ((n_max - n_min)/step) + 1
    print 'Number, Naive, Lexi'
    for i in range(1, max_i + 1):
        time_naive = 0
        time_lexialgo = 0
        for j in range(50):
            y = vecs(step * i, m)
            
            start_time = time.time()
            result = naive(y)
            end_time = time.time()
            time_naive += end_time - start_time

            start_time = time.time()
            result = lexialgo(y)
            end_time = time.time()
            time_lexialgo += end_time - start_time
        time_naive = time_naive/50
        time_lexialgo = time_lexialgo/50
        toprint = str(step * i) + ', ' + str(time_naive) + ', ' + str(time_lexialgo)
        print toprint
        f.write(str(toprint) + '\n')
    f.close()

main()
