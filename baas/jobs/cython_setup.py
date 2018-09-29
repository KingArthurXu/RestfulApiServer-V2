from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [Extension("events", ["events.py"]),
               Extension("jobs", ["jobs.py"]),
               ]
setup(
    name="baas cpy",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
# python setup.py build_ext --inplace