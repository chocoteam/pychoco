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

# Pick the installer before cleaning anything: virtualenvs created by uv
# ship without pip, so fall back to uv when pip is missing
if python -m pip --version > /dev/null 2>&1; then
  PIP="python -m pip"
elif command -v uv > /dev/null 2>&1; then
  PIP="uv pip"
else
  echo "Neither pip nor uv is available"
  exit 1
fi

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
$PIP install -e .

if [ "$NO_WHEEL" != true ]; then
  $PIP install wheel build
  OS=$(uname)
  if [ "$OS" = "Linux" ]; then
    python -m build --wheel -C--plat-name=manylinux2014_x86_64
  else
    python -m build --wheel
  fi
fi
