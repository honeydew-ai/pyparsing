from setuptools import setup, Extension
from Cython.Build import cythonize
import os
from Cython.Distutils import build_ext as cython_build_ext
import multiprocessing

# This will find all .py files in the pyparsing package
py_files = [
    os.path.join("pyparsing", file)
    for file in os.listdir("pyparsing")
    if file.endswith(".py")
]
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

# os.environ["CFLAGS"] = f"-Rpass-analysis=loop-vectorize"

# add link time optimization flag:
os.environ["CFLAGS"] = "-flto=thin -fprofile-generate"
# Get the number of physical cores
num_cores = multiprocessing.cpu_count()
extensions = cythonize(
    py_files, compiler_directives=base_compiler_directives, nthreads=8
)


# Custom build_ext command to include -j option
class build_ext(cython_build_ext):
    def initialize_options(self):
        super().initialize_options()
        self.parallel = num_cores


# class build_ext(cython_build_ext):
#     # def initialize_options(self):
#     #     super().initialize_options()
#     #     self.parallel = num_cores
#     def build_extension(self, ext):
#         # Compile the extension as usual
#         super().build_extension(ext)

#         # Get the object files
#         objects = self.compiler.object_filenames(ext.sources, output_dir=self.build_temp)

#         # Create the static library
#         # Create the static library
#         static_lib_path = os.path.join(self.build_lib, f"lib{ext.name}.a")
#         self.compiler.create_static_lib(objects, ext.name, output_dir=self.build_lib)

#         # Remove the shared library
#         shared_lib_path = self.get_ext_fullpath(ext.name)
#         if os.path.exists(shared_lib_path):
#             os.remove(shared_lib_path)

#         # Move the static library to the final destination
#         final_static_lib_path = self.get_ext_fullpath(ext.name).replace('.so', '.a')
#         if os.path.exists(static_lib_path):
#             os.rename(static_lib_path, final_static_lib_path)


ext_modules = [
    Extension(
        "pyparsing",
        sources=py_files,
        extra_compile_args=["-flto", "-march=native", "-fno-omit-frame-pointer"],
        extra_link_args=["-flto"],  # Create a static library
    )
]


setup(
    name="pyparsing",
    version="3.1.4",
    # ext_modules=extensions,
    ext_modules=cythonize(ext_modules, compiler_directives=base_compiler_directives),
    cmdclass={"build_ext": build_ext},
)
