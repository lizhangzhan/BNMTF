"""
Recover the toy dataset generated by example/generate_toy/bnmf/generate_bnmf.py
using VB, and plot the MSE against timestamps.

We can plot the MSE, R2 and Rp as it converges, on the entire dataset.

We have I=100, J=80, K=10, and no test data.
We give flatter priors (1/10) than what was used to generate the data (1).
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_vb_optimised import bnmf_vb_optimised
from ml_helpers.code.mask import calc_inverse_M

import numpy, random, scipy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmf/"

repeats = 10

iterations = 10
init_UV = 'random'
I, J, K = 100,80,10

alpha, beta = 1., 1. #1., 1.
lambdaU = numpy.ones((I,K))/10.
lambdaV = numpy.ones((J,K))/10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.ones((I,J))


# Run the VB algorithm, <repeats> times
times_repeats = []
performances_repeats = []
for i in range(0,repeats):
    # Set all the seeds
    numpy.random.seed(0)
    random.seed(0)
    scipy.random.seed(0)
    
    # Run the classifier
    BNMF = bnmf_vb_optimised(R,M,K,priors) 
    BNMF.initialise(init_UV)
    BNMF.run(iterations)

    # Extract the performances and timestamps across all iterations
    times_repeats.append(BNMF.all_times)
    performances_repeats.append(BNMF.all_performances)

# Check whether seed worked: all performances should be the same
assert all([numpy.array_equal(performances, performances_repeats[0]) for performances in performances_repeats]), \
    "Seed went wrong - performances not the same across repeats!"

# Print out the performances, and the average times
vb_all_times_average = list(numpy.average(times_repeats, axis=0))
vb_all_performances = performances_repeats[0]
print "vb_all_times_average = %s" % vb_all_times_average
print "vb_all_performances = %s" % vb_all_performances


# Print all time plots, the average, and performance vs iterations
plt.figure()
plt.title("Performance against time")
plt.ylim(0,10)
for times in times_repeats:
    plt.plot(times, vb_all_performances['MSE'])

plt.figure()
plt.title("Performance against average time")
plt.plot(vb_all_times_average, vb_all_performances['MSE'])
plt.ylim(0,10)

plt.figure()
plt.title("Performance against iteration")
plt.plot(vb_all_performances['MSE'])
plt.ylim(0,10)