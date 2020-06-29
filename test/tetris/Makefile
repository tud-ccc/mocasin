# Prepare the configuration files and run lit-testing.
# Two targets supported: generate (default) and test.

pykpn_root := $(abspath $(dir $(firstword $(MAKEFILE_LIST)))/../..)
yaml_out := ./conf/tetris.yaml ./conf/platform/exynos.yaml

.PHONY: generate test clean

generate: $(yaml_out)
	@ echo "Generated $(yaml_out)"

test: generate
	@ lit -v .

clean:
	@ echo "Cleaning"
	@ -rm -f $(yaml_out)
	@ find . -name outputs -type d -print0 | xargs -0 rm -rf
	@ find . -name Output -type d -print0 | xargs -0 rm -rf

$(yaml_out): %: %.in Makefile
	@ sed -e "s:PYKPN_ROOT:$(pykpn_root):g"  $< > $@
