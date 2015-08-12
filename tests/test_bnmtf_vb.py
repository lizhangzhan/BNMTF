"""
Tests for the BNMTF Variational Bayes algorithm.
"""

import numpy, math, pytest, itertools
from BNMTF.code.bnmtf_vb import bnmtf_vb


""" Test constructor """
def test_init():
    # Test getting an exception when R and M are different sizes, and when R is not a 2D array.
    R1 = numpy.ones(3)
    M = numpy.ones((2,3))
    I,J,K,L = 5,3,1,2
    lambdaF = numpy.ones((I,K))
    lambdaS = numpy.ones((K,L))
    lambdaG = numpy.ones((J,L))
    alpha, beta = 3, 1    
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R1,M,K,L,priors)
    assert str(error.value) == "Input matrix R is not a two-dimensional array, but instead 1-dimensional."
    
    R2 = numpy.ones((4,3,2))
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R2,M,K,L,priors)
    assert str(error.value) == "Input matrix R is not a two-dimensional array, but instead 3-dimensional."
    
    R3 = numpy.ones((3,2))
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R3,M,K,L,priors)
    assert str(error.value) == "Input matrix R is not of the same size as the indicator matrix M: (3, 2) and (2, 3) respectively."
    
    # Similarly for lambdaF, lambdaS, lambdaG
    I,J,K,L = 2,3,1,2
    R4 = numpy.ones((2,3))
    lambdaF = numpy.ones((2+1,1))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R4,M,K,L,priors)
    assert str(error.value) == "Prior matrix lambdaF has the wrong shape: (3, 1) instead of (2, 1)."
    
    lambdaF = numpy.ones((2,1))
    lambdaS = numpy.ones((1+1,2+1))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R4,M,K,L,priors)
    assert str(error.value) == "Prior matrix lambdaS has the wrong shape: (2, 3) instead of (1, 2)."
    
    lambdaS = numpy.ones((1,2))
    lambdaG = numpy.ones((3,2+1))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R4,M,K,L,priors)
    assert str(error.value) == "Prior matrix lambdaG has the wrong shape: (3, 3) instead of (3, 2)."
    
    # Test getting an exception if a row or column is entirely unknown
    lambdaF = numpy.ones((I,K))
    lambdaS = numpy.ones((K,L))
    lambdaG = numpy.ones((J,L))
    M1 = [[1,1,1],[0,0,0]]
    M2 = [[1,1,0],[1,0,0]]
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R4,M1,K,L,priors)
    assert str(error.value) == "Fully unobserved row in R, row 1."
    with pytest.raises(AssertionError) as error:
        bnmtf_vb(R4,M2,K,L,priors)
    assert str(error.value) == "Fully unobserved column in R, column 2."
    
    # Finally, a successful case
    I,J,K,L = 3,2,2,2
    R5 = 2*numpy.ones((I,J))
    lambdaF = numpy.ones((I,K))
    lambdaS = numpy.ones((K,L))
    lambdaG = numpy.ones((J,L))
    M = numpy.ones((I,J))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    BNMTF = bnmtf_vb(R5,M,K,L,priors)
    
    assert numpy.array_equal(BNMTF.R,R5)
    assert numpy.array_equal(BNMTF.M,M)
    assert BNMTF.I == I
    assert BNMTF.J == J
    assert BNMTF.K == K
    assert BNMTF.size_Omega == I*J
    assert BNMTF.alpha == alpha
    assert BNMTF.beta == beta
    assert numpy.array_equal(BNMTF.lambdaF,lambdaF)
    assert numpy.array_equal(BNMTF.lambdaS,lambdaS)
    assert numpy.array_equal(BNMTF.lambdaG,lambdaG)
    
    
""" Test initialing parameters """
def test_initialise():
    I,J,K,L = 5,3,2,4
    R = numpy.ones((I,J))
    M = numpy.ones((I,J))
    
    lambdaF = 2*numpy.ones((I,K))
    lambdaS = 3*numpy.ones((K,L))
    lambdaG = 4*numpy.ones((J,L))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    # Initialisation without custom values
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.initialise()
    
    assert BNMTF.alpha_s == alpha
    assert BNMTF.beta_s == beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMTF.tauF[i,k] == 1.
        assert BNMTF.muF[i,k] == 1./lambdaF[i,k]
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        assert BNMTF.tauS[k,l] == 1.
        assert BNMTF.muS[k,l] == 1./lambdaS[k,l]
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        assert BNMTF.tauG[j,l] == 1.
        assert BNMTF.muG[j,l] == 1./lambdaG[j,l]
        
    # Test whether the expectation and variance values are correctly computed
    assert BNMTF.exptau == alpha/beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert abs(BNMTF.expF[i,k] - (0.5 + 0.352065 / (1-0.3085))) < 0.0001
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        assert abs(BNMTF.expS[k,l] - (1./3. + 0.377383 / (1-0.3694))) < 0.0001
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        assert abs(BNMTF.expG[j,l] - (1./4. + 0.386668 / (1-0.4013))) < 0.0001
    
    # Then initialise with predefined values. First override muF, tauS, tauG, alpha_s
    values1 = {
        'muF' : numpy.ones((I,K))*100, 
        'tauS' : numpy.ones((K,L))*5, 
        'tauG' : numpy.ones((J,L))*15, 
        'alpha_s' : 12.
    
    }
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.initialise(values1)
    
    assert BNMTF.alpha_s == 12.
    assert BNMTF.beta_s == beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMTF.tauF[i,k] == 1.
        assert BNMTF.muF[i,k] == 100.
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        assert BNMTF.tauS[k,l] == 5.
        assert BNMTF.muS[k,l] == 1./lambdaS[k,l]
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        assert BNMTF.tauG[j,l] == 15.
        assert BNMTF.muG[j,l] == 1./lambdaG[j,l]
        
    # Then override tauF, muS, muG, beta_s
    values2 = {
        'tauF' : numpy.ones((I,K))*10,
        'muS' : numpy.ones((K,L))*200,
        'muG' : numpy.ones((J,L))*300,
        'beta_s' : 13.
    }
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.initialise(values2)
    
    assert BNMTF.alpha_s == alpha
    assert BNMTF.beta_s == 13.
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMTF.tauF[i,k] == 10.
        assert BNMTF.muF[i,k] == 1./lambdaF[i,k]
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        assert BNMTF.tauS[k,l] == 1.
        assert BNMTF.muS[k,l] == 200.
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        assert BNMTF.tauG[j,l] == 1.
        assert BNMTF.muG[j,l] == 300.
        
        
""" Test computing the ELBO. """
def test_elbo():
    #TODO:
    return
    
        
""" Test updating parameters U, V, tau """          
I,J,K,L = 5,3,2,4
R = numpy.ones((I,J))
M = numpy.ones((I,J))
M[0,0], M[2,2], M[3,1] = 0, 0, 0 # size Omega = 12

lambdaF = 2*numpy.ones((I,K))
lambdaS = 3*numpy.ones((K,L))
lambdaG = 4*numpy.ones((J,L))
alpha, beta = 3, 1
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }

def test_exp_square_diff():
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.expF = 1./lambdaF #[[1./2.]]
    BNMTF.expS = 1./lambdaS #[[1./3.]]
    BNMTF.expG = 1./lambdaG #[[1./4.]]
    BNMTF.varF = numpy.ones((I,K))*2 #[[2.]]
    BNMTF.varS = numpy.ones((K,L))*3 #[[3.]]
    BNMTF.varG = numpy.ones((J,L))*4 #[[4.]]
    # expF * expS * expV.T = [[1./3.]]. (varF+expF^2)=2.25, (varS+expS^2)=3.+1./9., (varG+expG^2)=4.0625
    exp_square_diff = 2735+1./6. #12.*(4./9.) + 12.*(2*4*(2.25*(3.+1./9.)*4.0625-1./4.*1./9.*1./16.)) 
    assert abs(BNMTF.exp_square_diff() - exp_square_diff) < 0.000000000001

def test_update_tau():
    BNMF = bnmtf_vb(R,M,K,L,priors)
    BNMF.expF = 1./lambdaF #[[1./2.]]
    BNMF.expS = 1./lambdaS #[[1./3.]]
    BNMF.expG = 1./lambdaG #[[1./4.]]
    BNMF.varF = numpy.ones((I,K))*2 #[[2.]]
    BNMF.varS = numpy.ones((K,L))*3 #[[3.]]
    BNMF.varG = numpy.ones((J,L))*4 #[[4.]]
    BNMF.update_tau()
    assert BNMF.alpha_s == alpha + 12./2.
    assert abs(BNMF.beta_s - (beta + (2735+1./6.)/2.)) < 0.000000000001
    
def test_update_F():
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        BNMTF.muF = numpy.zeros((I,K))
        BNMTF.tauF = numpy.zeros((I,K))
        BNMTF.expF = 1./lambdaF #[[1./2.]]
        BNMTF.expS = 1./lambdaS #[[1./3.]]
        BNMTF.expG = 1./lambdaG #[[1./4.]]
        BNMTF.varF = numpy.ones((I,K))*2 #[[2.]]
        BNMTF.varS = numpy.ones((K,L))*3 #[[3.]]
        BNMTF.varG = numpy.ones((J,L))*4 #[[4.]]
        BNMTF.exptau = 3.
        BNMTF.update_F(i,k)
        
        tauFik = 3. * sum([
            sum([BNMTF.expS[k,l]*BNMTF.expG[j,l] for l in range(0,L)])**2 \
            + sum([(BNMTF.varS[k,l]+BNMTF.expS[k,l]**2)*(BNMTF.varG[j,l]+BNMTF.expG[j,l]**2) - BNMTF.expS[k,l]**2*BNMTF.expG[j,l]**2 for l in range(0,L)])
        for j in range(0,J) if M[i,j]])
        muFik = (1./tauFik) * ( -2. + BNMTF.exptau * sum([     
            (sum([BNMTF.expS[k,l]*BNMTF.expG[j,l] for l in range(0,L)]))*(R[i,j] - sum([
                BNMTF.expF[i,kp]*BNMTF.expS[kp,l]*BNMTF.expG[j,l]
            for kp,l in itertools.product(xrange(0,K),xrange(0,L)) if kp != k]))
        for j in range(0,J) if M[i,j]]))
            
        assert BNMTF.tauF[i,k] == tauFik
        assert BNMTF.muF[i,k] == muFik
    
def test_update_S():
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        BNMTF.muS = numpy.zeros((K,L))
        BNMTF.tauS = numpy.zeros((K,L))
        BNMTF.expF = 1./lambdaF #[[1./2.]]
        BNMTF.expS = 1./lambdaS #[[1./3.]]
        BNMTF.expG = 1./lambdaG #[[1./4.]]
        BNMTF.varF = numpy.ones((I,K))*2 #[[2.]]
        BNMTF.varS = numpy.ones((K,L))*3 #[[3.]]
        BNMTF.varG = numpy.ones((J,L))*4 #[[4.]]
        BNMTF.exptau = 3.
        BNMTF.update_S(k,l)
        
        tauSkl = 3. * sum([
            BNMTF.expF[i,k]**2 * BNMTF.expG[j,l]**2 \
            + (BNMTF.varF[i,k]+BNMTF.expF[i,k]**2)*(BNMTF.varG[j,l]+BNMTF.expG[j,l]**2) - BNMTF.expF[i,k]**2*BNMTF.expG[j,l]**2
        for i,j in itertools.product(xrange(0,I),xrange(0,J)) if M[i,j]])
        muSkl = (1./tauSkl) * ( -3. + BNMTF.exptau * sum([     
            BNMTF.expF[i,k]*BNMTF.expG[j,l] * (R[i,j] - sum([
                BNMTF.expF[i,kp]*BNMTF.expS[kp,lp]*BNMTF.expG[j,lp]
            for kp,lp in itertools.product(xrange(0,K),xrange(0,L)) if (kp != k or lp != l)]))
        for i,j in itertools.product(xrange(0,I),xrange(0,J)) if M[i,j]]))
            
        assert BNMTF.tauS[k,l] == tauSkl
        assert BNMTF.muS[k,l] == muSkl
    
def test_update_G():
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        BNMTF.muG = numpy.zeros((J,L))
        BNMTF.tauG = numpy.zeros((J,L))
        BNMTF.expF = 1./lambdaF #[[1./2.]]
        BNMTF.expS = 1./lambdaS #[[1./3.]]
        BNMTF.expG = 1./lambdaG #[[1./4.]]
        BNMTF.varF = numpy.ones((I,K))*2 #[[2.]]
        BNMTF.varS = numpy.ones((K,L))*3 #[[3.]]
        BNMTF.varG = numpy.ones((J,L))*4 #[[4.]]
        BNMTF.exptau = 3.
        BNMTF.update_G(j,l)
        
        tauGjl = 3. * sum([
            sum([BNMTF.expF[i,k]*BNMTF.expS[k,l] for k in range(0,K)])**2 \
            + sum([(BNMTF.varS[k,l]+BNMTF.expS[k,l]**2)*(BNMTF.varF[i,k]+BNMTF.expF[i,k]**2) - BNMTF.expS[k,l]**2*BNMTF.expF[i,k]**2 for k in range(0,K)])
        for i in range(0,I) if M[i,j]])
        muGjl = (1./tauGjl) * ( -4. + BNMTF.exptau * sum([     
            (sum([BNMTF.expS[k,l]*BNMTF.expF[i,k] for k in range(0,K)]))*(R[i,j] - sum([
                BNMTF.expF[i,k]*BNMTF.expS[k,lp]*BNMTF.expG[j,lp]
            for k,lp in itertools.product(xrange(0,K),xrange(0,L)) if lp != l]))
        for i in range(0,I) if M[i,j]]))
        
        assert BNMTF.tauG[j,l] == tauGjl
        assert BNMTF.muG[j,l] == muGjl


""" Test computing expectation, variance F, S, G, tau """     
def test_update_exp_F():
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        values = { 'tauF' : 4*numpy.ones((I,K)) }
        BNMTF.initialise(values) # muF = [[0.5]], tauF = [[4.]]
        BNMTF.update_exp_F(i,k) #-mu*sqrt(tau) = -0.5*2 = -1. lambda(1) = 0.241971 / (1-0.1587) = 0.2876155949126352. gamma = 0.37033832534958433
        assert abs(BNMTF.expF[i,k] - (0.5 + 1./2. * 0.2876155949126352)) < 0.00001
        assert abs(BNMTF.varF[i,k] - 1./4.*(1.-0.37033832534958433)) < 0.00001

def test_update_exp_S():
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        values = { 'tauS' : 4*numpy.ones((K,L)) }
        BNMTF.initialise(values) # muS = [[1./3.]], tauS = [[4.]]
        BNMTF.update_exp_S(k,l) #-mu*sqrt(tau) = -2./3., lambda(..) = 0.319448 / (1-0.2525) = 0.4273551839464883, gamma = 
        assert abs(BNMTF.expS[k,l] - (1./3. + 1./2. * 0.4273551839464883)) < 0.00001
        assert abs(BNMTF.varS[k,l] - 1./4.*(1. - 0.4675359092102624)) < 0.00001

def test_update_exp_G():
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        BNMTF = bnmtf_vb(R,M,K,L,priors)
        values = { 'tauG' : 4*numpy.ones((J,L)) }
        BNMTF.initialise(values) # muG = [[1./4.]], tauG = [[4.]]
        BNMTF.update_exp_G(j,l) #-mu*sqrt(tau) = -0.5., lambda(..) = 0.352065 / (1-0.3085) = 0.5091323210412148, gamma = 0.5137818808494219
        assert abs(BNMTF.expG[j,l] - (1./4. + 1./2. * 0.5091323210412148)) < 0.0001
        assert abs(BNMTF.varG[j,l] - 1./4.*(1. - 0.5137818808494219)) < 0.0001
    
def test_update_exp_tau():
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.initialise()  
    BNMTF.update_exp_tau()
    assert BNMTF.exptau == 3.
    assert BNMTF.explogtau == 0.9227843350984671393934879099175975689578406640600764 - 0.
    

""" Test two iterations of run(), and that all values have changed. """
def test_run():
    I,J,K,L = 10,5,3,2
    R = numpy.ones((I,J))
    M = numpy.ones((I,J))
    M[0,0], M[2,2], M[3,1] = 0, 0, 0
    R[0,1], R[0,2] = 2., 3.
    
    lambdaF = 2*numpy.ones((I,K))
    lambdaS = 3*numpy.ones((K,L))
    lambdaG = 4*numpy.ones((J,L))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    iterations = 2
    
    BNMF = bnmtf_vb(R,M,K,L,priors)
    BNMF.initialise()
    BNMF.run(iterations)
    
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMF.muF[i,k] != 1./lambdaF[i,k]
        assert BNMF.tauF[i,k] != 1.
        assert BNMF.expF[i,k] != numpy.inf and not math.isnan(BNMF.expF[i,k])
        assert BNMF.tauF[i,k] != numpy.inf and not math.isnan(BNMF.tauF[i,k])
    for k,l in itertools.product(xrange(0,K),xrange(0,L)):
        assert BNMF.muS[k,l] != 1./lambdaS[k,l]
        assert BNMF.tauS[k,l] != 1.
        assert BNMF.expS[k,l] != numpy.inf and not math.isnan(BNMF.expS[k,l])
        assert BNMF.tauS[k,l] != numpy.inf and not math.isnan(BNMF.tauS[k,l])
    for j,l in itertools.product(xrange(0,J),xrange(0,L)):
        assert BNMF.muG[j,l] != 1./lambdaG[j,l]
        assert BNMF.tauG[j,l] != 1.
        assert BNMF.expG[j,l] != numpy.inf and not math.isnan(BNMF.expG[j,l])
        assert BNMF.tauG[j,l] != numpy.inf and not math.isnan(BNMF.tauG[j,l])
    assert BNMF.alpha_s != alpha
    assert BNMF.beta_s != beta
    assert BNMF.exptau != numpy.inf and not math.isnan(BNMF.exptau)
    assert BNMF.explogtau != numpy.inf and not math.isnan(BNMF.explogtau)
    

""" Test computing the performance of the predictions using the expectations """
def test_predict():
    (I,J,K) = (5,3,2)
    R = numpy.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]],dtype=float)
    M = numpy.ones((I,J))
    K = 3
    lambdaF = 2*numpy.ones((I,K))
    lambdaS = 3*numpy.ones((K,L))
    lambdaG = 5*numpy.ones((J,L))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    expF = numpy.array([[125.,126.],[126.,126.],[126.,126.],[126.,126.],[126.,126.]])
    expS = numpy.array([[84.,84.,84.,84.],[84.,84.,84.,84.]])
    expG = numpy.array([[42.,42.,42.,42.],[42.,42.,42.,42.],[42.,42.,42.,42.]])
    
    M_test = numpy.array([[0,0,1],[0,1,0],[0,0,0],[1,1,0],[0,0,0]]) #R->3,5,10,11, R_pred->3542112,3556224,3556224,3556224
    MSE = ((3.-3542112.)**2 + (5.-3556224.)**2 + (10.-3556224.)**2 + (11.-3556224.)**2) / 4.
    R2 = 1. - ((3.-3542112.)**2 + (5.-3556224.)**2 + (10.-3556224.)**2 + (11.-3556224.)**2) / (4.25**2+2.25**2+2.75**2+3.75**2) #mean=7.25
    Rp = 357. / ( math.sqrt(44.75) * math.sqrt(5292.) ) #mean=7.25,var=44.75, mean_pred=3552696,var_pred=5292, corr=(-4.25*-63 + -2.25*21 + 2.75*21 + 3.75*21)
    
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    BNMTF.expF = expF
    BNMTF.expS = expS
    BNMTF.expG = expG
    performances = BNMTF.predict(M_test)
    
    assert performances['MSE'] == MSE
    assert performances['R^2'] == R2
    assert performances['Rp'] == Rp
       
        
""" Test the evaluation measures MSE, R^2, Rp """
def test_compute_statistics():
    R = numpy.array([[1,2],[3,4]],dtype=float)
    M = numpy.array([[1,1],[0,1]])
    I, J, K, L = 2, 2, 3, 4
    lambdaF = 2*numpy.ones((I,K))
    lambdaS = 3*numpy.ones((K,L))
    lambdaG = 4*numpy.ones((J,L))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }
    
    BNMTF = bnmtf_vb(R,M,K,L,priors)
    
    R_pred = numpy.array([[500,550],[1220,1342]],dtype=float)
    M_pred = numpy.array([[0,0],[1,1]])
    
    MSE_pred = (1217**2 + 1338**2) / 2.0
    R2_pred = 1. - (1217**2+1338**2)/(0.5**2+0.5**2) #mean=3.5
    Rp_pred = 61. / ( math.sqrt(.5) * math.sqrt(7442.) ) #mean=3.5,var=0.5,mean_pred=1281,var_pred=7442,cov=61
    
    assert MSE_pred == BNMTF.compute_MSE(M_pred,R,R_pred)
    assert R2_pred == BNMTF.compute_R2(M_pred,R,R_pred)
    assert Rp_pred == BNMTF.compute_Rp(M_pred,R,R_pred)
    