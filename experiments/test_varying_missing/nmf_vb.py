"""
Test the performance of Variational Bayes for recovering a toy dataset, where 
we vary the fraction of entries that are missing.
We repeat this 10 times per fraction and average that.

We use the correct number of latent factors and same priors as used to generate the data.

I, J, K = 100, 80, 10
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_vb_optimised import bnmf_vb_optimised
from BNMTF.experiments.generate_toy.bnmf.generate_bnmf import try_generate_M
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

fractions_unknown = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmf/"

repeats = 10 # number of times we try each fraction
iterations = 1000
I,J,K = 100, 80, 10 #20,10,3 #

alpha, beta = 1., 1.
lambdaU = numpy.ones((I,K))/10.
lambdaV = numpy.ones((J,K))/10.    
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

init_UV = 'random'

metrics = ['MSE', 'R^2', 'Rp']


#'''
# Load in data
R = numpy.loadtxt(input_folder+"R.txt")


# Generate matrices M - one list of M's for each fraction
M_attempts = 100
all_Ms = [ 
    [try_generate_M(I,J,fraction,M_attempts) for r in range(0,repeats)]
    for fraction in fractions_unknown
]
all_Ms_test = [ [calc_inverse_M(M) for M in Ms] for Ms in all_Ms ]


# Make sure each M has no empty rows or columns
def check_empty_rows_columns(M,fraction):
    sums_columns = M.sum(axis=0)
    sums_rows = M.sum(axis=1)
    for i,c in enumerate(sums_rows):
        assert c != 0, "Fully unobserved row in M, row %s. Fraction %s." % (i,fraction)
    for j,c in enumerate(sums_columns):
        assert c != 0, "Fully unobserved column in M, column %s. Fraction %s." % (j,fraction)
        
for Ms,fraction in zip(all_Ms,fractions_unknown):
    for M in Ms:
        check_empty_rows_columns(M,fraction)


# We now run the VB algorithm on each of the M's for each fraction.
all_performances = {metric:[] for metric in metrics} 
average_performances = {metric:[] for metric in metrics} # averaged over repeats
for (fraction,Ms,Ms_test) in zip(fractions_unknown,all_Ms,all_Ms_test):
    print "Trying fraction %s." % fraction
    
    # Run the algorithm <repeats> times and store all the performances
    for metric in metrics:
        all_performances[metric].append([])
    for (repeat,M,M_test) in zip(range(0,repeats),Ms,Ms_test):
        print "Repeat %s of fraction %s." % (repeat+1, fraction)
    
        BNMF = bnmf_vb_optimised(R,M,K,priors)
        BNMF.initialise(init_UV)
        BNMF.run(iterations)
    
        # Measure the performances
        performances = BNMF.predict(M_test)
        for metric in metrics:
            # Add this metric's performance to the list of <repeat> performances for this fraction
            all_performances[metric][-1].append(performances[metric])
            
    # Compute the average across attempts
    for metric in metrics:
        average_performances[metric].append(sum(all_performances[metric][-1])/repeats)
    
    
print "repeats=%s \nfractions_unknown = %s \nall_performances = %s \naverage_performances = %s" % \
    (repeats,fractions_unknown,all_performances,average_performances)


'''
repeats=10 
fractions_unknown = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] 
all_performances = {'R^2': [[0.9683884038267335, 0.9646169881339781, 0.9664777405474239, 0.9670287785874833, 0.9624240881702343, 0.9680355038256945, 0.9719307299997457, 0.9629826925022824, 0.9602855205649463, 0.9686705195002323], [0.9653987822562707, 0.9636273772329373, 0.9640673367298059, 0.966066739890249, 0.9633793377232198, 0.9679830987986853, 0.9620785803612693, 0.96082553183301, 0.9661693135001368, 0.9663244944657601], [0.9617930248094203, 0.9642355392384485, 0.9627655889098621, 0.9634443979607432, 0.9596607722421969, 0.9578754064932169, 0.9624082866584496, 0.9538263576952851, 0.9618078543645939, 0.963271891900556], [0.9599720724228168, 0.9589949486255698, 0.9624692958301866, 0.9600292193732625, 0.9586718181830132, 0.9644936230314554, 0.9601011113115265, 0.9582402555176157, 0.9610914150598637, 0.9568099713514397], [0.9510575870994907, 0.953133159466471, 0.9572018168117287, 0.9555886955604032, 0.9562238953027933, 0.9535614336904481, 0.9573252257504995, 0.9524315798133682, 0.9529882110179831, 0.9542089981937436], [0.9415774776278928, 0.9422029887451251, 0.9442776105339002, 0.9389233420029472, 0.9391074784542185, 0.9398795777026226, 0.9422419596592234, 0.9456691395310083, 0.9468243139570814, 0.9398076162947815], [0.9195686981189897, 0.9079605465864389, 0.9078082797884448, 0.9220014020277639, 0.9108287430753849, 0.9037028915591239, 0.912591476608551, 0.918270531533928, 0.9188651953510093, 0.9179806928033701], [0.6920410395599819, 0.6008746365040979, 0.5866015587287425, 0.6186019054564796, 0.5668339370408491, 0.6094993454431883, 0.6132762475293851, 0.49265601928467573, 0.6022068381761583, 0.5266814373578397], [0.498127855582871, 0.46276570487837276, 0.4688479204125017, 0.4643276992518711, 0.485925226956077, 0.47531296302186266, 0.47253208953783354, 0.4575697706092281, 0.32915747811593643, 0.3982904426552035]], 'MSE': [[1.3307806443295218, 1.3860030221750916, 1.3491865404494512, 1.2629440098447298, 1.3525845995372878, 1.3265179972285617, 1.3099149226729085, 1.3020277237977143, 1.4601402263219909, 1.2513376147112634], [1.435952160790894, 1.4303848268759256, 1.3641094842905677, 1.3897974028163187, 1.4508505446515516, 1.3585230505898929, 1.4387783797472564, 1.4369681270833714, 1.3365463498588703, 1.3972466786242712], [1.4560875651344829, 1.4162829303391684, 1.4619786232698355, 1.4634447984464445, 1.419116277117898, 1.5617928762366986, 1.4340335524769894, 1.5602103918913377, 1.4913875309554596, 1.434913867582116], [1.6041488253096432, 1.5757054761400267, 1.51638250689182, 1.6144003105634825, 1.5879065992141508, 1.5553875416864309, 1.5117231920229905, 1.6480661011771951, 1.6104213492947808, 1.5746276392092045], [1.8249532954410042, 1.8684675176149066, 1.6884323641027121, 1.7357984294610043, 1.7600831122286691, 1.7602824360794105, 1.7541479574284402, 1.8496812642592837, 1.8017840734869119, 1.8028886582045112], [2.2830756844552869, 2.3381965848102286, 2.216514115860623, 2.3093143677485344, 2.3415264238240638, 2.2899284412993794, 2.2271667169283544, 2.1963148167304456, 2.0830955631671704, 2.4138472512538964], [3.1232560756434995, 3.5500566611187123, 3.5434235337850692, 3.1256896633925706, 3.5094838277923319, 3.7894116899659496, 3.3721896132320386, 3.1328631528840871, 3.1814614927189346, 3.2612035339698324], [12.285753990084888, 15.358471185031494, 16.052806094752338, 14.905585025277116, 16.848948739652801, 15.506789499794692, 14.846760598929515, 20.165428714525419, 15.641343624014961, 18.888603197701336], [19.91181911887352, 21.089792265365787, 20.820169006409735, 21.111090007086695, 20.383431673137796, 20.692187943371938, 20.931366119129279, 21.338393635409702, 26.574615383488879, 23.191480741378562]], 'Rp': [[0.98417814296283501, 0.98223400580549158, 0.98310326759249378, 0.98340722606591879, 0.98109337471923375, 0.98404390169079525, 0.98592775532569599, 0.98131947992398216, 0.97998468118843007, 0.98422609008714801], [0.9826101986875232, 0.98164905167945748, 0.98193816637754328, 0.98290389426688474, 0.98154124970139101, 0.98390533314231476, 0.98101064425676598, 0.98026353532428501, 0.98297973175637066, 0.98305830615657197], [0.98078317148555072, 0.98198414505700715, 0.98122073773732377, 0.98155713977161774, 0.97963966020841486, 0.97874970585541088, 0.98104144030097185, 0.97667120348535452, 0.98076429936402731, 0.98151649299554744], [0.97994720265290991, 0.97937813547381558, 0.98107978700989862, 0.97983062508002172, 0.97919011307640369, 0.98208889140778566, 0.97990775152411236, 0.97892552090575269, 0.98035357770873099, 0.97823011129973625], [0.97527494390058556, 0.97661348931923153, 0.97847670949617727, 0.97768219832746694, 0.9778798337102893, 0.97658532879410387, 0.97851222466341137, 0.97598467728753147, 0.97623619637760939, 0.97694115727467978], [0.97039259977702308, 0.97073350305394834, 0.97179438232063309, 0.96901986600092904, 0.96919448091426885, 0.96948570832841707, 0.9707251134658279, 0.97246199162764579, 0.97310098700035219, 0.9694711588036119], [0.95912297665582935, 0.95332670849063539, 0.95288766098517352, 0.9602238588797064, 0.95446281935606847, 0.95093148902935831, 0.95553021872522659, 0.95856275340635955, 0.95885273967483775, 0.95837112445540062], [0.83309959117472532, 0.78392590768509252, 0.78228908789976048, 0.79230555909437228, 0.77539309469738738, 0.79410490646410281, 0.7990139950108649, 0.73383952871177027, 0.78463353986423079, 0.74223137952499108], [0.73535887538412503, 0.72700259454644678, 0.72810312108849651, 0.73051322809824903, 0.73276297324422102, 0.73165859759103224, 0.73380231876238378, 0.71376455057499144, 0.67766815789763035, 0.70196034943723151]]} 
average_performances = {'R^2': [0.96608409656587535, 0.96459205927913449, 0.96110891202727733, 0.96008737307067504, 0.95437206027069299, 0.94205115045088017, 0.91395784574530037, 0.5909272965081398, 0.4512857151021758], 'MSE': [1.3331437301068518, 1.4039157005328922, 1.4699248413450432, 1.5798769541509725, 1.7846519108306853, 2.2698979966077983, 3.3589039244503018, 16.050049066976456, 21.604434589365191], 'Rp': [0.98295179253620246, 0.98218601113491089, 0.98039279962612258, 0.97989317161391676, 0.97701867591510871, 0.97063797912926564, 0.9562272349658596, 0.78208365901272991, 0.72125947666248069]}
'''


# Plot the MSE, R^2 and Rp
for metric in metrics:
    plt.figure()
    x = fractions_unknown
    y = average_performances[metric]
    plt.plot(x,y)
    plt.xlabel("Fraction missing")
    plt.ylabel(metric)