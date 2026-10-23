# Records a new PGO profile for choco-solver-capi from the test suite, then rebuilds the
# optimized library with it (see choco-solver-capi/pgo/README.md).
# Needs Oracle GraalVM 25 or later in $JAVA_HOME, on Linux or macOS.

set -e

# Instrumented library, and the extension built against it
(cd choco-solver-capi && sh build.sh instrument)
sh build.sh nocapibuild nowheel

rm -f choco-solver-capi/target/choco.iprof
python pgo/train.py tests
test -s choco-solver-capi/target/choco.iprof
gzip -9 -n -c choco-solver-capi/target/choco.iprof > choco-solver-capi/pgo/choco.iprof.gz

# Optimized library, guided by the new profile
sh build.sh nowheel
