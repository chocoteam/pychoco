# NOTE: before launching, ensure that $JAVA_HOME points
# to graalVM

# Parse command line arguments
for i in "$@"; do
  case $i in
    nocapibuild)
      NO_CAPI_BUILD=true
      shift
      ;;
    nowheel)
      NO_WHEEL=true
      shift
      ;;
    *)
      echo "Unknown option $i"
      exit 1
      ;;
  esac
done

# Build choco-solver-capi
if [ "$NO_CAPI_BUILD" != true ]; then
  cd choco-solver-capi
  git pull origin master
  sh ./build.sh
  cd ..
fi

# Clean previous build
rm -f -r build
rm -f pychoco/backend.py
rm -f pychoco/backend_wrap.c
rm -f pychoco/*.so

# Create C interface to python with SWIG
swig -python pychoco/backend.i

# Build extensions
#pip install .

python setup.py develop -e -b .
if [ "$NO_WHEEL" != true ]; then
  pip install wheel
  OS=`uname`
  if [ "$OS" = "Linux" ]; then
    python setup.py bdist_wheel --plat manylinux2014_x86_64
  else
    python setup.py bdist_wheel
  fi
fi
