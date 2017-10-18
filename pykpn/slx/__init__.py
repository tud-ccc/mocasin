# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

# a list of supported SLX versions


_VERSIONS = ['2017.10', '2017.04']


_version = None


def set_version(version):
    global _version
    if _version is None:
        if version in _VERSIONS:
            _version = version
        else:
            raise ValueError('SLX Version %s is not supported' % (version))
    else:
        raise RuntimeError('The SLX version may only be set once and only '
                           'before get_version() is called')


def get_version():
    global _version
    if _version is None:
        # set default
        _version = _VERSIONS[0]
    return _version
