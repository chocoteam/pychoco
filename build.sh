# NOTE: befaure launching ensure that $JAVA_HOME points
# to graalVM

# Build choco-solver-capi
cd choco-solver-capi
sh ./build.sh
cd ..

# Clean previous build
rm -f -r build
rm -f pychoco/backend.py
rm -f pychoco/backend_wrap.c
rm -f pychoco/*.so

# Create C interface to python with SWIG
swig -python -py3 pychoco/backend.i

# Build extensions
sudo python3 setup.py develop
