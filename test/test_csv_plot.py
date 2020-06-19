# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import subprocess
import filecmp
import os

def test_csv_plot(datadir, expected_dir, csv_file_path):
    file_path = os.path.join(datadir, csv_file_path)
    out_file = os.path.join(datadir, "csv_output.txt")

    subprocess.check_call(["pykpn", "csv_plot",
                           "kpn=audio_filter",
                           "platform=exynos",
                           "csv_file=%s" % file_path,
                           "log_to_file=True",
                           "output_file=%s" % out_file,
                           "prefix=default",
                           "suffix=default",
                           "property=wall_clock_time"],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, "audio_filter_exynos.txt"), out_file)

