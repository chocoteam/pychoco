# NOTE: before launching, ensure that $JAVA_HOME points
# to graalVM

set -e

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
  mvn clean package -Pnative
  cd ..
fi

# Clean previous build
rm -f -r build
rm -f pychoco/backend.py
rm -f pychoco/backend_wrap.c
rm -f pychoco/*.so

# Create C interface to python with SWIG
swig -python pychoco/backend.i

# Build and install in development mode
pip install -e .

if [ "$NO_WHEEL" != true ]; then
  pip install wheel build
  OS=$(uname)
  if [ "$OS" = "Linux" ]; then
    python -m build --wheel -C--plat-name=manylinux2014_x86_64
  else
    python -m build --wheel
  fi
fi
