from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'Sausage fider',
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize
)