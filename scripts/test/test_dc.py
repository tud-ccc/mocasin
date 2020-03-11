# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

from scripts.slx.dc import *
import sys
import hydra


@hydra.main(config_path='../conf/.dc_af_exy.yaml')
def test_dc_audio_filter_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_exynos.ini")
    sys.argv = argv
    main()

@hydra.main(config_path='../conf/.dc_af_parallella.yaml')
def test_dc_audio_filter_parallella():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_parallella.ini")
    sys.argv = argv
    main()

@hydra.main(config_path='../conf/.dc_af_multidsp.yaml')
def test_dc_audio_filter_multidsp():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_multidsp.ini")
    sys.argv = argv
    main()

@hydra.main(config_path='../conf/.dc_hog_exy.yaml')
def test_dc_hog_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/hog_exynos.ini")
    sys.argv = argv
    main()

@hydra.main(config_path='../conf/.dc_sr_exy.yaml')
def test_dc_speaker_recognition_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/speaker_recognition_exynos.ini")
    sys.argv = argv
    main()
