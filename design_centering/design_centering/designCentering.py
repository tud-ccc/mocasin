#!/usr/bin/python
import re
import sys
import json
import logging
import dcUtils as dcu
import matplotlib.pyplot as plt


# take this valuses from config.p later
sample      = dcu.cube_sample     # return the next sample within volume
adaptation  = dcu.cube_adaptation # volume adaptation
oracle      = dcu.test_oracle     # return the feasability of a sample

max_samples   = 100  # maximum number of samples
adapt_samples = 10   # interval for adaption of p-value

max_pe = 16

class DesignCentering(object):
    samples = {}

    def ds_explore(self):
        """ explore design space (main loop of the DC algorithm) """
	for i in range(0,max_samples+1, adapt_samples):
	    for j in range(0,adapt_samples+1):
		s = sample()
		print oracle(s)
		self.samples.update({tuple(s):oracle(s)})
		adaptation()
		#print("i: {:d} j:{:d}".format(i,j))

    def plot_samples(self):
        for point in self.samples:
	    if self.samples[point]:
		plt.plot(point[0], point[1],"o", color='b')
	    else:
		plt.plot(point[0], point[1],"o", color='r')
	plt.xticks(range(0, max_pe-1, 1))
	plt.yticks(range(0, max_pe-1, 1))
	plt.show()


def main(argv):
    print "===== run DC ====="
    logging.basicConfig(filename="dc.log", level=logging.DEBUG)
    logging.debug(" mu: {:f} radius: {:f}".format(1.1, 3.14))
    if (len(argv) > 1):
	try:
	    sample = json.loads(argv[1])
	except ValueError:
	    print(" {:s} is not a vector \n".format(argv[1]))
	    sys.stderr.write("JSON decoding failed (in read file) \n")
	# run DC algorithm    
	dc = DesignCentering()
	dc.ds_explore()
	dc.plot_samples()
	print oracle(sample)
    else:
	print "usage: python designCentering [x1,x2,...,xn]\n"

    
    return 0

if __name__ == "__main__":
    main(sys.argv)

