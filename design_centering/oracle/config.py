from pertubation import PertubationGenerator as pgen

threshold = 9 # lower bound for feasibility in ms

tool_path = "/opt/maps"
benchmark = "sobel"
architecture = "generic_arm.architecture"
xml_root = "/opt/maps/apps/cpn/sobel/mapper/result_analyzer/oracle/"
xml_path = "/opt/maps/apps/cpn/sobel/mapper/result_analyzer/oracle/tmpmapping.xml"
default_path = "/opt/maps/apps/cpn/sobel/mapper/results/2017-02-28--08-09-23_default/default.mapping"
log_path = "/net/home/hempel/dca/dc_algorithm-sobel/oracle_sobel.log"
max_pe = 15 # maximum PEs for the given architecture
num_pr = 5 # number of precesses in KPN
cluster_lvl = 2 #cluster and shared_mem
cores_per_cluster = 15
use_oracle_cache = 1
pe_prefix = "ARM" # available CPU type
#mem_prefix = {"noc_cp":["noc_mem_c", "slow_mem_c"]} # dict of available comm. primitives for specific memory

# used to select the correct com_prefix
mem_sel = {50:0, 250:1, 500:2}
# dict of avilable memories per core (from local to global) and the corrssponding comm primitive
# {core: [(mem,primitive), (mem,primitive) ,...] ...} 
com_prefix = {0 :  [("local_mem_arm00", "local"), ("shared_mem_cluster0", "cluster0"), ("shared_mem", "shared")],
              1 :  [("local_mem_arm01", "local"), ("shared_mem_cluster0", "cluster0"), ("shared_mem", "shared")], 
              2 :  [("local_mem_arm02", "local"), ("shared_mem_cluster0", "cluster0"), ("shared_mem", "shared")],
              3 :  [("local_mem_arm03", "local"), ("shared_mem_cluster0", "cluster0"), ("shared_mem", "shared")],
              4 :  [("local_mem_arm04", "local"), ("shared_mem_cluster1", "cluster1"), ("shared_mem", "shared")],
              5 :  [("local_mem_arm05", "local"), ("shared_mem_cluster1", "cluster1"), ("shared_mem", "shared")],
              6 :  [("local_mem_arm06", "local"), ("shared_mem_cluster1", "cluster1"), ("shared_mem", "shared")],
              7 :  [("local_mem_arm07", "local"), ("shared_mem_cluster1", "cluster1"), ("shared_mem", "shared")],
              8 :  [("local_mem_arm08", "local"), ("shared_mem_cluster2", "cluster2"), ("shared_mem", "shared")],
              9 :  [("local_mem_arm09", "local"), ("shared_mem_cluster2", "cluster2"), ("shared_mem", "shared")],
              10:  [("local_mem_arm10", "local"), ("shared_mem_cluster2", "cluster2"), ("shared_mem", "shared")],
              11:  [("local_mem_arm11", "local"), ("shared_mem_cluster2", "cluster2"), ("shared_mem", "shared")],
              12:  [("local_mem_arm12", "local"), ("shared_mem_cluster3", "cluster3"), ("shared_mem", "shared")],
              13:  [("local_mem_arm13", "local"), ("shared_mem_cluster3", "cluster3"), ("shared_mem", "shared")],
              14:  [("local_mem_arm14", "local"), ("shared_mem_cluster3", "cluster3"), ("shared_mem", "shared")],
              15:  [("local_mem_arm15", "local"), ("shared_mem_cluster3", "cluster3"), ("shared_mem", "shared")]}
	      
arch_mapping = {0: [0,0],1: [0,1],2: [0,2],3: [0,3],
                4: [1,0],5: [1,1],6: [1,2],7: [1,3],
		8: [2,0],9: [2,1],10:[2,2],11:[2,3],
		12:[3,0],13:[3,1],14:[3,2],15:[3,3]}

# generic ARM sparse tuple-matrix to determine fastes connection
#                c00  c01  c02  c03  c04  c05  c06  c07  c08  c09  c10  c11  c12  c13  c14  c15
comm_network = [[ 50, 250, 250, 250, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], # c00
                [250,  50, 250, 250, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], # c01
                [250, 250,  50, 250, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], # c02
                [250, 250, 250,  50, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], # c03
                [500, 500, 500, 500,  50, 250, 250, 250, 500, 500, 500, 500, 500, 500, 500, 500], # c04
                [500, 500, 500, 500, 250,  50, 250, 250, 500, 500, 500, 500, 500, 500, 500, 500], # c05
                [500, 500, 500, 500, 250, 250,  50, 250, 500, 500, 500, 500, 500, 500, 500, 500], # c06
                [500, 500, 500, 500, 250, 250, 250,  50, 500, 500, 500, 500, 500, 500, 500, 500], # c07
                [500, 500, 500, 500, 500, 500, 500, 500,  50, 250, 250, 250, 500, 500, 500, 500], # c08
                [500, 500, 500, 500, 500, 500, 500, 500, 250,  50, 250, 250, 500, 500, 500, 500], # c09
                [500, 500, 500, 500, 500, 500, 500, 500, 250, 250,  50, 250, 500, 500, 500, 500], # c10
                [500, 500, 500, 500, 500, 500, 500, 500, 250, 250, 250,  50, 500, 500, 500, 500], # c11
                [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,  50, 250, 250, 250], # c12
                [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 250,  50, 250, 250], # c13
                [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 250, 250,  50, 250], # c14
                [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 250, 250, 250,  50]] # c15

# list of pertubation functions to call

# test set for pertubation (first entry shold be the design center)
# xstart=[15;9;8;15;14;2;6;8;7;10];
#test_set = [[12,8,8,8,8,12,12,7,2,11]]
#test_set = [[3,2,8,4,1,6,9,4,13,6]] #(current best mapping 96% manhattan r=5,8)
#test_set = [[5,1,2,3,0,2,4,2,2,3,0,4,3,3,2,6,3,4,0,0,4,0,3,3]] #JPEG best effort
test_set = [[4,4,4,6,8],[1,2,3,4,5]] #Sobel
#test_set = [[4,0,4,0,1,1,0,1,7,0]] #(75% manhattan r=3,01)

#---------------------------------------
#       xstart = [9 ;0;6;4;7;5;8;1;2;3];
#test_set = [[10,3,8,7,8,6,9,4,2,7]] #bad center
random_seed = 42

pertubations = [pgen.tripleCoreArchMove, 
                pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,

		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,
		
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,
		
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,

		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,

		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,
		
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,
		
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,
		
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove,

		pgen.tripleCoreArchMove,
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove, 
		pgen.tripleCoreArchMove 
		]

