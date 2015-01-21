import numpy as np
import sys

def vecs(n, m):
    #Returns an array of n random 2-vectors with mean m and stdev m/4
    if m <= 0:
        return 0
    rand = np.random.normal(m + 0.0, m/4.0, 2*n)
    toreturn = np.ndarray(shape=(n,2))
    for i in range(0,n):
        toreturn[i] = [rand[2*i], rand[2*i + 1]]
    return toreturn.tolist()

def f(y, alpha):
    #y is a vector in R2, alpha is the interval
    #Since f is a linear function of alpha, when the first element of
    #y is greater than the second, the value of alpha that maximises
    #this function is the greatest value; and vice-versa
    if y[0] > y[1]:
        a = alpha[1]
    else:
        a = alpha[0]
    return a * y[0] + (1 - a) * y[1]

def naive(y, alpha):
    #y here is an array of 2-vectors, alpha is the relevant interval
    f_values = []
    for i in range(len(y)):
        f_values += [f(y[i], alpha)]
    toreturn = []
    for i in range(len(y)):
        f1 = f_values[i]
        best = True
        for j in range(len(y)):
            if i != j and f_values[j] < f1:
                best = False
                break
        if best:
            toreturn += [i]
    return toreturn

def q4(y, alpha):
    #same as naive
    #first let's do a lexicographical order sort
    #sorted_y = y.sort()
    sorted_y = y[np.lexsort((y[:,1], y[:,0]))]
    #this algorithm fills the list with all the vectors that have the
    #same f-value as the current best one, and if an even better one
    #is found, that list is emptied
    current_f = f(y[0], alpha)
    toreturn = [0]
    for i in range(1, len(y)):
        new_f = f(y[i], alpha)
        if new_f < current_f:
            current_f = new_f
            toreturn = [i]
        elif new_f == current_f:
            toreturn = [i] + toreturn
    return toreturn

def main():
    

main()
