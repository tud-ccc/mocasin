# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os

def test_generate_mapping_slx(datadir, slx_kpn,representation):
    subprocess.check_call(["pykpn", "pareto_front",
                           "kpn=%s" % slx_kpn,
                           "platform=exynos",
                           "representation=%s" % representation,
                           "outdir=../../../",
                           "trace=slx_default"],
                          cwd=datadir)

    try:
        file_path = os.path.join(datadir, 'mapping0.pickle')
        file = open(file_path, 'r')
        file.close()
    except FileNotFoundError:
        assert False

def test_generate_mapping_tgff(datadir, tgff):
    tgff_dir = os.path.join(datadir, 'tgff/e3s-0.9')
    subprocess.check_call(["pykpn", "pareto_front",
                           "kpn=tgff_reader",
                           "platform=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=%s.tgff" % tgff,
                           "outdir=../../../",
                           "trace=tgff_reader"],
                          cwd=datadir)
    try:
        file_path = os.path.join(datadir, "results0.txt")
        file = open(file_path, 'r')
        file.close()
    except FileNotFoundError:
        assert False
