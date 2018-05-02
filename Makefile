all: third_party_dependencies/pynauty-0.6/Makefile
	cd third_party_dependencies/pynauty-0.6/ && make pynauty && python -m tests.test_isomorphic && python -m tests.test_autgrp
