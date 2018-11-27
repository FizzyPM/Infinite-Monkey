# Infinite Monkey Theorem
The “infinite monkey theorem” is stated as follows: A monkey hitting keys randomly on a typewriter will eventually type the complete works of Shakespeare (given an infinite amount of time). The problem with this theory is that the probability of said monkey actually typing Shakespeare is so low that even if that monkey started at the Big Bang, it’s unbelievably unlikely we’d even have Hamlet at this point.

## Genetic algorithm:
```
SETUP:

Step 1: Initialize. Create a population of N elements, each with randomly generated DNA.

LOOP:

Step 2: Selection. Evaluate the fitness of each element of the population and build a mating pool.

Step 3: Reproduction. Repeat N times:

    a) Pick two parents with probability according to relative fitness.
    b) Crossover—create a “child” by combining the DNA of these two parents.
    c) Mutation—mutate the child’s DNA based on a given probability.
    d) Add the new child to a new population.

Step 4. Replace the old population with the new population and return to Step 2.
```
The code is written in Python3 and the GUI is implemented using the python library **pygame** . Install the pygame on your virtual environment using the command : `pip3 install pygame` .
