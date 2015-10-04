"""
Plot the performances of the many different NMTF algorithms in a single bar chart.

We plot the average performance across all 10 attempts for different noise levels.

We have the following methods:
- VB NMTF
- Gibbs NMTF
- ICM NMTF
- Non-probabilistic NMTF
"""

import matplotlib.pyplot as plt, numpy
metrics = ['MSE'] #['MSE','R^2','Rp']

noise_ratios = [ 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5 ]
# Which noise ratios we put in the bar chart:
shown_noise_ratios = [ 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5 ] #[ 0, 0.01, 0.02, 0.05, 0.1 ]
indices_selected = [noise_ratios.index(noise) for noise in shown_noise_ratios]


# Settings for the bar chart
N = len(shown_noise_ratios) # number of bars
ind = numpy.arange(N) # x locations groups
width = 0.2 # width of bars
MSE_max = 500


# VB NMTF
vb_all_performances = {'R^2': [[0.999977568342796, 0.9961103091884986, 0.999976416968676, 0.9978496629630349, 0.9965944224635548, 0.9970765629738028, 0.9999742226731961, 0.9975393274141776, 0.9970616336921483, 0.9999865937438499], [0.9895024498316826, 0.9866051306784898, 0.9873440146192843, 0.9873333925773455, 0.9864899209692103, 0.9886907174748508, 0.9853082187591301, 0.9886593953341857, 0.9849926486286337, 0.9845696543262131], [0.9715796343964314, 0.9671422705566192, 0.9774687317189032, 0.9771123133335249, 0.9791105759273937, 0.9735900589559295, 0.9757981347285288, 0.97417772766574, 0.9758346936595138, 0.9746379955867931], [0.951720213422425, 0.963200094603104, 0.9563321237809524, 0.9399624005964081, 0.9315850485441399, 0.9225158187553606, 0.9278096565055353, 0.9347012626761187, 0.9368191106122273, 0.9459754332032912], [0.8924017009339518, 0.8660094856563707, 0.8968004136886432, 0.8964784475571275, 0.9159720852441341, 0.8853364976350075, 0.8819501546102964, 0.8933935234021028, 0.9012796409832254, 0.8784064736211331], [0.8258594708695134, 0.8178902291242944, 0.8264458232683239, 0.8164677990059468, 0.7961417238951712, 0.813937453949935, 0.8188282633186179, 0.8160161810481261, 0.8343194181355225, 0.7760189826641879], [0.621631761637544, 0.6160920987466983, 0.6489729443169876, 0.6830982146421207, 0.6320693673107713, 0.5769323565015294, 0.622055087934474, 0.5901422898631956, 0.5914397420855159, 0.6394800336132574]], 'MSE': [[0.011577282182312463, 1.9036075572177777, 0.014204792295890367, 1.1668732047976882, 1.7997327047913669, 1.5471797112727734, 0.015588258498828202, 1.1832883647923118, 1.6143579642651888, 0.0086494495858002191], [6.218526952756287, 7.3092217036942602, 6.9487941098011685, 6.7135338370204964, 7.3989471097444062, 6.1677049392027312, 7.5045089764866635, 6.9967842988002023, 8.2694784102594845, 7.4210833436226222], [13.718219115374341, 27.17317084959776, 13.70895243186694, 14.12188400028294, 13.92842920001625, 13.851161337796523, 13.404403556856794, 14.365144842410293, 12.980739135324574, 13.424036583914084], [28.270539569826077, 31.146631970409285, 30.205405492601209, 31.216750704969783, 33.57571600160113, 38.000956511201927, 44.565901178576702, 40.009940489683743, 34.999050704513465, 27.919753297482952], [73.143228907433027, 83.390404167826006, 72.919470419059209, 65.975889794181072, 75.41102307545971, 63.026253807119083, 72.888171601040355, 73.881719707719668, 64.491533500684838, 66.667507034484387], [139.55171644350207, 132.27096508176845, 133.99828855874554, 132.36499207163143, 128.66306079756509, 138.65688804202114, 130.26182426197786, 145.75599581727164, 129.42261045212538, 141.04824339105951], [294.82550112659976, 302.53835753470889, 311.76224777732136, 304.09821609434772, 333.88079631888161, 334.30475484140521, 313.46266257136858, 306.33174858128677, 357.61054012781091, 313.61382425025641]], 'Rp': [[0.99998892938321671, 0.998092870624538, 0.99998821640663271, 0.99892447656391181, 0.99830054507430432, 0.99854972254607433, 0.9999871288217772, 0.99877635431644274, 0.99853309669532975, 0.99999329748476229], [0.99479213426331636, 0.99346210949856573, 0.99365764005167689, 0.99366603111407237, 0.99329863830785348, 0.9943670409883385, 0.99263397186169555, 0.99431649029894287, 0.99258033773513388, 0.99226040126343829], [0.98576305052316826, 0.983498994045377, 0.98875338115849754, 0.98850523042621485, 0.9895159272618288, 0.98671688107979638, 0.98787322409545963, 0.98708417086080324, 0.98788560280524818, 0.98732904007854239], [0.975577786941903, 0.98144667404056529, 0.97795722174842536, 0.96962430635870345, 0.96528958321744596, 0.96068437613716706, 0.9634261076246744, 0.96684658227618736, 0.96801330415698328, 0.97271671252163938], [0.94469204243598925, 0.93204078952445002, 0.94710702191882445, 0.94761915051679246, 0.9571263677817955, 0.94105565728555995, 0.93999726669708583, 0.94561761811168632, 0.94971531612880022, 0.9374024894412446], [0.90881067308737229, 0.90445075008843723, 0.90913030123599292, 0.90360470784430669, 0.89233652055660229, 0.90236493338134494, 0.90518173131445412, 0.90342785124258873, 0.91422783205828284, 0.88242580588409059], [0.78933846471224833, 0.78501495278981581, 0.80561943748553932, 0.82746523524175941, 0.79513717683306517, 0.76061051092219478, 0.7899459532725609, 0.77069224953289239, 0.76922318577573046, 0.80149187360671192]]} 
vb_average_performances = {'R^2': [0.99821467204237346, 0.98694955431990261, 0.97464521365293777, 0.94106211626995617, 0.89080284233319929, 0.81419253452796381, 0.62219138966520959], 'MSE': [0.92650592896999373, 7.0948583681388326, 15.067614105344049, 33.99106459208663, 71.179520201500736, 135.19945849176682, 317.24286492239878], 'Rp': [0.99911346379169896, 0.99350347953830342, 0.98729255023349372, 0.97015826550236961, 0.94423737198422297, 0.9025961106693472, 0.78945390401725191]}

# Gibbs NMTF
gibbs_all_performances = {'R^2': [[0.9999640982474265, 0.999976662301363, 0.9999843514925597, 0.9999691931995058, 0.9999837090405099, 0.9999810598672735, 0.9999794549577409, 0.9999757021424392, 0.9963706851626953, 0.9999774424439364], [0.9887188254670738, 0.9876487813733615, 0.9888061298199565, 0.9883583710771858, 0.9896117991659635, 0.9861289512300546, 0.9872263835753372, 0.990472931494721, 0.9897171806347015, 0.9894613944026888], [0.9824560689479832, 0.9776955917526902, 0.9797947830345879, 0.9759832577953403, 0.9826032048727562, 0.9745347061180676, 0.9825738662186562, 0.9751853238589827, 0.97544680734672, 0.9786223927141903], [0.9527822862881948, 0.9407587376787945, 0.9430675459250004, 0.9427957003932831, 0.9482435559002408, 0.9479445529988814, 0.9434689531211573, 0.9529238496238643, 0.9472045133847624, 0.9536730490771194], [0.8865216326992937, 0.8870854653801203, 0.8880645484076666, 0.8921851145355723, 0.9125682113099509, 0.903454618164275, 0.9159655611024895, 0.888532025977158, 0.897404427655667, 0.8910352093577653], [0.7930249179029341, 0.7760057578624064, 0.8128742622786951, 0.8250443649828061, 0.810429706755466, 0.8100275399079921, 0.7866149458605467, 0.7879558264299412, 0.8403259813883655, 0.8224473824475729], [0.6838060862552677, 0.6777566749104094, 0.6236466849385653, 0.6416699811809343, 0.6521527397996659, 0.6577822072739117, 0.6300743802083444, 0.675574535888237, 0.6290401848023921, 0.6393660563558972]], 'MSE': [[0.016447594702847932, 0.01386835136476525, 0.0084577958536406466, 0.016290681282664338, 0.0089278291804378261, 0.011778688571337022, 0.012845321662760647, 0.012975383723015306, 1.9299812259530333, 0.0099777390138387281], [6.5367351673391418, 6.9483066510321816, 6.336986548645025, 7.06885439421072, 6.1376115329635139, 6.296995102228899, 6.6836440385620017, 6.972918283415285, 6.3626498685059971, 6.0509739453395976], [11.364130312368307, 14.211802881155956, 13.260938146974997, 13.659130540957248, 12.883066955577329, 13.006480902682794, 13.888108548803459, 12.63665697101108, 14.472569318504382, 13.134452715011811], [30.697442134390943, 31.104435533450637, 31.170023684032106, 31.644856938847866, 30.672401300938727, 30.27810278529028, 31.515588612131832, 33.105725119101628, 29.862474846697754, 30.668839914644238], [63.561091627935696, 61.147254483535768, 69.28178718762409, 61.571713640126248, 63.596114873964233, 68.828675169762121, 64.004825226366648, 64.971258277011387, 61.892934315310342, 64.637825688920799], [134.30557557257518, 130.9282044804043, 120.59565632726452, 121.38654723178968, 134.45885036015062, 128.62771049553595, 132.09493606715256, 128.71505507671648, 128.86432064560387, 116.39656612591978], [298.51302322400056, 282.31148793814913, 297.82639537004036, 323.85471704384696, 306.68057654971426, 254.92084483757887, 307.52553881157149, 298.9611220320088, 282.3800179878333, 313.5240999585651]], 'Rp': [[0.99998206058877015, 0.99998837465016099, 0.99999224250650387, 0.99998460020604119, 0.99999189792924048, 0.99999058076471636, 0.99998995780983757, 0.99998793402091002, 0.99821694849476239, 0.99998872460645849], [0.99436522659988136, 0.99387216979092929, 0.99439760221687701, 0.99417485433845865, 0.99482786301751724, 0.99321251979179193, 0.99359320240177307, 0.99524250177724449, 0.99484955447092305, 0.99473989564682297], [0.99119067944947858, 0.9888332231255188, 0.98993393512796157, 0.98803441729420349, 0.99135150041135078, 0.98718813011441842, 0.99126450210607919, 0.98764843448375095, 0.98779838377761142, 0.98931841924626596], [0.97623024098311173, 0.97086039617202002, 0.97126046185367154, 0.97128119730708184, 0.97388725669376819, 0.97374455971947804, 0.97181423342449469, 0.976360007343263, 0.9733636172290997, 0.97660586888208045], [0.9419407598203724, 0.94202470057602605, 0.94310303819095465, 0.9447641052649135, 0.95584821964837408, 0.95078050084487853, 0.95774460960621355, 0.94293660844736382, 0.94767227775898821, 0.94438868683755117], [0.89240304983805274, 0.88270564457583844, 0.90168222038427259, 0.90836019968339343, 0.90033342108224834, 0.90193109192403353, 0.88691816036256255, 0.88823604262690059, 0.9178699846639875, 0.90700771250264534], [0.82775022906788132, 0.82428462381119383, 0.78997529777273479, 0.80139742364172561, 0.80952936879035087, 0.81295453109753724, 0.79415852587625946, 0.82272736783784417, 0.7936576640461962, 0.79975504303526301]]} 
gibbs_average_performances = {'R^2': [0.99961623588554505, 0.98861507482410427, 0.97848960026599729, 0.94728627443912983, 0.89628168145899578, 0.80647506858167262, 0.65108695316136256], 'MSE': [0.20415506113083409, 6.5395675532242352, 13.251733729304737, 31.071989086952605, 64.34934804905572, 127.63734223831129, 296.64978237533086], 'Rp': [0.99981133215774032, 0.99432753900522197, 0.98925616251366399, 0.9735407839608069, 0.94712035069956357, 0.89874475276439347, 0.80761900749769866]}

# ICM NMTF
icm_all_performances = {'R^2': [[0.999845460169911, 0.9999022715641026, 0.9999475793910907, 0.9999184056996892, 0.9999163435891139, 0.9999226601855131, 0.9999293481527641, 0.9999078687766354, 0.9999266335711907, 0.9998742200988066], [0.9880548419622303, 0.9902091931664591, 0.988040390128037, 0.9864939759655382, 0.9884615641737413, 0.9884075874943741, 0.9880847457298473, 0.9886760234821876, 0.9872214903902712, 0.9861923988337536], [0.9788792317619726, 0.976812822095893, 0.9780548300808166, 0.9747747793108394, 0.9780599005033862, 0.978885021708471, 0.9751112815654013, 0.976133826804325, 0.9786000269274711, 0.9762145251591746], [0.9454962684662657, 0.9398461290282167, 0.9438485978143312, 0.9472517907350142, 0.9395063368584395, 0.9394851841003802, 0.9496732102879967, 0.9400631038462538, 0.9533739873520835, 0.9493356711930867], [0.8780064836374761, 0.8981891187317712, 0.8819164944466622, 0.8964247836532026, 0.8766786576750065, 0.9119840988839636, 0.8960192237816988, 0.904296846961825, 0.8880862833703997, 0.8982556416925839], [0.7903466131514447, 0.7902867958732855, 0.7673546509159677, 0.7775485852662493, 0.8012036701692535, 0.7774315276275359, 0.8078119595610362, 0.7801522885032528, 0.7783181100201378, 0.7536185632693208], [0.6009785632095666, 0.6166178275701555, 0.6151859210593813, 0.5814602232402175, 0.6199320569290512, 0.5773062739453014, 0.5638790054180441, 0.6095723893425564, 0.5475397983190898, 0.5793205693974062]], 'MSE': [[0.097727968869588705, 0.064123927212889509, 0.033834792811192116, 0.045687031638371949, 0.048790257037139996, 0.034801584288425912, 0.047136893329671505, 0.05328451065540421, 0.040488997746199518, 0.066715966573012958], [6.7989136007380839, 6.4348676779072722, 6.5791685499763037, 6.5318557512594841, 6.4602064492046649, 6.4649498861786379, 6.3209774986716134, 6.9654393362451774, 6.8216651655651672, 6.7375071004621825], [13.445682639148361, 13.280786887214246, 13.776235857272606, 13.724674443676145, 12.985198479387718, 13.662920333412931, 13.897825615273716, 12.457627383187123, 14.048740694623227, 13.238416317231186], [31.221434410435275, 35.159089535960888, 34.369315834665983, 34.707639648649071, 35.37572222665775, 37.039670691380493, 33.687037063324098, 36.248600973548143, 32.508738437717199, 34.408228793413322], [70.146138744969818, 64.271213902668947, 68.091633546689565, 69.130953244573135, 72.048799607897266, 66.315836266705389, 72.569009379021907, 59.777919193837903, 70.32443151325171, 68.699111836170786], [139.95014730648265, 143.30300209580554, 135.04976740821996, 130.4543071260394, 144.19597533772742, 135.54065723293289, 130.83436299722345, 132.19449949915625, 141.00042202602509, 129.21136044153943], [323.87740331806231, 334.72926534953956, 338.08281024643003, 342.56652812222734, 355.61609904693091, 326.24512787756453, 333.45483749808847, 339.19801895407801, 342.82584575723354, 362.15245484989674]], 'Rp': [[0.9999231506198385, 0.99995149559902463, 0.99997439787438824, 0.99995975873913956, 0.99995836060925281, 0.99996158482337261, 0.99996553139979216, 0.99995416312461249, 0.99996455277755647, 0.99993796128692092], [0.99402710139966421, 0.99509303483634926, 0.99403151582801619, 0.99324288691426221, 0.99422867733038989, 0.99421568007806627, 0.99403555258532661, 0.99434645926606446, 0.99359233771422306, 0.99309119719640926], [0.98939883724825328, 0.98836370764881909, 0.98896671694262595, 0.98732952474755176, 0.98898883780580826, 0.98940439073125497, 0.98756973749821653, 0.98799931144796282, 0.98926809486819112, 0.98805197920925347], [0.97236688256324511, 0.96954936431819838, 0.97158484046108939, 0.97327516479879195, 0.96930520113442731, 0.96935304782189391, 0.97468445780276913, 0.9697806283597924, 0.97640897053242226, 0.97437097486988922], [0.93729493144923981, 0.94782021096091595, 0.9392408349962823, 0.94684983007367185, 0.93668308283978552, 0.95531559773058827, 0.94661424523492355, 0.9512276601189722, 0.94289076179150921, 0.9479070586544901], [0.89092469054961976, 0.88961022398669631, 0.8783531165110614, 0.88380924728893728, 0.89612993284432485, 0.88326707816957717, 0.89914764612761144, 0.88362118971135872, 0.88272015502158707, 0.87117358392447064], [0.78351224766892202, 0.78652453153782809, 0.78595296877452692, 0.76739682165127299, 0.78827962432679621, 0.76789919167479825, 0.75753911465408885, 0.7827784431242546, 0.74708761479598107, 0.76414858411878006]]} 
icm_average_performances = {'R^2': [0.99990907911988169, 0.98798422113264406, 0.97715262459177521, 0.94478802796820671, 0.89298576328345902, 0.78240727643574837, 0.59117926284307687], 'MSE': [0.053259193016189629, 6.6115551016208585, 13.451810865042725, 34.472547761575228, 68.137504723578644, 136.1734501471152, 339.87483910200524], 'Rp': [0.99995509568538987, 0.99399044431487726, 0.98853411381479361, 0.97206795326625195, 0.94518442138503789, 0.88587568641352432, 0.77311191423272485]}

# Non-probabilistic NMTF
np_all_performances = {'R^2': [[0.9977618217427497, 0.9999642483865081, 0.9995235519112435, 0.9996401284884944, 0.9973291087130546, 0.9974644287923543, 0.9998182631537678, 0.9989551105557226, 0.998093683404878, 0.9975544176598959], [0.9899629394023917, 0.9866032029766125, 0.9888166828122352, 0.987603688401702, 0.9885978357475388, 0.9891819593373499, 0.9886334975270366, 0.9870968782844781, 0.9879917870877409, 0.988950312232051], [0.9748495128216816, 0.9765496132145074, 0.974617875576446, 0.9778829727189384, 0.9717595954653456, 0.9758475470810044, 0.9731435881952403, 0.9795325249367332, 0.9754342875560892, 0.9735240793493118], [0.841579155565285, 0.8948726421464258, -44495492.61819067, -862597009886.9603, -1.2668854636645226, 0.9022590210182452, 0.901351389698418, -97147684.09564237, -877513405.8922911, 0.8868931330958452], [-118735941385004.03, -542128837992558.25, -228296684429.02267, -1.4596019428775688e+19, -29875.69315119856, 0.8517188082806545, 0.8351887466390326, -8064716390.230581, -2006308585.663292, -8223345.524931528], [-1295.6393274774364, -86703312516891.7, -257.55774632190605, -28629619.770905644, -7033264.557492386, -444003862425372.06, 0.6899689971498573, -1.2776980537092035e+42, 0.7612274491135117, 0.7532347259980153], [-1862186570.0580919, -1.108172259649051e+37, -5608379779.4675865, -2902940564131349.5, -7.297605988553715e+26, -3.6260224832057636e+18, -2392.2520029005414, -6.051118938968386e+19, -3.0324164807801315e+19, 0.6403338046850477]], 'MSE': [[1.283016680028799, 0.020599755002031067, 0.29767622591827381, 0.1849792740638497, 1.3361654600050556, 1.2825927725637254, 0.11054270736704598, 0.46485391581407431, 1.149350324217411, 1.162534304503662], [6.5710909677814824, 6.8566132112008153, 6.2128041172041542, 6.5571830648546232, 6.8811907812303978, 6.0893906387102854, 6.0397033898541475, 6.8792855605064327, 6.6447163130183311, 6.1123807276339415], [14.346599081579825, 13.126782169061723, 14.539204252632178, 14.792943850110879, 14.876139808039639, 13.822909094853712, 14.591870966144516, 12.892653102800914, 14.337596518035443, 13.912293818327067], [75.870782418867165, 75.069049752435816, 23165778490.538223, 570161121518190.25, 1306.3554867273219, 65.304689531711205, 58.083432745087528, 50831825416.560242, 568103851792.30359, 67.252222772647826], [74437390767330544.0, 2.9475279896711482e+17, 145804123720407.09, 8.7426892347514133e+21, 18363608.995120086, 96.245519940796441, 106.51842005463506, 5378791651225.8623, 1327239040866.7615, 4940741944.5962124], [828078.00611678918, 57440918289457784.0, 185130.0557259281, 20672296264.33823, 5311689530.5798359, 2.866889109766953e+17, 213.97372089245317, 8.7204748160865645e+44, 160.59009125694999, 150.38910408785745], [1687385724548.9695, 9.5175377059023408e+39, 4855110544826.1172, 2.2906744487412797e+18, 5.7043802236142102e+29, 3.1352912565663485e+21, 1764936.3219393154, 4.97807979138208e+22, 2.3674014755007284e+22, 317.21994131708124]], 'Rp': [[0.99888031401759669, 0.99998216086368552, 0.99976320412231046, 0.99982052467064975, 0.99866610777913112, 0.9987453189554506, 0.99991008372810086, 0.99947842738976922, 0.99904648536155383, 0.99878552105167351], [0.99498125876078369, 0.9933148321459061, 0.99440067866335025, 0.99383364161568044, 0.99432929883639198, 0.99459513963812818, 0.99430207716136887, 0.99356075984939951, 0.993978270838907, 0.99446238005700538], [0.98734876812980354, 0.98822424781064278, 0.98734162869677267, 0.98891703529725117, 0.98577981975530815, 0.98789215130356245, 0.98660674228201661, 0.98972543939394586, 0.9877096898464669, 0.98670129911008431], [0.91841739810346568, 0.94841821417256722, 0.027931652779525463, 0.0070275465234739638, 0.48617374755227782, 0.94994071540364799, 0.94960653469582623, -0.029945300213811928, 0.029095499513705853, 0.94181234830903349], [-0.02576017054996111, -0.0012777541169250422, 0.14966304492507532, 0.040090164109107727, -0.059437577457751883, 0.92292335671459202, 0.91428795410949681, -0.050331810715965423, -0.012222945140772514, -0.043644897649199765], [0.0016799568495092139, 0.043181508553630711, 0.035912140626434448, 0.012113402633041538, 0.028197554789386528, 0.0043061418367188915, 0.83664656593906483, -0.037114019640318116, 0.8733465577168521, 0.86809191325471191], [-0.091837397785982447, -0.020025350170963394, 0.033097746310890595, 0.026405969265087682, -0.028492631934035974, -0.035116571322598392, 0.044460266540813059, -0.049135219825617686, 0.03743049254086437, 0.80039376412392838]]} 
np_average_performances = {'R^2': [0.99861047628086674, 0.98834387838091364, 0.9753141596915299, -86361616646.640656, -1.4596680531931028e+18, -1.2776980537092035e+41, -1.1081722597220271e+36], 'MSE': [0.72923114194839278, 6.484435877199461, 14.123899266158592, 57080322297553.75, 8.743058577456262e+20, 8.7204748160865643e+43, 9.5175377064727788e+38], 'Rp': [0.999307814793992, 0.99417583375669205, 0.98762468216258537, 0.5228478356839712, 0.18342893642276961, 0.26663617225590319, 0.071718106774238621]}



# Assemble the average performances and method names
methods = ['VB-NMTF', 'G-NMTF', 'ICM-NMTF', 'NP-NMTF']
avr_performances = [
    vb_average_performances,
    gibbs_average_performances,
    icm_average_performances,
    np_average_performances
]
colours = ['r','b','g','c']


for metric in metrics:
    fig = plt.figure(figsize=(1.9,1.5))
    fig.subplots_adjust(left=0.18, right=0.99, bottom=0.17, top=0.95)
    #plt.title("Performances (%s) for different fractions of missing values" % metric)
    plt.xlabel("Noise to signal ratio", fontsize=8, labelpad=1)
    plt.ylabel(metric, fontsize=8, labelpad=-1)
    plt.yticks(range(0,MSE_max+1,50),fontsize=6)
    plt.xticks(fontsize=6)
    
    x = noise_ratios 
    offset = 0
    for (method, avr_performance, colour) in zip(methods,avr_performances,colours):
        all_performances = avr_performance[metric]
        y = numpy.array([all_performances[i] for i in indices_selected])
        plt.bar(ind+offset, y, width, label=method, color=colour)
        offset += width
        
    plt.ylim(0,MSE_max)
    plt.xticks(numpy.arange(N) + 2*width, x)
    
    