# NOTE: befaure launching ensure that $JAVA_HOME points
# to graalVM

# Build choco-solver-capi
cd choco-solver-capi
git pull origin master
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
#pip3 install .

python3 setup.py develop -e -b .
if [$1 != "nowheel"]; then
  pip install wheel
  OS=`uname`
  if [ "$OS" = "Linux" ]; then
      python setup.py bdist_wheel --plat manylinux2014_x86_64
  else
      python3 setup.py bdist_wheel
  fi
fi