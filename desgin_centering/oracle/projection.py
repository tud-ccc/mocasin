#!/usr/bin/python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import mapping_utils as mu
import config as conf
import itertools
import numpy as np
import json
import re

#draw a vector
import pylab
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    """Defines an arrow in 3D space"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

class ProjectionGenerator(object):
     def read_LogFile(self, path, threshold):
         """Generate a mapping [([mapping],bool),...,([mapping],bool)]"""
         log = open(path, "r")
	 log_map = []
	 for line in log:
	     vec = re.findall("\[\d+\,.+\]",line)
	     nextline = log.next()
	     val = re.findall("[-+]?\d*\.\d+|\d+",nextline)
	     if (len(vec) > 0):
		 try:
		     mapping = json.loads(vec[0])
		 except ValueError:
		     sys.stderr.write("JSON decoding failed")

	     log_map.append((mapping,float(val[0]) < threshold))
         return log_map
     
     def simple_scatter(self, data, title):
	 #x = np.arange(1, 101)
	 #y = 20 + 3 * x + np.random.normal(0, 60, 100)
	 data_x = []
	 data_y = []
	 m_size = []
	 for x in data:
	     data_x.append(x)
	     data_y.append(float(data[x][0]) / float(data[x][0] + data[x][1]))
	     m_size.append(float(data[x][0] + data[x][1]))
	 fig = plt.figure()
	 fig.suptitle(title)
	 ax1 = fig.add_subplot(111)
	 ax1.scatter(data_x, data_y, marker="o", s=m_size)
     
     def pshow(self):
         plt.show()

     def plot_mapping(self, pr2pe_map, channel_list, arch_mapping, dim_x, dim_y, c):
         """Special function that draw mappings for 3x3 NOC architectures only"""
         fig = plt.figure(figsize=(15,10))
	 ax = fig.add_subplot(111, projection='3d')
	 depth = {}
	 x=0
	 # set a height for each pocess
	 for mapping in pr2pe_map:
	     depth.update({mapping:x})
	     x = x+1
	 
	 cnt = 0
	 for pe in pr2pe_map: # must be a list
	     #pe_To_map = {}
	     ax.scatter(arch_mapping[pr2pe_map[pe][0]][0],arch_mapping[pr2pe_map[pe][0]][1], depth[pe], marker="o", color=c)
	     ax.text(arch_mapping[pr2pe_map[pe][0]][0],arch_mapping[pr2pe_map[pe][0]][1], depth[pe], pe, size=8, zorder=1)

         for chan in channel_list:
	     sx = arch_mapping[chan[0]][0]
	     sy = arch_mapping[chan[0]][1]
	     sz = depth[chan[2]]
	     tx = arch_mapping[chan[1]][0]
	     ty = arch_mapping[chan[1]][1]
	     tz = depth[chan[3]]
	     arr = Arrow3D([sx,tx], [sy,ty],[sz,tz], mutation_scale=20, lw=1, arrowstyle="->", color="#555555")
	     ax.add_artist(arr)
	     cnt= cnt + 1

	 print("No of Channels: {:d}".format(cnt))

	 ax.set_xlabel("Cores X")
	 ax.set_ylabel("Cores Y")
	 ax.set_zlabel("Process")
	 ax.set_xlim3d(0, dim_x)
         ax.set_ylim3d(0, dim_y)
         ax.set_zlim3d(0, len(depth)-1)
	 plt.show()
	 return
     
     def line_chart(self, ):
         fig = plot.figure(1)
	 DAU = (  2,  20,  25,  60, 190, 210,  18, 196, 212)
	 WAU = ( 50, 160, 412, 403, 308, 379, 345, 299, 258)
	 MAU = (760, 620, 487, 751, 612, 601, 546, 409, 457)
	 
	 firstDay = datetime.datetime(2012,1,15)
	 
	 #create an array with len(DAU) entries from given starting day
	 dayArray = [firstDay + datetime.timedelta(days = i) for i in xrange(len(DAU))]

         line1 = plot.plot(dayArray, DAU, 'o-', color = '#336699')
	 line2 = plot.plot(dayArray, WAU, 'o-', color = '#993333')
	 line3 = plot.plot(dayArray, MAU, 'o-', color = '#89a54e')
	 
	 ax = plot.subplot(111)
	 dateLocator   = mticker.MultipleLocator(2)
	 dateFormatter = dates.DateFormatter('%d.%m.%Y')
	 ax.xaxis.set_major_locator(dateLocator)
	 ax.xaxis.set_major_formatter(dateFormatter)
	 fig.autofmt_xdate(rotation = 90, ha = 'center')
	 
	 yMax = max(np.max(DAU), np.max(WAU), np.max(MAU))
	 yLimit = 100 - (yMax % 100) + yMax
	 plot.yticks(np.arange(0, yLimit + 1, 100))

	 plot.title('Active users', weight = 'bold')
	 plot.grid(True, axis = 'both')
	 plot.subplots_adjust(bottom = 0.2)
	 plot.subplots_adjust(right = 0.82)

     def mark_dc(self, val, dc):
        if dc == val:
	    return val
	else:
	    return 0

     def multidim_line_chart(self, log):
     	for mapping, bool_res in log:
	    if bool_res:
	        #plt.plot ( np.arange(0,10),mapping,'.-',label='feasible', color='r' )
		continue
            else:
		plt.plot ( np.arange(0,10),mapping,'o-',label='infeasable', color='b' )

	plt.plot ( np.arange(0,10),conf.test_set[0],'.-',label='feasible', color='r' )
	plt.xlabel('x axis')
	plt.ylabel('y axis')
	plt.title('my sample graphs')
	plt.legend(('sample1','sample2'))
	#savefig("sampleg.png",dpi=(640/8))
        pass

     def bar_chart(self, dc, results, x_len=1, y_len=1, x_label="", y_label=""):
        """Draws a simple bar chart. 
	Input: list of floats and optional x_len, y_len, X-Label, Y-Label"""

        ind = np.arange(x_len)  # the x locations for the groups
        width = 0.3       # the width of the bars
        
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, results, width, color='r')
	dc_peaks = map(lambda x: self.mark_dc(x,dc) ,results)
        rects1 = ax.bar(ind, dc_peaks, width, color='b')
        
        # add some text for labels, title and axes ticks
        ax.set_ylabel('Mappings passed in %')
        ax.set_title('Pertubation Chart')
        ax.set_xticks(ind + width)
	xtick_label = []
	for i in range(0, 200, 1):
	    if ((i % 10) == 0):
		xtick_label.append("M{:d}".format(i))
            else:
		xtick_label.append("")
        ax.set_xticklabels(xtick_label)
        plt.show()
        #ax.legend((rects1[0]), ('Mapping'))

     def scatterplot_matrix(self, data_1, data_2, names, **kwargs):
        """Plots a scatterplot matrix of subplots.  Each row of "data" is plotted
        against other rows, resulting in a nrows by nrows grid of subplots with the
        diagonal subplots labeled with "names".  Additional keyword arguments are
        passed on to matplotlib's "plot" command. Returns the matplotlib figure
        object containg the subplot grid."""

	mpl.rcParams['font.size']=8 #font size=8 for the whole figure
        numvars, numdata = data_1.shape
        numvars, numdata = data_2.shape
        fig, axes = plt.subplots(nrows=numvars, ncols=numvars, figsize=(12,12))
        fig.subplots_adjust(hspace=0.05, wspace=0.05)

        for ax in axes.flat:
	    # Hide all ticks and labels
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)

            # Set up ticks only on one side for the "edge" subplots...
            if ax.is_first_col():
                ax.yaxis.set_ticks_position('left')
            if ax.is_last_col():
                ax.yaxis.set_ticks_position('right')
            if ax.is_first_row():
                ax.xaxis.set_ticks_position('top')
            if ax.is_last_row():
		ax.xaxis.set_ticks_position('bottom')

        # Plot the data.
        for i, j in zip(*np.triu_indices_from(axes, k=1)):
            for x, y in [(i,j), (j,i)]:
		#print data_1
		#print data_2
                axes[x,y].plot(data_1[x], data_1[y], color='b', **kwargs)
                axes[x,y].plot(data_2[x], data_2[y], color='r', **kwargs)

        # Label the diagonal subplots...
        for i, label in enumerate(names):
            axes[i,i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                    ha='center', va='center')

        # Turn on the proper x or y axes ticks.
        for i, j in zip(range(numvars), itertools.cycle((-1, 0))):
            axes[j,i].xaxis.set_visible(True)
            axes[i,j].yaxis.set_visible(True)

        return fig

     def plot(self, dim_x, dim_y, dim_z, vmin, vmax, log):
         fig = plt.figure()
	 ax = fig.add_subplot(111, projection='3d')
	 num_matches = 0
	 for mapping, bool_res in log:
	     if bool_res:
		 ax.scatter(mapping[dim_x],mapping[dim_y],mapping[dim_z],marker="^", color="b")
		 num_matches=num_matches+1
             else:
		 ax.scatter(mapping[dim_x],mapping[dim_y],mapping[dim_z],marker="v", color="r")
		 num_matches=num_matches+1

	         #print mapping 
         
	 ax.set_xlabel("dim_0")
	 ax.set_ylabel("dim_1")
	 ax.set_zlabel("dim_2")
	 ax.set_xlim3d(vmin, vmax)
         ax.set_ylim3d(vmin, vmax)
         ax.set_zlim3d(vmin, vmax)
	 plt.show()
	 print("Found matches: {:d}\n".format(num_matches))
	 return
         
     
def main():
    arch_mapping = conf.arch_mapping 
    vmin = 0
    vmax = conf.max_pe
    num_pr = conf.num_pr
    dim_x = 3
    dim_y = 3
    dim_z = 3
   
    p = ProjectionGenerator()

    numvars, numdata = 4, 10
    data_true = np.empty(shape=(num_pr,0))
    data_false = np.empty(shape=(num_pr,0))

    
    log_map = p.read_LogFile(conf.log_path, conf.threshold) # [([c1,c2,c3,...,cn],bool),...,(...)]
    pr_names = []

    mapgen = mu.MappingGenerator(conf.default_path)

    #p.multidim_line_chart(log_map)
    #p.simple_scatter(log_map)

    # gather data for scatter matrix
    for mapping, bool_res in log_map:
        # generate new mapping-XML similar to a given default mapping
        mapgen = mu.MappingGenerator(conf.default_path)
        pr2pe_map = mapgen.generatePr2PeMap(mapping)
        pr_names = sorted(pr2pe_map) #alphabetic list of keys
        #channel_list = mapgen.generateFromToList(pr2pe_map)

        # Design Center
        # m = np.array([[11,9,9,11,10,5,5,10,3,9]])
        m = np.array([conf.test_set[0]])
        data_true = np.concatenate((data_true,m.T),axis=1)

        if bool_res:
            #p.plot_mapping(pr2pe_map, channel_list, arch_mapping, dim_x, dim_y, "b")
            
            m = np.array([mapping])
            data_true = np.concatenate((data_true,m.T),axis=1)
            #continue
            #p.plot(0,1,2,0,15,log_map)
        else:
            m = np.array([mapping])
            data_false = np.concatenate((data_false,m.T),axis=1)

            #p.plot_mapping(pr2pe_map, channel_list, arch_mapping, dim_x, dim_y, "r")



    pr2pe_map = mapgen.generatePr2PeMap(conf.test_set[0])
    channel_list = mapgen.generateFromToList(pr2pe_map)
    p.plot_mapping(pr2pe_map, channel_list, arch_mapping, dim_x, dim_y, "b")

    fig = p.scatterplot_matrix(data_false, data_true, pr_names, linestyle='none', marker='.', mfc='none')
    fig.suptitle("Scatterplot Matrix: {:s}".format(conf.benchmark))
    plt.show()
    return


if __name__ == "__main__": main()
