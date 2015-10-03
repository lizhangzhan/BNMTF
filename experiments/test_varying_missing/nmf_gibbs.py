"""
Test the performance of Gibbs sampling for recovering a toy dataset, where we 
vary the fraction of entries that are missing.
We repeat this 10 times per fraction and average that.

We use the correct number of latent factors and same priors as used to generate the data.

I, J, K = 100, 80, 10
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmf_gibbs_optimised import bnmf_gibbs_optimised
from BNMTF.experiments.generate_toy.bnmf.generate_bnmf import try_generate_M
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

fractions_unknown = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

input_folder = project_location+"BNMTF/experiments/generate_toy/bnmf/"

repeats = 10 # number of times we try each fraction
iterations = 1000
burn_in = 800
thinning = 5

init_UV = 'random'
I,J,K = 100, 80, 10

alpha, beta = 1., 1.
lambdaU = numpy.ones((I,K))/10.
lambdaV = numpy.ones((J,K))/10.    
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

metrics = ['MSE', 'R^2', 'Rp']

#'''
# Load in data
R = numpy.loadtxt(input_folder+"R.txt")

# Seed all of the methods the same
numpy.random.seed(3)

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


# We now run the Gibbs sampler on each of the M's for each fraction.
all_performances = {metric:[] for metric in metrics} 
average_performances = {metric:[] for metric in metrics} # averaged over repeats
for (fraction,Ms,Ms_test) in zip(fractions_unknown,all_Ms,all_Ms_test):
    print "Trying fraction %s." % fraction
    
    # Run the algorithm <repeats> times and store all the performances
    for metric in metrics:
        all_performances[metric].append([])
    for (repeat,M,M_test) in zip(range(0,repeats),Ms,Ms_test):
        print "Repeat %s of fraction %s." % (repeat+1, fraction)
    
        BNMF = bnmf_gibbs_optimised(R,M,K,priors)
        BNMF.initialise(init_UV)
        BNMF.run(iterations)
    
        # Measure the performances
        performances = BNMF.predict(M_test,burn_in,thinning)
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
all_performances = {'R^2': [[0.9619059001208281, 0.9640827667211137, 0.9694512746263138, 0.9701886721742091, 0.9657569043522852, 0.9645199588372723, 0.9634705713931656, 0.9676267917708213, 0.9675622254798245, 0.9684506981142136], [0.9661983256111081, 0.9616205514088321, 0.964782466321369, 0.9642198246274559, 0.9609647615999493, 0.9645080846532873, 0.9628567568565517, 0.9625100016209683, 0.9647052208065231, 0.9617419670924906], [0.9643234840870709, 0.9617430678118996, 0.961338418396636, 0.9621685540717345, 0.9590790976588984, 0.9630979205180834, 0.9648309654552717, 0.9610122836488321, 0.961987672033106, 0.9612220362972822], [0.9595101862277302, 0.9594776094947263, 0.957823871926474, 0.9570380281896163, 0.9565386172828394, 0.9598820325488254, 0.9578290274243525, 0.9568794205531495, 0.9614822869442783, 0.9590428076940245], [0.9522941300113166, 0.9592824357136986, 0.9523343094760195, 0.9530924121407341, 0.9545449371032484, 0.9552885193209901, 0.9535007755625815, 0.9533325771726907, 0.9538848182936318, 0.9526588158499125], [0.9431535719627517, 0.9430805152703715, 0.9438988157247572, 0.939609300028728, 0.9419858916360788, 0.9414720533278618, 0.9431853506983003, 0.9450629953350186, 0.9420390340603483, 0.940740567078019], [0.907184519966465, 0.8893815616999061, 0.8947153607127359, 0.9210263887880934, 0.9165479957564602, 0.9011617012566961, 0.914193937886436, 0.9096273664291488, 0.8954458717355149, 0.9141336520293362], [0.7156007465858046, 0.6608549871190714, 0.5081403620663952, 0.5878899388839927, 0.569112134184095, 0.5922612076738332, 0.6788791286000178, 0.6756450333289706, 0.6368380147278165, 0.6412391457100886], [-0.03883065769894101, 0.39937236004066956, 0.28768810475157225, 0.09263549338150567, 0.3168058803008834, -0.09290240474776601, 0.35323399570551717, 0.3214323519141459, 0.4174905865373635, 0.33869715838260983]], 'MSE': [[1.3435161026525739, 1.422961444249444, 1.3631881946753663, 1.2758401195570195, 1.3723055080209405, 1.3591839088535866, 1.3073380616795633, 1.2759250524622099, 1.3171618674650449, 1.3008268160586309], [1.4052993493654045, 1.4061825751225325, 1.4145324544645925, 1.416226609062057, 1.3686757539628065, 1.3963021810316414, 1.3295080392294472, 1.413876209948091, 1.3895909892824541, 1.419473598871462], [1.4527645268465443, 1.4826447252288502, 1.4254506857209015, 1.4201453258828076, 1.5561327664672613, 1.3896139933122358, 1.4093211449035519, 1.496694920695091, 1.5080125674525022, 1.4776551431702634], [1.6273693364025781, 1.5613122281634206, 1.6454573438972488, 1.5741174307843806, 1.6605585104955143, 1.5484879861149485, 1.5673643158482429, 1.602940012847651, 1.583455906458755, 1.6025335487371899], [1.8894807573583676, 1.7080057208270207, 1.8633500585485623, 1.7974722582784888, 1.8347187228173907, 1.7174347001477308, 1.8581357148871396, 1.929932788496548, 1.8084403552739736, 1.913959453942534], [2.2776321156547823, 2.1936042177364317, 2.2241365566054401, 2.3483636322993302, 2.3154926960962983, 2.2067045058831347, 2.2426850409475771, 2.1446587159580708, 2.2992147876063465, 2.2943319870938215], [3.7685336471769131, 4.3642248206791576, 4.1420738260722327, 3.1913847733566691, 3.16274898450681, 3.8163163270379021, 3.4308795689453064, 3.5367105688459781, 3.969659603845769, 3.4073620151958273], [11.059472488515201, 13.473029553247274, 19.291326753948525, 15.885738351988971, 16.899217668762873, 15.993607044250318, 12.602174595100042, 12.64226363202151, 14.496466797700567, 14.251389800630605], [40.67778578143124, 23.597337597218569, 27.599872865640666, 35.191150325252806, 27.086630055043276, 43.222847307391774, 25.432423502446227, 26.565062181981109, 22.777538269386849, 26.061386510100139]], 'Rp': [[0.9808300176523761, 0.98191012955331602, 0.9846447380668788, 0.98502372410143113, 0.98295436323656427, 0.98218222196692218, 0.98158559788405897, 0.98384206390239581, 0.98365853961110095, 0.98422252322658887], [0.98305770886688504, 0.98070818786031999, 0.98237072800530101, 0.98206139647059831, 0.98049188373631291, 0.98216731690336034, 0.9814417415253478, 0.98131137814915259, 0.98232864345704773, 0.98082516803012287], [0.9820606197511198, 0.9807351745160261, 0.98051949001280969, 0.98101659543957065, 0.97957670034473365, 0.98148427289695284, 0.98237543663511029, 0.98054936315594643, 0.98081102068623438, 0.98044887461040298], [0.97969381119965981, 0.97981830085026567, 0.97887161359914421, 0.97844051123524944, 0.97818134826056602, 0.97981148323928802, 0.97895143393769946, 0.97837373509892023, 0.98068194861727975, 0.97933890222115283], [0.97596914606319907, 0.97948998779897789, 0.97608484457282485, 0.97631491477655108, 0.97722559468427406, 0.97745619114463023, 0.97664134200129493, 0.97653440518293821, 0.97676845964285663, 0.9760570600875722], [0.97156149840243344, 0.97130590105423775, 0.97183373860842126, 0.96992716504553211, 0.97100065017491433, 0.97049381180634986, 0.97126367292558591, 0.97259156409279002, 0.97088110253196591, 0.97014609337518065], [0.95278667585694221, 0.94408340080594666, 0.94637016462172452, 0.96041168374829489, 0.95772863817233489, 0.95008710901536975, 0.95697256258891428, 0.95486074666490039, 0.94714480274787571, 0.95637229731612861], [0.85582341403166551, 0.83015757498009135, 0.76494459314321051, 0.80433937728497462, 0.79221780577170087, 0.79481080120454572, 0.84458468684503507, 0.83521337317818112, 0.82050034724166165, 0.81678073214726177], [0.67367981676225963, 0.7433971381896638, 0.70087233632151957, 0.68318666823004459, 0.69454459159521076, 0.66938293877487642, 0.73835592140083472, 0.71422274278175091, 0.74078332437265537, 0.73012959685238132]]} 
average_performances = {'R^2': [0.9663015763590048, 0.9634107960598536, 0.9620803499978814, 0.9585503888286014, 0.9540213730644822, 0.9424228095122235, 0.9063418356260794, 0.6266460698880085, 0.23956228685675604], 'MSE': [1.3338247075674379, 1.3959667760340486, 1.461843579968001, 1.5973596619749928, 1.8320930530577755, 2.2546824255881233, 3.6789894135662573, 14.659468668616592, 29.821203439589265], 'Rp': [0.9830853919201632, 0.98167641530044492, 0.98095775480489067, 0.97921630882592259, 0.97685419459551182, 0.97110051980174106, 0.95268180815384329, 0.81593727058283272, 0.70885550752811977]}
'''


# Plot the MSE, R^2 and Rp
for metric in metrics:
    plt.figure()
    x = fractions_unknown
    y = average_performances[metric]
    plt.plot(x,y)
    plt.xlabel("Fraction missing")
    plt.ylabel(metric)