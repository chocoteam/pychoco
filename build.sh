# Clean previous build
rm -r build
rm pychoco/backend.py
rm pychoco/backend_wrap.c
rm pychoco/*.so

# Create C interface to python with SWIG
swig -python -py3 pychoco/backend.i

# Build extensions
python3 setup.py develop
