# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os


def test_symmetries_slx(datadir):
    subprocess.check_call(["pykpn", "generate_mapping",
                           "kpn=audio_filter",
                           "platform=exynos",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym",
                           "platform.symmetries_json=../../../platform/symmetries/exynos.json",
                           "trace=slx_default"],
                          cwd=datadir)

    subprocess.check_call(["pykpn", "generate_mapping",
                           "kpn=audio_filter",
                           "platform=exynos",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../python",
                           "platform.symmetries_json=null",
                           "trace=slx_default"],
                          cwd=datadir)

    try:
        mpsym_file_path = os.path.join(datadir, 'mpsym/generated_mapping')
        mpsym_file = open(mpsym_file_path, 'r')
        python_file_path = os.path.join(datadir, 'python/generated_mapping')
        python_file = open(python_file_path, 'r')
        python_line = python_file.readline()
        mpsym_line = mpsym_file.readline()
        while python_line != '' and mpsym_line != '':
            assert python_line == mpsym_line
            python_line = python_file.readline()
            mpsym_line = mpsym_file.readline()
        python_file.close()
        mpsym_file.close()
    except FileNotFoundError:
        assert False

def test_symmetries_tgff(datadir):
    tgff_dir = os.path.join(datadir, 'tgff/e3s-0.9')
    subprocess.check_call(["pykpn", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           "platform=coolidge",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym",
                           "platform.symmetries_json=../../../platform/symmetries/coolidge.json",
                           "trace=tgff_reader"],
                          cwd=datadir)

    subprocess.check_call(["pykpn", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           "platform=coolidge",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../python",
                           "platform.symmetries_json=null",
                           "trace=tgff_reader"],
                          cwd=datadir)

    try:
        mpsym_file_path = os.path.join(datadir, 'mpsym/generated_mapping')
        mpsym_file = open(mpsym_file_path, 'r')
        python_file_path = os.path.join(datadir, 'python/generated_mapping')
        python_file = open(python_file_path, 'r')
        python_line = python_file.readline()
        mpsym_line = mpsym_file.readline()
        while python_line != '' and mpsym_line != '':
            assert python_line == mpsym_line
            python_line = python_file.readline()
            mpsym_line = mpsym_file.readline()
        python_file.close()
        mpsym_file.close()
    except FileNotFoundError:
        assert False
