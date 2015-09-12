"""
Recover the toy dataset generated by example/generate_toy/bnmf/generate_bnmf.py
We use the parameters for the true priors.

For 10% values missing we quickly converge to a good solution, and even after
reaching convergence the MSE on the test dataset barely goes up as we do more
iterations. MSE 0.16, R^2 0.9988, after 1000 iterations.

When 80% of the values are missing, we converge to a local minimum, but one
that has very poor performance (MSE 13 on the training, 45 on test - but still 
an R^2 of 0.85). 
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_vb import bnmf_vb
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/example/generate_toy/bnmf/"

iterations = 100
init = 'random'
I, J, K = 20, 10, 5 #100, 50, 10

alpha, beta = 1., 1. #1., 1.
lambdaU = numpy.ones((I,K))*2
lambdaV = numpy.ones((J,K))*2
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.loadtxt(input_folder+"M.txt")
M_test = calc_inverse_M(M)

# Run the Gibbs sampler
BNMF = bnmf_vb(R,M,K,priors)
BNMF.initialise()
BNMF.run(iterations)

# Also measure the performances
performances = BNMF.predict(M_test)
print performances

# Plot the tau expectation values to check convergence
plt.plot(BNMF.all_exp_tau)