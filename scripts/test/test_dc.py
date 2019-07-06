from scripts.slx.dc import *
import sys


def test_dc_audio_filter_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_exynos.ini")
    sys.argv = argv
    main()

def test_dc_audio_filter_parallella():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_parallella.ini")
    sys.argv = argv
    main()

def test_dc_audio_filter_multidsp():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/audio_filter_multidsp.ini")
    sys.argv = argv
    main()

def test_dc_hog_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/hog_exynos.ini")
    sys.argv = argv
    main()

def test_dc_speaker_recognition_exynos():
    argv = [sys.argv[0]]
    argv.append("scripts/test/dc/speaker_recognition_exynos.ini")
    sys.argv = argv
    main()
