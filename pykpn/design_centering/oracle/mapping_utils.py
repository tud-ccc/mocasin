import slxmapping as mapper
import subprocess
import re
import config as conf

# provides methods to generate a new mapping from a given DC-vector
class PartialMapper(object):
    pe2process_map = {}
    max_pe = conf.max_pe
    
    def __init__(self, default_path):
        """Initilize mapping-generator with a path to a default mapping and 
	prefix strings for cores and memory elements """
        #default mapping xml required as template for generated mappings
        self.filename = default_path
	self.parsedfile = mapper.parse(self.filename,True)

    def get_ProcessNames(self):
        """Extract names of all processes in default mapping"""
	process_names = []

	for xmlroot in self.parsedfile.get_SingleSchedulerDesc():
	    for process in xmlroot.get_OutSchedulerInfo().get_AttributedProcesses().get_Process():
		process_names.append(process.get_Name())
        return process_names
    
    def get_ChannelNames(self):
        """Extract names of all channels in default mapping"""
	channel_names = []
	additional_desc = self.parsedfile.get_AdditionalDesc()

	for fifo in additional_desc.get_BoundInfo().get_BoundList().get_FifoBound():
	    channel_names.append(fifo.get_Fifo())
	return channel_names
    
    def find_core2process(self, p_name):
        for xmlroot in self.parsedfile.get_SingleSchedulerDesc():
	    for process in xmlroot.get_OutSchedulerInfo().get_AttributedProcesses().get_Process():
		if (process.get_Name() == p_name):
		    return xmlroot.get_ID()

    def get_defaultPE2ProcessDict(self):
        """Returns the dictionary <process_name>:<PE> defined by the default mapping-XML"""
	pe2process_map = {}
        for process in self.get_ProcessNames():
	    core = self.find_core2process(process)
	    cluster = re.findall('\d+', conf.com_prefix[core][1][1])[0]
	    pe2process_map.update({process:[core,int(cluster)]})
	return pe2process_map
    
    def set_PE2ProcessDict(self, pr2pe_map):
        """Sets the dictionary <process_name>:<PE>"""
	self.pe2process_map = pr2pe_map

    def inconsistancyCheck(self, pr2pe_map):
        """Check for inconsistancies of given pr2pe mapping and default mapping"""
	default_map = self.get_defaultPE2ProcessDict()
	for process in default_map:
	    if process not in pr2pe_map:
		return False
	return True

    def generateFromToList(self, pr2pe_map):
        """Generates a (src,sink) list for all channels"""
        self.adjustChannelMappings(pr2pe_map) # {noc_mem_c0, noc_mem_c0, noc_mem_c0, noc_mem_c0, noc_mem_c14, noc_mem_c12, noc_mem_c12, noc_mem_c2, noc_mem_c13, noc_mem_c2, noc_mem_c1, noc_mem_c1, noc_mem_c10, noc_mem_c10, noc_mem_c11, noc_mem_c11}
        self.adjustSchedGroups(pr2pe_map)
	channel_mappings = self.parsedfile.get_MapperDesc().get_OutMapperInfo().get_ChannelMappings().get_ChannelMapping()
	channel_list = []
        # build list [(from_pe_no, to_pe_no, from_pr_name, to_pr_name), ... , (...)]
	for chan in channel_mappings:
	    p_fr = re.sub('[{:s}]'.format(conf.pe_prefix), '', chan.get_ProcessorFrom())
	    p_to = re.sub('[{:s}]'.format(conf.pe_prefix), '', chan.get_ProcessorTo())
	    channel_list.append((int(p_fr), int(p_to), chan.get_ProcessFrom(), chan.get_ProcessTo()))
        return channel_list

    def get_CommPrimitive(self, mem_core ,src, des):
        """Returns the index of the best communiction primitive for Cn->Cm"""
	costs = conf.comm_network[src][des]
	return conf.com_prefix[mem_core][conf.mem_sel[costs]][1]

    def get_suitableMemory(self, mem_core ,src, des):
        """Returns the index of a suitable memory for the given communication channel Cn->Cm"""
	costs = conf.comm_network[src][des]
	return conf.com_prefix[mem_core][conf.mem_sel[costs]][0]
    
    def get_pe_no(self, cluster_core, cluster):
        return 4 * cluster + cluster_core
    
    def adjustChannelMappings(self, pr2pe_map): #, chan2com_map):
        """Replace from/to channel information of new mapping
        Adjust memory-channel binding with new binding"""
	channel_mappings = self.parsedfile.get_MapperDesc().get_OutMapperInfo().get_ChannelMappings().get_ChannelMapping()
	default_map = self.get_defaultPE2ProcessDict()
	if not self.inconsistancyCheck(pr2pe_map):
	    print ("The given mapping dict does not match the default mapping ... abort")
	    return

	for process in default_map:
	    # adjust TO mapping to values in pe2pr_map
	    to_match = filter(lambda chan: chan.get_ProcessTo() == process, channel_mappings)
	    map(lambda chan : chan.set_ProcessorTo("{:s}{:02d}".format(conf.pe_prefix, 
	             self.get_pe_no(pr2pe_map[process][0],pr2pe_map[process][1]))), to_match)
	    # adjust FROM mapping to values in pe2pr_map
	    from_match = filter(lambda chan: chan.get_ProcessFrom() == process, channel_mappings)
	    map(lambda chan : chan.set_ProcessorFrom("{:s}{:02d}".format(conf.pe_prefix, 
	             self.get_pe_no(pr2pe_map[process][0],pr2pe_map[process][1]))), from_match)
            # adjust memory and comm primitive mapping
	    for mem in from_match:
		#print mem.get_Memory()
		#print (re.findall('\d+', mem.get_Memory())[0])
		#if (re.findall('\d+', mem.get_Memory())[0] == str(default_map[process])):a
                # TODO: write an universal method for this
		#print pr2pe_map[process][0]
		#print pr2pe_map[process][1]
		mem_str = self.get_suitableMemory(
		          self.get_pe_no(pr2pe_map[process][0], pr2pe_map[process][1]),
			  self.get_pe_no(pr2pe_map[process][0], pr2pe_map[process][1]),
			  self.get_pe_no(pr2pe_map[mem.get_ProcessTo()][0], pr2pe_map[mem.get_ProcessTo()][1]))
		comm_str = self.get_CommPrimitive(
		          self.get_pe_no(pr2pe_map[process][0], pr2pe_map[process][1]),
			  self.get_pe_no(pr2pe_map[process][0], pr2pe_map[process][1]),
			  self.get_pe_no(pr2pe_map[mem.get_ProcessTo()][0], pr2pe_map[mem.get_ProcessTo()][1]))
		#else:
		#    mem_str = self.get_suitableMemory(pr2pe_map[mem.get_ProcessTo()], pr2pe_map[process], pr2pe_map[mem.get_ProcessTo()])
		#    comm_str = self.get_CommPrimitive(pr2pe_map[mem.get_ProcessTo()], pr2pe_map[process], pr2pe_map[mem.get_ProcessTo()])
		mem.set_Memory("{:s}".format(mem_str))
		mem.set_CommPrimitive("{:s}".format(comm_str))
	 
	
    def adjustSchedGroups(self, pr2pe_map):
        """Adapt scheduling groups to new mapping"""
	default_map = self.get_defaultPE2ProcessDict()
	schedulers = self.parsedfile.get_SingleSchedulerDesc()
	if not self.inconsistancyCheck(pr2pe_map):
	    print ("03 The given mapping dict does not match the default mapping ... abort")
	    return

	for sched in schedulers:
            #remove old processes
	    sched.get_OutSchedulerInfo().get_AttributedProcesses().set_Process([])
            # filter all (pr:pe) tuples using the same processing element
	    dict2add = {pr:  self.get_pe_no(pe[0], pe[1]) 
	                for pr, pe in pr2pe_map.items() if self.get_pe_no(pe[0], pe[1]) == sched.get_ID()}
	    for pr,pe in dict2add.items():
		new_pr = mapper.ProcessAttribute.factory()
		new_pr.set_Name(pr)
		# The attributedProcess may need an attribute too
		new_pr.set_Attribute(1)
		sched.get_OutSchedulerInfo().get_AttributedProcesses().add_Process(new_pr)

    def generatePr2PeMap(self, mapping):
        """Map the given mapping-vector to a sorted pr2pe dict. The resulting mapping starts with 
	the first value of the vector for the first process name (alphabetic order) and so forth..."""
	if (len(mapping) <= conf.num_pr):
    	    mapping = self.map2extmap(mapping) 
	default_map = self.get_defaultPE2ProcessDict()
	if (len(default_map) != (len(mapping) / conf.cluster_lvl)):
	    print ("01 The given mapping vector length does not match the default mapping ... abort")
	    return
	if not all(pe <= conf.cores_per_cluster-1 for pe in mapping):
	    print ("02 The given mapping vector contains invalid PEs ... abort")
	    return
	
	pr2pe_map = {}
	i = 0
        # generate new map sorted by processes
	for item in sorted(default_map):
	    mapping[i]
	    pr2pe_map.update({item:[mapping[i],mapping[i+1]]})
	    i = i+2
	    
	return pr2pe_map

    def XMLfile_postprocess(self, path):
        """This method is a hack to generate valid XML files for the
	picky XML parser in maps"""
	xmlout = open(path, "r")
	preserve = "slxMapping:SlxMappingDescriptor"
	delete = "slxMapping:" #avoid double definitions of namespaces
	reworked = []
	reworked.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n")
	
	for line in xmlout:
	    if preserve in line:
	        reworked.append(line)
		continue
	    elif delete in line:
		line = line.replace(delete, "")
	    reworked.append(line)
	xmlout.close()
	xmlout = open(path, "w")
	for line in reworked:
	    xmlout.write(line)
	xmlout.close()

    def export2XML(self, path, pr2pe_map):  
        """Export a mapping XML file for the given pr2pe mapping"""
        self.adjustChannelMappings(pr2pe_map)
        self.adjustSchedGroups(pr2pe_map)
        xmlout = open(path, "w")
        self.parsedfile.export(xmlout,0)
	xmlout.close()
	self.XMLfile_postprocess(path)
    
    def extmap2map(self, ext_mapping):
        mapping = []
        for i in range(0,len(ext_mapping)):
	    if (i % 2 == 0):
		mapping.append(self.get_pe_no(ext_mapping[i], ext_mapping[i+1]))
        return mapping

    def map2extmap(self, mapping):
        ext_mapping = []
	for i in range(0,len(mapping)):
	    cluster = re.findall('\d+', conf.com_prefix[mapping[i]][1][1])[0]	    
	    ext_mapping.append(mapping[i]%4)
	    ext_mapping.append(int(cluster))
        return ext_mapping


class MappingTester(object):
    
    def trace(self, xml_path, tool_path, bm):
        result = subprocess.check_output(["{:s}/app_analysis/kpn/kpn_synth/app/bin/kpnsynthapp".format(tool_path), 
                         "--pn-graph", "{:s}/apps/cpn/{:s}/generator/.cpnxml/sobel.cpn.xml".format(tool_path, bm, bm), 
        		 "--trace-format", "bb", 
        		 "--architecture", "{:s}/platforms/platform_descriptions/{:s}".format(tool_path, conf.architecture), 
        		 "--log-verbosity", "VERBO", 
        		 "--log-folder", ".log", 
        		 "--trace-folder", "{:s}/apps/cpn/{:s}/mapper/.cpntrace".format(tool_path, bm),
			 "--replay", "{:s}".format(xml_path)],stderr=subprocess.STDOUT, shell=False)
	return result
        #return "Total execution time: 197.00 ms"

    def extract_TraceResults(self, trace_out):
	res = []
        for line in trace_out.split('\n'):
	     #expect utf-8!!!
	    if (re.findall("Total execution time: [-+]?\d*\.\d+ \xc2\xb5s|Total execution time: \d+ \xc2\xb5s", line)):
		res = re.findall("[-+]?\d*\.\d+|\d+", line)
		res = float(res[0]) / 1000
	    elif (re.findall("Total execution time: [-+]?\d*\.\d+ ms|\d+ ms", line)):
		res = re.findall("[-+]?\d*\.\d+|\d+", line)
		res = float(res[0])
	    else:
		continue
        return res
