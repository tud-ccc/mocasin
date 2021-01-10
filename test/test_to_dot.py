# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import filecmp
import pytest
import subprocess
import os


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_slx_kpn_to_dot(datadir, expected_dir, slx_kpn):
    dot_file = "%s.dot" % slx_kpn
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "kpn_to_dot",
                           "kpn=%s" % slx_kpn,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_slx_platform_to_dot(datadir, expected_dir, slx_platform):
    dot_file = "%s.dot" % slx_platform
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "platform_to_dot",
                           "platform=%s" % slx_platform,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_slx_mapping_to_dot(datadir, expected_dir, slx_kpn_platform_pair):
    kpn, platform = slx_kpn_platform_pair
    dot_file = "%s_on_%s.dot" % (kpn, platform)
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "mapping_to_dot",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "mapper=slx_default",
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


def test_tgff_kpn_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.kpn.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "kpn_to_dot",
                           "kpn=tgff_reader",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


def test_tgff_platform_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.platform.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "platform_to_dot",
                           "platform=designer_bus",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


def test_tgff_mapping_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.mapping.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "mapping_to_dot",
                           "platform=designer_bus",
                           "kpn=tgff_reader",
                           "mapper=random",
                           "mapper.random_seed=42",
                           "tgff.file=%s.tgff" % tgff,
                           "output_file=%s" % out_file],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)


def test_sdf3_kpn_to_dot(datadir, expected_dir):
    dot_file = "sdf3_medium_cyclic.dot"
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(["pykpn", "kpn_to_dot",
                           "kpn=sdf3_reader",
                           "sdf3.file=../../../sdf3/medium_cyclic.xml",
                           f"output_file={out_file}"],
                          cwd=datadir)
    assert filecmp.cmp(os.path.join(expected_dir, dot_file), out_file,
                       shallow=False)
