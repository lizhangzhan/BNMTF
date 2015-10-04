"""
Plot the performances of the many different NMF algorithms in a single graph.

We plot the average performance across all 10 attempts for different fractions:
[0.1, 0.2, ..., 0.9].

We use a dataset of I=100, J=80, K=10, with unit mean priors and zero mean unit
variance noise.

We have the following methods:
- VB NMF
- Gibbs NMF
- ICM NMF
- Non-probabilistic NMF
"""

import matplotlib.pyplot as plt
metrics = ['MSE']#['MSE','R^2','Rp']

MSE_max = 7

fractions_unknown = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] 

# VB NMF
vb_all_performances = {'R^2': [[0.9630856037244127, 0.9670215107562922, 0.9661045051134491, 0.9722018575258015, 0.9675999313577555, 0.9714297004377326, 0.9608472667855322, 0.9730333544231496, 0.9666510063942921, 0.9603541051163762], [0.9665170350567773, 0.964946197097694, 0.9663350781598471, 0.9627130095757848, 0.9616497277432379, 0.9640427240029992, 0.9678159049304254, 0.9669349000437315, 0.9641029182026513, 0.9685062857795189], [0.959773536111611, 0.9619285393512471, 0.9612240892216553, 0.9614987452100451, 0.9584291900683835, 0.9625229889130691, 0.9613925806791348, 0.9635766555104377, 0.9619711274413051, 0.9637773429736658], [0.9582224235087118, 0.9591420955113374, 0.9595049864880968, 0.9589604749797365, 0.9590359277212913, 0.9585875441047893, 0.960902037779746, 0.9614427654183628, 0.9609469576204902, 0.9589845126561516], [0.9527508903860804, 0.9532794041128106, 0.9514561283382098, 0.9542335555606037, 0.9566239021533259, 0.9540670856579738, 0.9545119685902426, 0.9565341570138918, 0.9549420865598607, 0.9552309386352669], [0.944824160627708, 0.9443509173528474, 0.9417312447125505, 0.9438389652711955, 0.9427625876422, 0.9425193651599165, 0.9418179180323941, 0.9424462796553271, 0.9420853896708117, 0.9465518001065166], [0.9001951862432918, 0.9183769138373294, 0.9166251929599342, 0.9069886075247062, 0.9115460497313663, 0.9151656497212621, 0.9123698613361313, 0.9124628297593562, 0.9092181617299763, 0.9196836026740838], [0.5718452222629703, 0.6583451513873824, 0.556741155657702, 0.583570843165066, 0.5104570853808321, 0.6360167602951334, 0.6512768325827929, 0.5214192895053769, 0.6275751203453768, 0.564905893846642], [0.5027844119329963, 0.4933257161288198, 0.4496685398864789, 0.4746077863315795, 0.4522656764387484, 0.5368917178074404, 0.4755783852096349, 0.4087673131892968, 0.4898747418380873, 0.4562544542743766]], 'MSE': [[1.4292554648676139, 1.3974051235158393, 1.29440666612722, 1.3217147142340593, 1.3208653575825622, 1.2551131044832673, 1.3757415666406905, 1.3065565812238904, 1.2042610271487089, 1.353798372612641], [1.3515803752693407, 1.3733054586267974, 1.3605784424251741, 1.5082085923523942, 1.412474232111794, 1.3422121840192229, 1.3633847814127587, 1.3403919024877198, 1.4268521219705763, 1.3289609470877093], [1.5502007005526373, 1.4662981005339264, 1.4619454920602812, 1.4335526755575416, 1.4595506807654832, 1.4625057118999791, 1.5535336837966451, 1.4382786571200279, 1.5083283919668102, 1.3930085927285758], [1.5541487972104295, 1.5713266193529145, 1.5946890731711545, 1.6056428426898903, 1.6251711444313219, 1.6215805013925217, 1.6220695413856037, 1.5378342018350912, 1.5531413220895049, 1.5350785451061721], [1.8117382277125307, 1.8477089630749928, 1.8897308174736871, 1.8201218699708099, 1.7956362330203772, 1.752797709484893, 1.7216079538498541, 1.6453618999158146, 1.8054631354026731, 1.8195334536523358], [2.184303640722197, 2.1949240106826875, 2.2056897515984528, 2.2641485953679252, 2.3428786178800967, 2.2597863299291139, 2.302011581068792, 2.1774461811293935, 2.3360642336198585, 2.1121378157470256], [3.9794794510337508, 3.2397568599609925, 3.3357028761301137, 3.7144139551688489, 3.4156036936427556, 3.3906177543890812, 3.3771166204052192, 3.386053503948375, 3.4216546182019933, 3.2108561252818357], [16.679921188539794, 13.650105558808882, 16.988458368541757, 16.29013292645822, 18.769667736252153, 14.529014512907999, 14.194886291079053, 18.888984430976617, 14.368616642611762, 17.500043934952473], [19.728859852733237, 20.0357738274881, 21.614472803471031, 20.376215739188623, 21.481467397245979, 18.315206156715181, 20.793134858429365, 23.458756395361693, 20.374177558979476, 21.495922836713685]], 'Rp': [[0.98137357044894324, 0.98356969304565223, 0.98307183949334243, 0.986023974645173, 0.983791401261639, 0.98567445089057881, 0.98024941158262702, 0.98645450391382405, 0.98319465746836576, 0.98020000016184972], [0.98313446665444237, 0.98232877010194075, 0.98304226090514368, 0.98118639812951347, 0.98065246443942522, 0.98185897615701179, 0.98377658992615691, 0.98333144836210784, 0.98199493342705979, 0.98412744103150163], [0.97975501823888478, 0.98088479147381558, 0.98045650434671505, 0.98057262460682237, 0.97902209539002805, 0.98118645391138437, 0.98053707911525445, 0.9816498220269525, 0.98084506735664256, 0.98174740424723672], [0.97890361614299271, 0.97939109918387257, 0.9795531120627371, 0.97932255725184125, 0.9793042901481851, 0.97914786008990751, 0.98025799335713648, 0.98055794984324751, 0.98029105475801981, 0.9792854032132573], [0.97613493661568473, 0.97641827119444946, 0.97556467703224747, 0.97687271912817053, 0.97817876610563415, 0.97683425927468293, 0.97701341756789306, 0.97808502827763166, 0.97723236000443159, 0.97738278258968225], [0.97203460912583317, 0.97183443904940936, 0.97053747482518804, 0.97151838581568295, 0.97096119919381663, 0.97090027611260332, 0.97050254907300826, 0.97086349701148777, 0.97066332933436827, 0.97297703058961549], [0.94884176188711122, 0.95871692564457744, 0.9574286431553255, 0.95245998639735729, 0.95482371817969269, 0.95665745045296158, 0.95521411307579607, 0.95532060353134696, 0.95377749055837036, 0.95903245723711927], [0.77169610839500669, 0.81194990763251429, 0.77315400488399622, 0.77421630884784298, 0.75639479857647018, 0.80636943929628646, 0.80820079878518392, 0.74909538974484358, 0.80153421908357991, 0.76058696280751781], [0.73902171116167437, 0.7298352820200974, 0.73032526666911179, 0.73544281542769874, 0.73313362065671095, 0.75912748936719998, 0.73653668038292519, 0.69850055406951517, 0.73406943170778083, 0.73171766157704843]]} 
vb_average_performances = {'R^2': [0.9668328841634795, 0.9653563780592667, 0.9616094795480554, 0.9595729725788713, 0.9543630117008268, 0.9432928628231467, 0.9122632055517437, 0.5882153354429274, 0.4740018743037459], 'MSE': [1.3259117978436494, 1.3807949037763489, 1.4727202686981908, 1.5820682588664607, 1.7909700263557968, 2.2379390757745541, 3.4471255458162964, 16.185983159112869, 20.767398742632636], 'Rp': [0.9833603502911995, 0.98254337491343047, 0.98066568607137372, 0.97960149360511983, 0.97697172177905078, 0.97127927901310118, 0.95522731501196601, 0.78131979380532424, 0.73277105130397613]}

# Gibbs NMF
gibbs_all_performances = {'R^2': [[0.9619059001208281, 0.9640827667211137, 0.9694512746263138, 0.9701886721742091, 0.9657569043522852, 0.9645199588372723, 0.9634705713931656, 0.9676267917708213, 0.9675622254798245, 0.9684506981142136], [0.9661983256111081, 0.9616205514088321, 0.964782466321369, 0.9642198246274559, 0.9609647615999493, 0.9645080846532873, 0.9628567568565517, 0.9625100016209683, 0.9647052208065231, 0.9617419670924906], [0.9643234840870709, 0.9617430678118996, 0.961338418396636, 0.9621685540717345, 0.9590790976588984, 0.9630979205180834, 0.9648309654552717, 0.9610122836488321, 0.961987672033106, 0.9612220362972822], [0.9595101862277302, 0.9594776094947263, 0.957823871926474, 0.9570380281896163, 0.9565386172828394, 0.9598820325488254, 0.9578290274243525, 0.9568794205531495, 0.9614822869442783, 0.9590428076940245], [0.9522941300113166, 0.9592824357136986, 0.9523343094760195, 0.9530924121407341, 0.9545449371032484, 0.9552885193209901, 0.9535007755625815, 0.9533325771726907, 0.9538848182936318, 0.9526588158499125], [0.9431535719627517, 0.9430805152703715, 0.9438988157247572, 0.939609300028728, 0.9419858916360788, 0.9414720533278618, 0.9431853506983003, 0.9450629953350186, 0.9420390340603483, 0.940740567078019], [0.907184519966465, 0.8893815616999061, 0.8947153607127359, 0.9210263887880934, 0.9165479957564602, 0.9011617012566961, 0.914193937886436, 0.9096273664291488, 0.8954458717355149, 0.9141336520293362], [0.7156007465858046, 0.6608549871190714, 0.5081403620663952, 0.5878899388839927, 0.569112134184095, 0.5922612076738332, 0.6788791286000178, 0.6756450333289706, 0.6368380147278165, 0.6412391457100886], [-0.03883065769894101, 0.39937236004066956, 0.28768810475157225, 0.09263549338150567, 0.3168058803008834, -0.09290240474776601, 0.35323399570551717, 0.3214323519141459, 0.4174905865373635, 0.33869715838260983]], 'MSE': [[1.3435161026525739, 1.422961444249444, 1.3631881946753663, 1.2758401195570195, 1.3723055080209405, 1.3591839088535866, 1.3073380616795633, 1.2759250524622099, 1.3171618674650449, 1.3008268160586309], [1.4052993493654045, 1.4061825751225325, 1.4145324544645925, 1.416226609062057, 1.3686757539628065, 1.3963021810316414, 1.3295080392294472, 1.413876209948091, 1.3895909892824541, 1.419473598871462], [1.4527645268465443, 1.4826447252288502, 1.4254506857209015, 1.4201453258828076, 1.5561327664672613, 1.3896139933122358, 1.4093211449035519, 1.496694920695091, 1.5080125674525022, 1.4776551431702634], [1.6273693364025781, 1.5613122281634206, 1.6454573438972488, 1.5741174307843806, 1.6605585104955143, 1.5484879861149485, 1.5673643158482429, 1.602940012847651, 1.583455906458755, 1.6025335487371899], [1.8894807573583676, 1.7080057208270207, 1.8633500585485623, 1.7974722582784888, 1.8347187228173907, 1.7174347001477308, 1.8581357148871396, 1.929932788496548, 1.8084403552739736, 1.913959453942534], [2.2776321156547823, 2.1936042177364317, 2.2241365566054401, 2.3483636322993302, 2.3154926960962983, 2.2067045058831347, 2.2426850409475771, 2.1446587159580708, 2.2992147876063465, 2.2943319870938215], [3.7685336471769131, 4.3642248206791576, 4.1420738260722327, 3.1913847733566691, 3.16274898450681, 3.8163163270379021, 3.4308795689453064, 3.5367105688459781, 3.969659603845769, 3.4073620151958273], [11.059472488515201, 13.473029553247274, 19.291326753948525, 15.885738351988971, 16.899217668762873, 15.993607044250318, 12.602174595100042, 12.64226363202151, 14.496466797700567, 14.251389800630605], [40.67778578143124, 23.597337597218569, 27.599872865640666, 35.191150325252806, 27.086630055043276, 43.222847307391774, 25.432423502446227, 26.565062181981109, 22.777538269386849, 26.061386510100139]], 'Rp': [[0.9808300176523761, 0.98191012955331602, 0.9846447380668788, 0.98502372410143113, 0.98295436323656427, 0.98218222196692218, 0.98158559788405897, 0.98384206390239581, 0.98365853961110095, 0.98422252322658887], [0.98305770886688504, 0.98070818786031999, 0.98237072800530101, 0.98206139647059831, 0.98049188373631291, 0.98216731690336034, 0.9814417415253478, 0.98131137814915259, 0.98232864345704773, 0.98082516803012287], [0.9820606197511198, 0.9807351745160261, 0.98051949001280969, 0.98101659543957065, 0.97957670034473365, 0.98148427289695284, 0.98237543663511029, 0.98054936315594643, 0.98081102068623438, 0.98044887461040298], [0.97969381119965981, 0.97981830085026567, 0.97887161359914421, 0.97844051123524944, 0.97818134826056602, 0.97981148323928802, 0.97895143393769946, 0.97837373509892023, 0.98068194861727975, 0.97933890222115283], [0.97596914606319907, 0.97948998779897789, 0.97608484457282485, 0.97631491477655108, 0.97722559468427406, 0.97745619114463023, 0.97664134200129493, 0.97653440518293821, 0.97676845964285663, 0.9760570600875722], [0.97156149840243344, 0.97130590105423775, 0.97183373860842126, 0.96992716504553211, 0.97100065017491433, 0.97049381180634986, 0.97126367292558591, 0.97259156409279002, 0.97088110253196591, 0.97014609337518065], [0.95278667585694221, 0.94408340080594666, 0.94637016462172452, 0.96041168374829489, 0.95772863817233489, 0.95008710901536975, 0.95697256258891428, 0.95486074666490039, 0.94714480274787571, 0.95637229731612861], [0.85582341403166551, 0.83015757498009135, 0.76494459314321051, 0.80433937728497462, 0.79221780577170087, 0.79481080120454572, 0.84458468684503507, 0.83521337317818112, 0.82050034724166165, 0.81678073214726177], [0.67367981676225963, 0.7433971381896638, 0.70087233632151957, 0.68318666823004459, 0.69454459159521076, 0.66938293877487642, 0.73835592140083472, 0.71422274278175091, 0.74078332437265537, 0.73012959685238132]]} 
gibbs_average_performances = {'R^2': [0.9663015763590048, 0.9634107960598536, 0.9620803499978814, 0.9585503888286014, 0.9540213730644822, 0.9424228095122235, 0.9063418356260794, 0.6266460698880085, 0.23956228685675604], 'MSE': [1.3338247075674379, 1.3959667760340486, 1.461843579968001, 1.5973596619749928, 1.8320930530577755, 2.2546824255881233, 3.6789894135662573, 14.659468668616592, 29.821203439589265], 'Rp': [0.9830853919201632, 0.98167641530044492, 0.98095775480489067, 0.97921630882592259, 0.97685419459551182, 0.97110051980174106, 0.95268180815384329, 0.81593727058283272, 0.70885550752811977]}

# ICM NMF
icm_all_performances = {'R^2': [[0.9675308056342089, 0.9706731183201378, 0.963515388656442, 0.9641470395458833, 0.9655826279217266, 0.9672294102359171, 0.9646001028981867, 0.9640619445467564, 0.9690036553956349, 0.9654409469483706], [0.9639738759573419, 0.963567010099971, 0.9654223808085468, 0.9643410967733337, 0.9624560435500431, 0.964324471631967, 0.9623909262839379, 0.9608493186526555, 0.9657672670199301, 0.9659115228364663], [0.9614572511485779, 0.9589819094877396, 0.963989588472418, 0.9608121334638506, 0.9642719642530541, 0.9608971571013196, 0.9612212583750915, 0.9612404133396623, 0.9618299957652703, 0.961369171789454], [0.9585160253993189, 0.9575779061062479, 0.9574643720429868, 0.9594241418510507, 0.9584959767975174, 0.9604005841420141, 0.9589059353654282, 0.9604642942489454, 0.95750675995146, 0.9607169405608774], [0.9512913413870069, 0.9542372391958707, 0.9570930945184041, 0.9536261975478091, 0.9535052419653446, 0.9511312110680381, 0.9509401809556668, 0.9504006562363108, 0.9512952600303107, 0.9533992700930061], [0.9421897455772862, 0.9377710137581358, 0.93923072477646, 0.9359583884993236, 0.9401515756921959, 0.9160080327252482, 0.9388377747710379, 0.9333978218918502, 0.9410161118470081, 0.4172077771215297], [0.6492870470824728, 0.41808562676856553, 0.8601954384863069, 0.18391754468568988, -0.3712969781058011, 0.1928831001369935, -0.04476264055036028, -0.07822039466291453, 0.7782838803614673, 0.8471368345342142], [-15.154083055897928, -3.2260813954603647, -3.0404150913693346, -2.8912227984149217, -1.6365028486809656, -3.701950932661954, -1.3347890580260828, -2.9721167590862185, -7.579224246222399, -0.8305063766953791], [-25.229116347034754, -2.584717328359927, -7.805478147382384, -4.3858408057911555, -45.58291647127771, -172.62011291578443, -11.135481520827124, -38.9551194732589, -45.484597899013046, -9.811203434168704]], 'MSE': [[1.187157164954578, 1.3898297200725369, 1.3783972956361257, 1.3143989657901607, 1.3677641943629277, 1.32361845717388, 1.3648837705275227, 1.3285044801517296, 1.1829726301849688, 1.2651118784833626], [1.453364418735541, 1.3700096800001251, 1.3376849941391245, 1.4339828974782167, 1.3969112642935315, 1.4114103780266951, 1.4552342906907807, 1.5236834547871951, 1.4261476182236223, 1.396701158803284], [1.5405572085051735, 1.5127404138095704, 1.4583016848597918, 1.5515746462240012, 1.4437979737297169, 1.5164660159943102, 1.4769147682537309, 1.4750441757138248, 1.5148205392710512, 1.5329485512131671], [1.6332378436324435, 1.6091543761045901, 1.6674524973738523, 1.5849445704145741, 1.6275463811308035, 1.5545596959921908, 1.7123338748280075, 1.5426972993965666, 1.626169671913325, 1.5774155055271952], [1.8827083597062471, 1.8869800012441869, 1.6869415553799403, 1.8643145673603752, 1.8209797481971748, 1.8191245605478923, 1.8684620275369468, 1.8263604829944977, 1.9202701967828466, 1.8196651252973335], [2.2619641354569513, 2.4692946761188788, 2.3902065843598028, 2.4807743653310128, 2.3144651089404418, 3.4190015777729346, 2.4776173216749866, 2.6065406236207629, 2.4281860289525961, 23.157360984753783], [13.888138409142835, 23.191374771463085, 5.4875067563411362, 32.046162842779452, 52.300603873623579, 31.832906750343106, 41.306738372637341, 42.640943734195858, 8.7846347172410315, 6.0689159243055224], [637.82330632690832, 164.64775884872782, 160.14683783654888, 154.27762959286534, 104.33047904751766, 183.18459490341436, 90.908851265961275, 158.29703989937892, 340.46365883945168, 72.517089326534872], [1027.0193630787844, 140.01123141089118, 345.50548111476979, 209.4833772439263, 1841.2300141903368, 6816.5173720613329, 476.1871633364039, 1591.571192212532, 1818.4092301141911, 425.908306211411]], 'Rp': [[0.98371254375777983, 0.9852593042200033, 0.98169025730922743, 0.9820463841118251, 0.98264745037432177, 0.98364597296075718, 0.98215363830320457, 0.98189268015836306, 0.98442356198749348, 0.98263394115834157], [0.98191812061810446, 0.98162072345629237, 0.98270050186274183, 0.98206503621597818, 0.98108147768777143, 0.98213101679579162, 0.98114539350026431, 0.98024769311959414, 0.98286605201274857, 0.98294943837519688], [0.98056513858036443, 0.97933317147454091, 0.98186393539653039, 0.98021947354660055, 0.98198582351158248, 0.98040588610494672, 0.98048303802774139, 0.98055718063417985, 0.98086247278375616, 0.98049684325918762], [0.97913294286247166, 0.9786355908419283, 0.97856675075222943, 0.97967119266141989, 0.97909324390033037, 0.98018288502510165, 0.97946117067749672, 0.98005418069212935, 0.97855095740841946, 0.98022701605169793], [0.97541613729030174, 0.97698358058682688, 0.97842381853910809, 0.97659228688440214, 0.97663770073844913, 0.97534140334396213, 0.97528835458281882, 0.97513083651584087, 0.97555595094597558, 0.97651242166614194], [0.97072674123090485, 0.96872680951692303, 0.96967332358728719, 0.96779800442128827, 0.96999790525567497, 0.95802255524500712, 0.96950122809024442, 0.96641199125903743, 0.97057469601659108, 0.77834325806882843], [0.8458462324193643, 0.76874646860456841, 0.93532706265827947, 0.73021663349220967, 0.66315121760061924, 0.71472380265694679, 0.6823375995997647, 0.69144435374124924, 0.89964626185006069, 0.92403445885840774], [0.31332946027253189, 0.39537928253773769, 0.47679860124063189, 0.39897732785199841, 0.4991530080173564, 0.45565956293722693, 0.4961447404344001, 0.45378913782676389, 0.33345827202983858, 0.5135021247128172], [0.3434072088157063, 0.47061044993748996, 0.39680929075293253, 0.39124671575428283, 0.34861242077073645, 0.22469325738464976, 0.29643158775236977, 0.28413749892097034, 0.28533432255364599, 0.34385929058618586]]} 
icm_average_performances = {'R^2': [0.9661785040103265, 0.9639003913614193, 0.9616070843196438, 0.9589472936465846, 0.9526919692997768, 0.8841768966660075, 0.3435509458736634, -4.236689256251556, -36.35945843428981], 'MSE': [1.3102638557337791, 1.4205130155178114, 1.5023165977574338, 1.6135511716313551, 1.8395806625047442, 4.6005411406982146, 25.7547926152073, 206.65972458873088, 1469.1842730974581], 'Rp': [0.98301057343413178, 0.98187254536444846, 0.980677296331943, 0.9793575930873224, 0.97618824910938273, 0.94897765126917866, 0.78554740914814702, 0.43361915178613025, 0.33851420432289692]}

# Non-probabilistic NMF
np_all_performances = {'R^2': [[0.9008720358092512, 0.9601292556538269, 0.9612346327882337, 0.9632370353344099, 0.9633416652818967, 0.9622524390617689, 0.9603462698770026, 0.9671543638475553, 0.963321176365319, 0.9647502561162388], [0.9587423807980398, 0.9594551242359872, -3.4181530290314203e+31, 0.9667705271422598, 0.9594795927427342, 0.9555980739163884, 0.9641509195014247, 0.9600012125982704, 0.9607054683210157, 0.9661084282762575], [0.9382181233060924, 0.9555854839521907, 0.9368037902628257, 0.9582622859261749, 0.9620448532122527, -9.575051602187483e+42, 0.9471224531572379, 0.7562029493130721, 0.9548875991119727, 0.9555910437196921], [0.9496402766263484, 0.9392930203111193, 0.9442935216869608, 0.9237404390903083, 0.9252803184201542, 0.9523531935481676, 0.9307580665584911, -8.133649834554712e+20, 0.9388936675208388, 0.9048524050134544], [-1.1598779258816443e+27, 0.9372133879068926, -3.961690031106814e+20, 0.9440248592259005, 0.9394813432143667, 0.9271719222979232, 0.9071206814997375, 0.9298946916088988, 0.9401015477550159, 0.9236712109281022], [0.8383378704069995, 0.8782152271084063, 0.917929309782159, 0.9064879190269263, -1.7332687521184305e+39, 0.8912375905665959, 0.8842081930840828, 0.9140398760507505, 0.9003029739978541, 0.9050855834326664], [0.4291718721362058, 0.2408221511005295, 0.633924944674207, 0.6059517361949012, 0.4764804275809116, 0.5876339971706936, 0.30137189935767383, 0.4659353092966517, 0.49461273376976167, 0.6103288971363448], [-2.342700361645398, -0.8577504348916534, -1.9468133763345055, -0.34252122761398285, -0.5991572676542325, -2.0317122701006682, -0.8312242875276055, -0.108334186297536, -0.17997801861930718, -0.5320222201096987], [-0.11243196632724661, 0.03940719301589024, -0.13528418448295598, -0.042675187196357545, -0.2120072997424549, -0.29388458483317614, -0.44435489468160605, -0.3475109932763185, -0.5122262467188277, -0.2011759238351314]], 'MSE': [[4.0862243392120989, 1.4299724526688331, 1.5478315731222576, 1.4485566598730231, 1.3419174296956933, 1.5154235230084641, 1.4766552639482657, 1.3331249217264756, 1.4567687519365884, 1.366132427982282], [1.5620403080588923, 1.4860195677252179, 1.3493431600534702e+33, 1.4751202752786454, 1.5220438439697228, 1.5607297865294163, 1.580556659686865, 1.5575718640615679, 1.5531311163348624, 1.4407339893520088], [2.3582786615099707, 1.7864543793984091, 2.4581876144444004, 1.6801830604913042, 1.6522341731931889, 3.7924425129609333e+44, 2.2929758478949553, 9.7356857972305821, 1.6214648973461219, 1.6976979410909789], [1.9142355382829572, 2.2816879721009702, 2.1346299355636189, 3.0480041665231195, 2.8851446240861547, 1.8758131708232826, 2.6862617238018971, 3.2579614472979008e+22, 2.4249045742967557, 3.8554037589132593], [4.6664732336351262e+28, 2.4824394405414516, 1.6265363356071028e+22, 2.1730815060057629, 2.3421266313290734, 2.743063926102657, 3.6572585424434725, 2.7496852131846103, 2.4005124113313241, 2.8468050558976619], [6.3329922360184616, 4.7910446382609768, 3.1623679445952599, 3.7030770129419066, 6.7674716120028753e+40, 4.2640269018660009, 4.567875948754005, 3.2404421535746017, 3.8234178604209772, 3.74623027931688], [22.002711432613282, 30.064556119472648, 14.683106704960636, 15.508973138068894, 20.51025684726568, 16.187068250196642, 26.826087912654543, 21.201330005593618, 20.008006653752226, 15.132184360577902], [131.83114074936503, 73.02538576627569, 119.33165121728589, 53.356695570391032, 63.919770764393228, 118.94930276474862, 71.317449613104927, 43.423013478239774, 47.509622297765574, 60.297065158413986], [43.577479696712679, 37.858347282609508, 45.531407591938404, 41.668997730021523, 48.279141935932088, 50.56517035994198, 57.213708264108064, 52.686229820235006, 59.166699743979777, 47.645945746358706]], 'Rp': [[0.95037857405740567, 0.97988404582615307, 0.98053049839702078, 0.98153477649269993, 0.98152521993533759, 0.98104821713427215, 0.97999923277144063, 0.98355933957506247, 0.98149880299043935, 0.98223755187360473], [0.97920353349754341, 0.97961173074760421, 0.030200726212311672, 0.98332653963263617, 0.97974966075550363, 0.97790157562680458, 0.98199762785234446, 0.97992759439844479, 0.98032876744747344, 0.98300650347533247], [0.96920967282957282, 0.97758323107328726, 0.96804413788979149, 0.97922104249115349, 0.98084388878994777, 0.0034839916357522665, 0.97329363289935722, 0.89072044389126603, 0.97732163806555494, 0.97764917791994499], [0.97464651976991989, 0.96944953281324575, 0.97210318321723144, 0.96179891441702603, 0.96218400971305429, 0.97598836501352693, 0.96543049507150214, -0.0051467773616229607, 0.9695531230206752, 0.95432741700674417], [-0.013080893326172505, 0.9687709598282892, 0.0154222415085759, 0.97228143642665765, 0.9698418909324481, 0.96359737010165236, 0.95359032632328022, 0.96465991235344772, 0.96975971293391483, 0.96172047493248258], [0.92145297881044197, 0.93887770864955522, 0.95923092603473969, 0.95307064461122093, 0.0019191481769650135, 0.94475008508827107, 0.94116943735172731, 0.9569184836230441, 0.94975816616296227, 0.95213011428914041], [0.75281984174534367, 0.69344700368562529, 0.82433916270976315, 0.8149423647725671, 0.77192858325793101, 0.80172230931040822, 0.71370441334474222, 0.76595337257687091, 0.7795462531197147, 0.81482529264009951], [0.4022157265391581, 0.49987556610742007, 0.40335727391104315, 0.55323898257513349, 0.5197183311959761, 0.41229207287725705, 0.53897287199072397, 0.60251608432676695, 0.56678540039532477, 0.54895666941604127], [0.58262057427916281, 0.59721078387221338, 0.53555919427868337, 0.5712455094801655, 0.53586240999279489, 0.5234212547737318, 0.49312408378952566, 0.53725758782329591, 0.52895742581609639, 0.56688119771431333]]} 
np_average_performances = {'R^2': [0.9566639130135502, -3.41815302903142e+30, -9.575051602187484e+41, -8.133649834554712e+19, -1.1598783220506474e+26, -1.7332687521184306e+38, 0.48462339684178807, -0.9772213650794589, -0.2262144088078184], 'MSE': [1.7002607343173981, 1.3493431600534702e+32, 3.7924425129609332e+43, 3.2579614472979009e+21, 4.6664748601714616e+27, 6.7674716120028753e+39, 20.212428142515609, 78.296109737998364, 48.41931281718378], 'Rp': [0.9782196259053435, 0.88552542596459993, 0.86973708574856268, 0.87003347826813027, 0.7726563432014576, 0.85192776927980685, 0.77332285971630665, 0.50479289793348447, 0.54721400218199834]}



# Assemble the average performances and method names
methods = ['VB-NMF', 'G-NMF', 'ICM-NMF', 'NP-NMF']
avr_performances = [
    vb_average_performances,
    gibbs_average_performances,
    icm_average_performances,
    np_average_performances
]
colours = ['r','b','g','c']

for metric in metrics:
    fig = plt.figure(figsize=(1.9,1.5))
    fig.subplots_adjust(left=0.12, right=0.95, bottom=0.17, top=0.95)
    #plt.title("Performances (%s) for different fractions of missing values" % metric)
    plt.xlabel("Fraction missing", fontsize=8, labelpad=1)
    plt.ylabel(metric, fontsize=8, labelpad=-1)
    plt.yticks(range(0,MSE_max+1),fontsize=6)
    plt.xticks(fontsize=6)
    
    x = fractions_unknown
    for method,avr_performance,colour in zip(methods,avr_performances,colours):
        y = avr_performance[metric]
        #plt.plot(x,y,label=method)
        plt.plot(x,y,linestyle='-', marker='o', label=method, c=colour, markersize=3)
    
    plt.xlim(0.0,1.)
    if metric == 'MSE':
        plt.ylim(0,MSE_max)
    else:
        plt.ylim(0,1)