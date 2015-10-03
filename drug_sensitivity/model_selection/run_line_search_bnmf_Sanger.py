"""
Run the line search for BNMF with the Exp priors on the Sanger dataset.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_vb_optimised import bnmf_vb_optimised
from ml_helpers.code.mask import compute_Ms, compute_folds
from load_data import load_Sanger
from BNMTF.grid_search.line_search_bnmf import LineSearch

import numpy, matplotlib.pyplot as plt

##########

standardised = False #standardised Sanger or unstandardised
no_folds = 5

restarts = 5
iterations = 1000
I, J = 622,139
values_K = range(31,35+1)

alpha, beta = 1., 1.
lambdaU = 1./10.
lambdaV = 1./10.
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

initUV = 'random'

classifier = bnmf_vb_optimised

# Load in data
(_,X_min,M,_,_,_,_) = load_Sanger(standardised=standardised)

folds_test = compute_folds(I,J,no_folds,M)
folds_training = compute_Ms(folds_test)
(M_train,M_test) = (folds_training[0],folds_test[0])

# Run the line search
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
line_search = LineSearch(classifier,values_K,X_min,M,priors,initUV,iterations,restarts=restarts)
line_search.search()

# Plot the performances of all four metrics
metrics = ['loglikelihood', 'BIC', 'AIC', 'MSE']
for metric in metrics:
    plt.figure()
    plt.plot(values_K, line_search.all_values(metric), label=metric)
    plt.legend(loc=3)
    
# Also print out all values in a dictionary
all_values = {}
for metric in metrics:
    all_values[metric] = line_search.all_values(metric)
    
print "all_values = %s" % all_values

'''
{'MSE': [3.0272045267867274, 2.5912982754926035, 2.3421361670917507, 2.1573447121174634, 2.0038243331243812, 1.8784259845268056, 1.7778387476966746, 1.708180464480777, 1.6429264869512277, 1.5743544560258957, 1.510963466212312, 1.4556030378512141, 1.4067992849188964, 1.352139317817434, 1.3038794309418051, 1.265443621895456, 1.2243072291024002, 1.189433738928334, 1.1561686922108647, 1.1175032736906385, 1.099602385471328, 1.065927015135751, 1.0453144714407552, 1.0110553320228033, 0.9900637907148588, 0.9618433024411556, 0.9409466977604016, 0.9184613303413715, 0.8959982159749676, 0.8790987197787278, 0.8602390454615657, 0.8410291237019341, 0.8200472590231683, 0.8036247007036755, 0.7909117242781721], 'loglikelihood': [-138379.73196191844, -132933.00697960873, -129397.98415939865, -126530.57279572886, -123960.73414372109, -121717.61056828291, -119814.62465031014, -118439.74426996421, -117111.14221036198, -115654.9915051248, -114264.97943092373, -113001.03622466451, -111856.12078137076, -110526.01789023768, -109321.18170649008, -108334.38968303277, -107257.48599766825, -106317.5299180052, -105395.42369197553, -104299.4118339516, -103791.11489491147, -102798.67578921128, -102188.75536988786, -101136.18855606556, -100483.28212715489, -99600.8398849109, -98935.61539521479, -98205.48454652501, -97443.1671045164, -96885.48032223292, -96231.39129112643, -95585.43415547578, -94864.8409259289, -94256.10530471621, -93802.97167136439], 'AIC': [278281.4639238369, 268910.01395921747, 263361.9683187973, 259149.14559145772, 255531.46828744217, 252567.22113656581, 250283.2493006203, 249055.48853992842, 247920.28442072397, 246529.9830102496, 245271.95886184747, 244266.07244932902, 243498.24156274152, 242360.03578047536, 241472.36341298016, 241020.77936606554, 240388.9719953365, 240031.0598360104, 239708.84738395107, 239038.8236679032, 239544.22978982294, 239081.35157842256, 239383.51073977572, 238800.37711213113, 239016.56425430978, 238773.6797698218, 238965.23079042957, 239026.96909305002, 239024.3342090328, 239430.96064446584, 239644.78258225287, 239874.86831095157, 239955.6818518578, 240260.21060943243, 240875.94334272877], 'BIC': [285250.93444804713, 282848.955007638, 284270.3798914281, 287027.0276882988, 290378.82090849354, 294384.0442818274, 299069.54297009215, 304811.25273361057, 310645.5191386164, 316224.6882523523, 321936.1346281604, 327899.71873985225, 334101.358377475, 339932.6231194191, 346014.4212761342, 352532.30775342986, 358869.97090691107, 365481.5292717952, 372128.78734394617, 378428.23415210855, 385903.11079823854, 392409.70311104844, 399681.33279661194, 406067.66969317757, 413253.32735956647, 419979.9133992888, 427140.93494410685, 434172.1437709376, 441138.97941113054, 448515.0763707739, 455698.3688327712, 462897.92508568015, 469948.2091507967, 477222.20843258157, 484807.41169008816]}
'''