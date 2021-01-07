# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Felix Teweleit, Andres Goens


import pytest
import os

@pytest.fixture
def datadir(tmpdir):
    """
    Fixture that prepares a data directory for running tests. The resulting
    directory contains symbolic links to the examples directory.
    """
    module_path = os.path.dirname(__file__)
    examples_path = os.path.join(module_path, "..", "examples")

    os.symlink(os.path.join(examples_path, "conf"),
               os.path.join(tmpdir, "conf"))
    os.symlink(os.path.join(examples_path, "slx"),
               os.path.join(tmpdir, "slx"))
    os.symlink(os.path.join(examples_path, "tgff"),
               os.path.join(tmpdir, "tgff"))
    os.symlink(os.path.join(examples_path, "sdf3"),
               os.path.join(tmpdir, "sdf3"))
    os.symlink(os.path.join(examples_path, "csv"),
               os.path.join(tmpdir, "csv"))
    os.symlink(os.path.join(examples_path, "tetris"),
               os.path.join(tmpdir, "tetris"))
    os.symlink(os.path.join(examples_path, "platform"),
               os.path.join(tmpdir, "platform"))

    return tmpdir

@pytest.fixture
def expected_dir(request):
    module_path = os.path.dirname(request.module.__file__)
    module_name, _ = os.path.splitext(os.path.basename(request.module.__file__))
    return os.path.join(module_path, "expected_%s" % module_name)

@pytest.fixture(params=[True,False])
def mpsym(request):
    return request.param

@pytest.fixture(params=["exynos", "multidsp", "parallella"])
def slx_platform(request):
    return request.param

@pytest.fixture(params=["exynos990", "designer_bus", "generic_mesh", "mppa_coolidge","multi_cluster","designer_odroid"])
def designer_platform(request):
    return request.param

#exclude coolidge, haec for time
@pytest.fixture(params=["exynos990", "designer_bus", "generic_mesh","multi_cluster"])
def designer_platform_small(request):
    return request.param

@pytest.fixture(params=["haec", "mppa_coolidge"])
def designer_platform_large(request):
    return request.param

@pytest.fixture(params=["slx_default", "random", "static_cfs", "random_walk", "tabu_search", "gradient_descent", "genetic",  "simulated_annealing", "gbm"])
def slx_mapper(request):
    return request.param

@pytest.fixture(params=["random", "random_walk", "gbm"])
def tgff_mapper(request):
    return request.param

@pytest.fixture(params=["SimpleVector", "MetricSpaceEmbedding", "Symmetries"])
def representation(request):
    return request.param

@pytest.fixture(params=["audio_filter"])
def slx_kpn(request):
    return request.param

@pytest.fixture(params=[("audio_filter", "exynos"),
                        ("audio_filter", "multidsp"),
                        ("audio_filter", "parallella")])
def slx_kpn_platform_pair(request):
    return request.param

@pytest.fixture(params=["auto-indust-cords"])
def tgff(request):
    return request.param

@pytest.fixture(params=[("'EXISTS fft_l MAPPED ARM00'", 0),
                        ("'EXISTS NOT ARM00 PROCESSING'", 1),
                        ("'EXISTS RUNNING TOGETHER [src, fft_r, ifft_r ]'", 2),
                        ("'EXISTS (fft_l MAPPED ARM06 OR fft_l MAPPED ARM05) AND (ARM00 PROCESSING)'", 3)])
def audio_filter_exynos_query(request):
    return request.param

@pytest.fixture(params=[("'EXISTS NOT fft_l MAPPED dsp2'", 0),
                        ("'EXISTS dsp3 PROCESSING'", 1),
                        ("'EXISTS RUNNING TOGETHER [fft_l, fft_r, filter_r ]'", 2),
                        ("'EXISTS (fft_l MAPPED dsp3 OR fft_l MAPPED dsp2) AND (dsp4 PROCESSING)'", 3)])
def audio_filter_multidsp_query(request):
    return request.param

@pytest.fixture(params=[("'EXISTS ifft_l MAPPED E02'", 0),
                        ("'EXISTS E07 PROCESSING'", 1),
                        ("'EXISTS NOT RUNNING TOGETHER [fft_l, src, sink ]'", 2),
                        ("'EXISTS (E08 PROCESSING) OR (E09 PROCESSING)'", 3)])
def audio_filter_parallella_query(request):
    return request.param

@pytest.fixture(params=[("'EXISTS DISTRIBUTOR MAPPED ARM05'", 0),
                        ("'EXISTS ARM07 PROCESSING'", 1),
                        ("'EXISTS RUNNING TOGETHER [DETECTION_WORKER_0, DETECTION_WORKER_1, DETECTION_WORKER_2 ]'", 2),
                        ("'EXISTS RUNNING TOGETHER [DETECTION_WORKER_1, DETECTION_WORKER_2 ] AND DETECTION_WORKER_5 \
                        MAPPED ARM07 AND ARM04 PROCESSING'", 3)])
def hog_query(request):
    return request.param

@pytest.fixture(params=[("'EXISTS NOT DCT_stage5 MAPPED ARM00'", 0),
                        ("'EXISTS ARM05 PROCESSING'", 1),
                        ("'EXISTS RUNNING TOGETHER [Worker_0, Worker_1, Worker_2 ]'", 2),
                        ("'EXISTS RUNNING TOGETHER [hamming_stage2, ShifterDLP, sink ] OR \
                        RUNNING TOGETHER [FFT_stage3, melFreqWrap_stage4 ]'", 3)])
def speaker_recognition_query(request):
    return request.param

@pytest.fixture
def csv_file_path():
    return "csv/test_values.csv"

