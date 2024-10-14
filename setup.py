from setuptools import setup, Extension
from Cython.Build import cythonize
import os
from Cython.Distutils import build_ext as cython_build_ext
import multiprocessing

# This will find all .py files in the pyparsing package
py_files = [os.path.join("pyparsing", file) for file in os.listdir("pyparsing") if file.endswith(".py")]
py_files.append(os.path.join("pyparsing", "diagram", "__init__.py"))
base_compiler_directives = {
    "language_level": 3,
    "overflowcheck": True,
    "cdivision": True,
    # "cpow": True,
    "infer_types": True,
    "embedsignature": True,
    "c_api_binop_methods": True,
    "profile": True,
}

# add CFLAGS:
# https://pythonspeed.com/articles/faster-cython-simd/

# https://llvm.org/docs/Vectorizers.html

os.environ["CFLAGS"] = f"-Rpass-analysis=loop-vectorize"

# Get the number of physical cores
num_cores = multiprocessing.cpu_count()
extensions = cythonize(py_files, compiler_directives=base_compiler_directives, nthreads=8)

# Custom build_ext command to include -j option
class build_ext(cython_build_ext):
    def initialize_options(self):
        super().initialize_options()
        self.parallel = num_cores



ext_modules = [
    Extension(
        "pyparsing",
        sources=py_files,
        # extra_compile_args=["-pgo"],
        extra_link_args=["-static"],  # Create a static library
    )
]


setup(
    name="pyparsing",
    version="3.1.4",
    # ext_modules=extensions,
    ext_modules=cythonize(ext_modules, compiler_directives=base_compiler_directives),
    cmdclass={'build_ext': build_ext},    
)
