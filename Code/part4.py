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

def lexialgo_I(y, alpha):
    #first this sorts lexicographically 
    y.sort()
    #Now we're going to find the I-optimal elements of y
    #Since y[0] is the lexicographic minimum, it certainly is
    #one of the I-optimal points
    #Unless, that is, alpha_min < 0, in which case we have to invert this order
    current_y = y[0]
    toreturn = [current_y]
    one_alpha_min = 1 - alpha[0]
    one_alpha_max = 1 - alpha[1]
    for i in range(1, len(y)):
        next_y = y[i]
        #For each other element, I compare that element to the current y
        #Since they're ordered lexicographically, they're in a growing order of their first elements
        #Therefore, I just compare their second elements
        if (one_alpha_max * current_y[1]) > (one_alpha_max * next_y[1]):
            toreturn = [next_y] + toreturn
            current_y = next_y
    
    #This operaton is O(n)
    if alpha[0] < 0:
        y.reverse()
        toreturn = [y[0]] + toreturn
    current_y = y[0]
    for i in range(1, len(y)):
        next_y = y[i]
        if (one_alpha_min * current_y[1]) > (one_alpha_min * next_y[1]):
            toreturn = [next_y] + toreturn
            current_y = next_y
    
    return toreturn

def P(y, k):
    #To avoid stack overflows, instead of doing this recursively, well do this linearly
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
                #Otherwise, we use the recurrence relation. We start with P(i-1, j-1)
                new_p = []
                for l in range(len(p_mat[j-1][i-1])):
                    #(This part only serves to keep track of which objects we've added so far)
                    elements = p_mat[j-1][i-1][l][2 : len(p_mat[j-1][i-1][l])]
                    #Each element of the pareto-optimal set is a tuple whose two first components are
                    #the cost of that element, and the others are the objects that make that element up
                    new_p += [[p_mat[j-1][i-1][l][0] + y[i][0], p_mat[j-1][i-1][l][1] + y[i][1], i] + elements]
                if i > 0:
                    #Here we add P(i-1, j)
                    new_p += to_add[i-1]
                #And here we find the pareto-optimal elements of the above-defined set
                to_add += [lexialgo(new_p)]
        #Finally, we add that line to the pareto-optimal matrix
        p_mat += [to_add]
    #And we return the final solution, a list of the pareto-optimal results
    return p_mat[k][n-1]

def P_I(y, k, alpha):
    #To avoid stack overflows, instead of doing this recursively, well do this linearly
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
                #Otherwise, we use the recurrence relation. We start with P(i-1, j-1)
                new_p = []
                for l in range(len(p_mat[j-1][i-1])):
                    #(This part only serves to keep track of which objects we've added so far)
                    elements = p_mat[j-1][i-1][l][2 : len(p_mat[j-1][i-1][l])]
                    #Each element of the pareto-optimal set is a tuple whose two first components are
                    #the cost of that element, and the others are the objects that make that element up
                    new_p += [[p_mat[j-1][i-1][l][0] + y[i][0], p_mat[j-1][i-1][l][1] + y[i][1], i] + elements]
                if i > 0:
                    #Here we add P(i-1, j)
                    new_p += to_add[i-1]
                #And here we find the pareto-optimal elements of the above-defined set
                to_add += [lexialgo_I(new_p, alpha)]
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
    #Given a bunch of vectors y and an interval alpha, this finds the minimax point
    current_best = 0
    current_f = f(y[0], alpha)
    for i in range(1, len(y)):
        new_f = f(y[i], alpha)
        if new_f < current_f:
            current_f = new_f
            current_best = i
    return y[current_best]

def main():
    if len(sys.argv) < 7:
        print "Error: too few arguments. The correct arguments are given by python part4.py n k m emin emax step filename where:"
        print " - n is number of vectors/objects to generate"
        print " - k is the number of objects to be chosen"
        print " - m is the mean of the vectors"
        print " - emin and emax are the minimum and maximum values of epsilon"
        print " - step is the step between each simulation"
        print " - filename is an optional argument that defines the name of the output file (default is 'part4.txt')"
        return 0
    n = int(sys.argv[1])
    if n <= 0:
        print "Error: n must be a positive integer"
        return 0
    k = int(sys.argv[2])
    if k <= 0:
        print "Error: k must be a positive integer"
        return 0
    if k > n:
        print "Error: k must be less than or equal to n"
        return 0
    m = int(sys.argv[3])
    if m <= 0:
        print "Error: m must be positive"
        return 0
    e_min = float(sys.argv[4])
    if e_min <= 0:
        print "Error: emin must be positive"
        return 0
    e_max = float(sys.argv[5])
    if e_max <= 0:
        print "Error: emax must be positive"
        return 0
    if e_max <= e_min:
        print "Error: emax must be greater than e_min"
        return 0
    step = float(sys.argv[6])
    if step <= 0:
        print "Error: step must be positive"
        return 0
    if len(sys.argv) < 8:
        filename = 'part4.txt'
    else:
        filename = str(sys.argv[7])
    
    f = open(filename, 'w')
    max_i = int((e_max - e_min)/step) + 1
    print 'Delta, Pareto, I'
    epsilon = 0
    i = 0
    for i in range(1, max_i + 2):
        time_pareto = 0
        time_I = 0
        epsilon = step * i
        alpha = [0.5 - epsilon, 0.5 + epsilon]
        for j in range(50):
            y = vecs(n, m)

            start_time = time.time()
            result = P(y, k)
            result = q8(result, alpha)
            end_time = time.time()
            time_pareto += end_time - start_time

            start_time = time.time()
            result = P_I(y, k, alpha)
            result = q8(result, alpha)
            end_time = time.time()
            time_I += end_time - start_time
        time_pareto = time_pareto/50
        time_I = time_I/50
        toprint = str(alpha[1]-alpha[0]) + ', ' + str(time_pareto) + ', ' + str(time_I)
        print toprint
        f.write(str(toprint) + '\n')
    f.close()

main()
