#!/usr/bin/python
import mapping_utils as mu
import sys
import config

def main(argv):
    # generate new mapping-XML similar to a given default mapping
    mapgen = mu.PartialMapper(config.default_path)
    pr2pe_map =  mapgen.get_defaultPE2ProcessDict()
    print pr2pe_map
    return

if __name__ == "__main__":
    main(sys.argv)
