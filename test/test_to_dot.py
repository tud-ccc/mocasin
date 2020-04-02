# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import filecmp
import subprocess
import os


def test_slx_kpn_to_dot(datadir, expected_dir, slx_kpn):
    dot_file = "%s.dot" % slx_kpn
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "kpn_to_dot",
                           "kpn=%s" % slx_kpn,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file)


def test_slx_platform_to_dot(datadir, expected_dir, slx_platform):
    dot_file = "%s.dot" % slx_platform
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "platform_to_dot",
                           "platform=%s" % slx_platform,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file)


def test_slx_mapping_to_dot(datadir, expected_dir, slx_kpn_platform_pair):
    kpn, platform, version = slx_kpn_platform_pair
    dot_file = "%s_on_%s.dot" % (kpn, platform)
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "mapping_to_dot",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "mapping=slx_default",
                           "slx.version=%s" % version,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file)


def test_tgff_kpn_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.kpn.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "kpn_to_dot",
                           "kpn=tgff_reader",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file)


def test_tgff_platform_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.platform.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "platform_to_dot",
                           "platform=tgff_reader",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file)


def test_tgff_mapping_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.mapping.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "platform_to_dot",
                           "platform=tgff_reader",
                           "kpn=tgff_reader",
                           "mapping=random_mapping",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    # Cannot validate random mappings
