#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
# 编译模块使用
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("auth", ["auth.py"]),
    Extension("bpdbjobs", ["bpdbjobs.py"]),
    Extension("bpimagelist", ["bpimagelist.py"]),
    Extension("decorators", ["decorators.py"]),
    Extension("nbuapi", ["nbuapi.py"]),
    Extension("popen", ["popen.py"]),
    Extension("ssh_exec", ["ssh_exec.py"]),
]
setup(
    name="baas cpy",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
# python setup.py build_ext --inplace