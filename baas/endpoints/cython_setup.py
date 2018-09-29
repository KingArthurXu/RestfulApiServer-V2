from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [Extension("auth", ["auth.py"]),
               Extension("bpdbjobs", ["bpdbjobs.py"]),
               Extension("nbuapi", ["nbuapi.py"]),
               Extension("decorators", ["decorators.py"]),
               ]
setup(
    name="baas cpy",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
# python setup.py build_ext --inplace