== part2.py ==
To run program part2.py, you need at least 4 arguments: n_min, n_max, step, and m, plus one optional filename argument.

- n_min is the minimum number of vectors to generate
- n_max is the maximum
- step is the step between each simulation
- m is the mean of the vectors
- filename is an optional argument that defines the name of the output file (default is 'part2.txt')

The examples asked for in Question 5 would then run as python part2.py 200 10000 200 1000.

This generates a text file with the number of vectors, the time using the naïve algorithm, and the time using the lexicographically sorted one.

== part3.py ==
To run program part3.py, you need at least 5 arguments: n, m, k, amin, and amax, plus one optional v argument.

- n is the number of vectors/objects generated;
- m is the mean of the normal distribution to generate them;
- k is how many objects the optimal set has to have;
- amin is the lower bound of the interval I;
- amax is the upper bound of that interval;
- v is an optional argument for verbosity (default 0).
-- 0 shows only the final result and its cost.
-- 1 shows the objects that make it up.
-- 2 includes the entire pareto-optimal set.
-- 3 includes all objects generated.

So, for example, run python part3.py 10 100 5 0 2 2 to generate 10 objects whose costs have mean 100 and stdev 25, 5 of which must be in the final optimal set, which will be calculated on the [0, 2] interval, and you'll see the final result, the objects that make it up, and the entire pareto-optimal set.

== part4.py ==
To run program part4.py, you need at least 6 arguments: n, k, m, emin, emax, step, plus one optional filename argument.

- n is number of vectors/objects to generate
- k is the number of objects to be chosen
- m is the mean of the vectors
- emin and emax are the minimum and maximum values of epsilon
- step is the step between each simulation
- filename is an optional argument that defines the name of the output file (default is 'part4.txt')

The examples asked for in Question 12 would then run as python part4.py 50 10 1000 0.025 0.5 0.025.

This generates a text file with the interval size, the time using the Pareto algorithm, and the time using the I-domination one.