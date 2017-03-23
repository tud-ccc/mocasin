import cpnxml, architectureDesc, slxmapping
from sys import argv
import argparse
from networkx.drawing.nx_agraph import write_dot
import networkx as nx
import itertools
import pydot

#assumes: 1 group per sched, 1 PE per group !
def mapping_pydot(cpn_filename, mapping_filename, proc_labels=False,pe_labels=True,link_labels=False):
    process2pe, chann2commprim = parse_mapping(mapping_filename)
    pe2process = { pe : [] for pe in process2pe.values()}
    for proc in process2pe:
        pe2process[process2pe[proc]].append(proc)

    parsedfile = cpnxml.parse(cpn_filename,True)
    cpn_graph = pydot.Dot(graph_type='digraph')
    
    for pe in pe2process:
        if pe_labels == True:
            cluster = pydot.Cluster(str(pe),label=str(pe))
        else:
            cluster = pydot.Cluster(str(pe))
        for proc in pe2process[pe]:
            if proc_labels == True:
                cluster.add_node(pydot.Node(str(proc),label=str(proc)))
            else:
                cluster.add_node(pydot.Node(str(proc),label=" "))
        cpn_graph.add_subgraph(cluster)

    
    # Create and add empty fifo channels for all the pn channels
    links_from = {}
    links_to = {}
    
    for pnchannel in parsedfile.get_PNchannel():
        links_from[pnchannel.get_Name()] = []
        links_to[pnchannel.get_Name()] = []
        
    for proc in parsedfile.get_PNprocess():
        for out_edge in  proc.get_PNout().get_Expr():
            links_from[out_edge].append(proc.get_Name())
        for in_edge in  proc.get_PNin().get_Expr():
            links_to[in_edge].append(proc.get_Name())
    
    for link in links_from:
        edges = itertools.product(*[links_from[link],links_to[link]])
        for (v,w) in edges:
            if link_labels == True:
                cpn_graph.add_edge(pydot.Edge(str(v),str(w),label=link))
            else:
                cpn_graph.add_edge(pydot.Edge(str(v),str(w)))
    return cpn_graph

def parse_mapping(filename):

    #init
    process2pe = {}
    chann2mem = {}
    chann2commprim = {}
    #internal: to construct process2pe
    process2sched = {}
    sched2group = {}
    group2pe = {}
    
    parsedfile = slxmapping.parse(filename,True)
    
    #populate schedulers
    for single_sched_desc in parsedfile.get_SingleSchedulerDesc():
        outsched = single_sched_desc.get_OutSchedulerInfo()
        atr_process = outsched.get_AttributedProcesses()
        for process in atr_process.get_Process():
            process2sched[process.get_Name()] = single_sched_desc.get_ID()
    
    
    mapper_desc = parsedfile.get_MapperDesc()
    out_mapper_info = mapper_desc.get_OutMapperInfo()
    grp2pe = out_mapper_info.get_GroupID2PEIDs()
    
    #populate pes
    for pe_group in grp2pe.get_PeGroup():
        group2pe[pe_group.get_GroupId()] = pe_group.get_Processors()
    
    #populate groups
    sched2grps = out_mapper_info.get_Schedulers2Groups()
    for sched2grp in sched2grps.get_Scheduler2Group():
        sched2group[sched2grp.get_SchedulerID()] = sched2grp.get_GroupID()
    
    #populate process-to-processor mapping
    for process in process2sched:
        process2pe[process] = group2pe[sched2group[process2sched[process]]]
    
    #populate communication mapping
    channel_mappings = out_mapper_info.get_ChannelMappings()
    for chann_mapping in channel_mappings.get_ChannelMapping():
        # chann_mapping.get_PnChannel #this would give me the cpn channel name
        sesame_chann_name = chann_mapping.get_ProcessFrom() + "." + chann_mapping.get_PnChannel() + "_in-&gt;" + chann_mapping.get_ProcessTo() + "." + chann_mapping.get_PnChannel() + "_out"
        chann2mem[sesame_chann_name] = chann_mapping.get_Memory()
        chann2commprim[sesame_chann_name] = chann_mapping.get_CommPrimitive()
    return process2pe, chann2commprim

def parse_cpn(filename):
    parsedfile = cpnxml.parse(filename,True)
    cpn_graph = nx.MultiDiGraph()
    
    # Create and add empty fifo channels for all the pn channels
    links_from = {}
    links_to = {}
    
    for proc in parsedfile.get_PNprocess():
        cpn_graph.add_node(proc.get_Name())
    
    for pnchannel in parsedfile.get_PNchannel():
        links_from[pnchannel.get_Name()] = []
        links_to[pnchannel.get_Name()] = []
        
    for proc in parsedfile.get_PNprocess():
        for out_edge in  proc.get_PNout().get_Expr():
            links_from[out_edge].append(proc.get_Name())
        for in_edge in  proc.get_PNin().get_Expr():
            links_to[in_edge].append(proc.get_Name())
    
    for link in links_from:
        edges = itertools.product(*[links_from[link],links_to[link]])
        #cpn_graph.add_edges_from(edges,label=link)
        cpn_graph.add_edges_from(edges,label=link)
    return cpn_graph

def parse_arch(filename):
    parsedfile = architectureDesc.parse(filename,True)
    arch_graph = nx.Graph()
    

    #comm_primitives = {}
    
    # for cp in parsedfile.get_CommPrimitive():
    #     comm_primitives[]
        
    print("Warning! I'm lazy, so the architecture parser is not complete, it just reads the NoC.")

    noc = {}
    i = 0
    for line in parsedfile.get_NocGrid()[0].get_Line():
        j = 0
        lastline = {}
        last = None
        for element in line.get_Element():
            if element.get_NODE() is not None:
                i_noc = element.get_NODE().get_Row()
                j_noc = element.get_NODE().get_Column()
                noc[(i,j)] = ((i_noc,j_noc), element.get_NODE().get_Processors().get_List())
            elif element.get_LINK() is not None:
                noc[(i,j)] = 'L'
            elif element.get_XXXX() is not None:
                noc[(i,j)] = 'N'
            j = j + 1
        i = i + 1
        
    links = []
    for (i,j) in noc:
        if isinstance(noc[(i,j)],tuple):
            ((i_noc,j_noc),proc) = noc[(i,j)]
            if (i-1,j) in noc and (i-2,j) in noc and noc[(i-1,j)] == 'L':
                #print("noc[" + str(i-2) + "," + str(j) + "] = " + str(noc[(i-2,j)]) )
                #for proc2 in noc[(i-2,j)][1]:
                proc2 =  noc[(i-2,j)][1] 
                links.append((proc2,proc))
            
            if (i+1,j) in noc and (i+2,j) in noc and noc[(i+1,j)] == 'L':
                proc2 =  noc[(i+2,j)][1]
                links.append((proc2,proc))
    
            if (i,j-1) in noc and (i,j-2) in noc and noc[(i,j-1)] == 'L':
                proc2 =  noc[(i,j-2)][1]
                links.append((proc2,proc))
            
            if (i,j+1) in noc and (i,j+2) in noc and noc[(i,j+1)] == 'L':
                proc2 =  noc[(i,j+2)][1]
                links.append((proc2,proc))
        
    #print("Links: " + str(links))
    arch_graph.add_edges_from(links)
    return arch_graph

def main(argv):    
    #--------------------------------------------------
    # INITIALIZATION 
    #--------------------------------------------------
    

    argparser = argparse.ArgumentParser(description="visualize_mapping")
    argparser.add_argument("cpnxml", metavar="CPN_description",
                           help = "CPN XML description")
    argparser.add_argument("archdesc", metavar="Architecture_description",
                        help = "Architecture description (.architecture)")
    argparser.add_argument("mapping", metavar="mapping_description",
                           help = "Mapping file (.mapping)")

    argparser.add_argument("--mappingout", metavar="mapping output dot", type=str,
                           help = "Graphviz output for mapping visualization")
    args = argparser.parse_args(argv[1:])

    #--------------------------------------------------
    # FILL UP DATA STRUCTURES 
    #--------------------------------------------------
    cpn_graph = parse_cpn(args.cpnxml)
    write_dot(cpn_graph,'cpngraph.dot')
    process2pe, chann2commprim = parse_mapping(args.mapping)
    arch_graph = parse_arch(args.archdesc)
    nx.write_dot(arch_graph,'archgraph.dot')
    layout = nx.graphviz_layout(arch_graph, prog='fdp', root=None)    #nx.draw(cpn_graph)
    
    mapping = mapping_pydot(args.cpnxml, args.mapping)
    if args.mappingout:
        mapping.write_raw(args.mappingout)
    #print(str(layout))
    #input()

if __name__ == "__main__":
    main(argv)
