from distutils.core import setup, Extension


lib_choco = Extension(
    'pychoco/_backend',
    ['pychoco/backend_wrap.c', 'pychoco/backend.c'],
    include_dirs=["choco-solver-capi", "pychoco"],
    library_dirs=["choco-solver-capi"],
    libraries=["choco_capi"],
    runtime_library_dirs=["choco-solver-capi"],
)

setup(
    name='pychoco',
    version='0.1',
    author="Dimitri Justeau-Allaire",
    description="""Python interface to Choco-solver""",
    ext_modules=[lib_choco],
    py_modules=["pychoco/backend"],
)
