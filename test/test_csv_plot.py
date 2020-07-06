# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andrés Goens

import subprocess
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
                           "show_plot=False",
                           "prefix=default",
                           "suffix=default",
                           "property=wall_clock_time"],
                          cwd=datadir)

    #we cannot expect the same output every time, but we want a sane output (for now, we will just count the number of lines)
    num_lines = sum(1 for line in open(out_file))
    assert num_lines == 199

