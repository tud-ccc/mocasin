# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import os

def test_dc_audio_filter_exynos(datadir):
    kpn = "audio_filter"
    platform = "exynos"
    trace_dir = os.path.join(datadir, 'slx/app/%s/%s/traces' % (kpn, platform))

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_reader",
                           "trace.directory=%s" % trace_dir,
                           "out_dir=%s" % datadir],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

def test_dc_audio_filter_parallella(datadir):
    kpn = "audio_filter"
    platform = "parallella"
    trace_dir = os.path.join(datadir, 'slx/app/%s/%s/traces' % (kpn, platform))

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_reader",
                           "trace.directory=%s" % trace_dir,
                           "out_dir=%s" % datadir],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

def test_dc_audio_filter_multidsp(datadir):
    kpn = "audio_filter"
    platform = "multidsp"
    trace_dir = os.path.join(datadir, 'slx/app/%s/%s/traces' % (kpn, platform))

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_reader",
                           "trace.directory=%s" % trace_dir,
                           "out_dir=%s" % datadir],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

def test_dc_hog_exynos(datadir):
    kpn = "hog"
    platform = "exynos"
    trace_dir = os.path.join(datadir, 'slx/app/%s/%s/traces' % (kpn, platform))

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_reader",
                           "trace.directory=%s" % trace_dir,
                           "out_dir=%s" % datadir],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

def test_dc_speaker_recognition_exynos(datadir):
    kpn = "speaker_recognition"
    platform = "exynos"
    trace_dir = os.path.join(datadir, 'slx/app/%s/%s/traces' % (kpn, platform))

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_reader",
                           "trace.directory=%s" % trace_dir,
                           "out_dir=%s" % datadir],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

