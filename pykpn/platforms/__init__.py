# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pykpn.platforms import Tomahawk2Platform
from pykpn.platforms import GenericNocPlatform


# TODO see if we can implement this in a better way

def createPlatformByName(name):
    if name is None:
        raise ValueError('Define the platform')

    elif name[0:name.find('_')] == 'generic':
        temp1 = name.find('_')
        temp2 = name[temp1 + 1:].find('_')
        arch = name[temp1 + 1:temp1 + temp2 + 1]
        x = int(name[-1])
        y = int(name[-3])
        return GenericNocPlatform(arch, x, y)

    elif name == 'tomahawk2':
        return (Tomahawk2Platform())
    else:
        raise ValueError('Platform does not exist')
