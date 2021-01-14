# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os
import pytest


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_symmetries_slx(datadir,slx_platform):
    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=audio_filter",
                           f"platform={slx_platform}",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym_json/",
                           f"platform.symmetries_json=../../../platform/symmetries/{slx_platform}.json",
                           "trace=slx_default"],
                          cwd=datadir)

    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=audio_filter",
                           f"platform={slx_platform}",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym_nauty/",
                           "platform.symmetries_json=null",
                           "trace=slx_default"],
                          cwd=datadir)

    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=audio_filter",
                           f"platform={slx_platform}",
                           "representation=Symmetries",
                           "representation.disable_mpsym=true",
                           "mapper=genetic",
                           "outdir=../../../python/",
                           "trace=slx_default"],
                          cwd=datadir)

    try:
        mpsym_json_file_path = os.path.join(datadir, 'mpsym_json/best_time.txt')
        mpsym_nauty_file_path = os.path.join(datadir, 'mpsym_nauty/best_time.txt')
        python_file_path = os.path.join(datadir, 'python/best_time.txt')
        mpsym_json_file = open(mpsym_json_file_path, 'r')
        mpsym_nauty_file = open(mpsym_nauty_file_path, 'r')
        python_file = open(python_file_path, 'r')
        mpsym_json_line = mpsym_json_file.readline()
        mpsym_nauty_line = mpsym_nauty_file.readline()
        python_line = python_file.readline()
        while python_line != '' or mpsym_json_line != '' or mpsym_nauty_line != '':
            assert python_line == mpsym_json_line, python_line and mpsym_json_line
            assert python_line == mpsym_nauty_line, mpsym_nauty_line and mpsym_json_line
            python_line = python_file.readline()
            mpsym_json_line = mpsym_json_file.readline()
            mpsym_nauty_line = mpsym_nauty_file.readline()
        python_file.close()
        mpsym_json_file.close()
        mpsym_nauty_file.close()
    except FileNotFoundError:
        assert False

@pytest.mark.skip(reason="Test just takes too long.")
def test_symmetries_tgff_large(datadir,designer_platform_large):
    tgff_dir = os.path.join(datadir, 'tgff/e3s-0.9')
    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           f"platform={designer_platform_large}",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym/",
                           f"platform.symmetries_json=../../../platform/symmetries/{designer_platform_large}.json",
                           "trace=tgff_reader"],
                          cwd=datadir)

    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           f"platform={designer_platform_large}",
                           "representation=Symmetries",
                           "representation.disable_mpsym=true",
                           "mapper=genetic",
                           "outdir=../../../python/",
                           "trace=tgff_reader"],
                          cwd=datadir)

    try:
        mpsym_file_path = os.path.join(datadir, 'mpsym/best_time.txt')
        mpsym_file = open(mpsym_file_path, 'r')
        python_file_path = os.path.join(datadir, 'python/best_time.txt')
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

def test_symmetries_tgff_small(datadir,designer_platform_small):
    tgff_dir = os.path.join(datadir, 'tgff/e3s-0.9')
    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           f"platform={designer_platform_small}",
                           "representation=Symmetries",
                           "mapper=genetic",
                           "outdir=../../../mpsym/",
                           f"platform.symmetries_json=../../../platform/symmetries/{designer_platform_small}.json",
                           "trace=tgff_reader"],
                          cwd=datadir)

    subprocess.check_call(["mocasin", "generate_mapping",
                           "kpn=tgff_reader",
                           "tgff.directory=%s" % tgff_dir,
                           "tgff.file=auto-indust-cords.tgff",
                           f"platform={designer_platform_small}",
                           "representation=Symmetries",
                           "representation.disable_mpsym=true",
                           "mapper=genetic",
                           "outdir=../../../python/",
                           "trace=tgff_reader"],
                          cwd=datadir)

    try:
        mpsym_file_path = os.path.join(datadir, 'mpsym/best_time.txt')
        mpsym_file = open(mpsym_file_path, 'r')
        python_file_path = os.path.join(datadir, 'python/best_time.txt')
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
