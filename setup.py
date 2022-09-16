import os
import sys
from distutils.command.build import build

from setuptools import Extension, setup, find_packages, Command
from setuptools.command.build_ext import build_ext

extra_link_args = []
runtime_library_dirs = []

if sys.platform.startswith('win32'):
    so_ext = '.dll'
    capi_filename = 'choco_capi' + so_ext
if sys.platform.startswith('linux'):
    so_ext = '.so'
    capi_filename = 'libchoco_capi' + so_ext
    runtime_library_dirs = ['$ORIGIN']
elif sys.platform.startswith('darwin'):
    so_ext = '.dylib'
    capi_filename = 'libchoco_capi' + so_ext
    extra_link_args = ['-Wl,-rpath,@loader_path']


class CopySharedLibrary(Command):
    user_options = []

    def initialize_options(self):
        self.build_lib = None
        self.inplace = 0
        self.build_dir = "choco-solver-capi/target"
        self.filename = capi_filename
        self.lib_source_path = os.path.join(self.build_dir, self.filename)
        self.package_name = 'pychoco'

    def finalize_options(self):
        self.set_undefined_options('build', ('build_lib', 'build_lib'), )
        self.set_undefined_options('build_ext', ('inplace', 'inplace'), )

    def run(self) -> None:
        self.inplace = self.get_finalized_command('build_ext').inplace
        if self.inplace:
            lib_target_path = self.package_name
        else:
            lib_target_path = os.path.join(self.build_lib, self.package_name)
            self.mkpath(lib_target_path)
        self.copy_file(self.lib_source_path, os.path.join(lib_target_path, self.filename))
        if sys.platform.startswith('win32'):
            self.copy_file(self.lib_source_path, os.path.join(lib_target_path, "lib{}".format(self.filename)))
        os.environ["ORIGIN"] = os.path.abspath(lib_target_path)


class CustomBuild(build):
    sub_commands = [
        ('build_clib', build.has_c_libraries),
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_scripts', build.has_scripts),
    ]


class CustomBuildExt(build_ext):

    def run(self):
        self.run_command('copy_chocolib')
        super().run()


lib_choco = Extension(
    'pychoco._backend', ['pychoco/backend.i', 'pychoco/backend.c'],
    include_dirs=["pychoco/", "choco-solver-capi/target"],
    library_dirs=["pychoco/", "choco-solver-capi/target"],
    libraries=["choco_capi"],
    runtime_library_dirs=runtime_library_dirs,
    extra_link_args=extra_link_args
)

setup(
    name='pychoco',
    cmdclass={
        'copy_chocolib': CopySharedLibrary,
        'build_ext': CustomBuildExt,
        'build': CustomBuild,
    },
    version='0.1',
    author="Dimitri Justeau-Allaire",
    description="""Python bindings to the Choco Constraint Programming solver""",
    license="BSD-4",
    author_email="dimitri.justeau@gmail.com",
    packages=find_packages(),
    ext_modules=[lib_choco],
)
