from setuptools import setup, Extension
from Cython.Build import cythonize
import os
from Cython.Distutils import build_ext as cython_build_ext
import multiprocessing

num_cores = multiprocessing.cpu_count()
# This will find all .py files in the pyparsing package


# py_files = [
#     os.path.join("pyparsing", file)
#     for file in os.listdir("pyparsing")
#     if file.endswith(".py")
# ]
# py_files.append(os.path.join("pyparsing", "diagram", "__init__.py"))
# base_compiler_directives = {
#     "language_level": "3str",
#     "binding": True,
#     "overflowcheck": True,
#     "cdivision": True,
#     # "cpow": True,
#     "infer_types": True,
#     "embedsignature": True,
#     "c_api_binop_methods": True,
#     "profile": True,
# }

base_compiler_directives = {
    "language_level": 3,
    "overflowcheck": True,
    "cdivision": True,
    "cpow": True,
    "infer_types": True,
    "embedsignature": True,
    "c_api_binop_methods": True,
    "profile": True,
}


# only _optimized_cache.pyx

# py_files = [
#     "pyparsing/_optimized_cache.pyx",
# ]

# py_files = [
#     os.path.join("pyparsing", "_optimized_cache.pyx"),
# ]

# add CFLAGS:
# https://pythonspeed.com/articles/faster-cython-simd/

# https://llvm.org/docs/Vectorizers.html

# os.environ["CFLAGS"] = f"-Rpass-analysis=loop-vectorize"

# add link time optimization flag:
# os.environ["CFLAGS"] = "-flto=thin -fprofile-generate"
# Get the number of physical cores
# extensions = cythonize(
#     py_files, compiler_directives=base_compiler_directives, nthreads=8
# )


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


# ext_modules = [
#     Extension(
#         "pyparsing",
#         sources=py_files,
#         extra_compile_args=[
#             "-flto",
#             "-march=native",
#             "-fno-omit-frame-pointer",
#             "-std=c++20",
#         ],
#         extra_link_args=["-flto", "-std=c++20"],  # Create a static library
#         language="c++",
#     )
# ]

# module = cythonize(ext_modules, compiler_directives=base_compiler_directives,
#                    annotate=True, language_level=3, nthreads=num_cores, parallel=num_cores)

# module = cythonize(ext_modules, language_level=3, nthreads=num_cores, parallel=num_cores)

# module = cythonize(py_files, language_level=3)

# py_files = [
#     os.path.join("pyparsing", file)
#     for file in os.listdir("pyparsing")
#     if file.endswith(".pyx")
# ]

# py_files.extend([os.path.join("pyparsing", file) for file in os.listdir("pyparsing") if file.endswith(".py")])
# py_files.append(os.path.join("pyparsing", "diagram", "__init__.py"))

# base_compiler_directives = {
#     "language_level": 3,
#     "overflowcheck": True,
#     "cdivision": True,
#     "cpow": True,
#     "infer_types": True,
#     "embedsignature": True,
#     "c_api_binop_methods": True,
#     "profile": True,
# }

# extensions = [
#     Extension(
#         "pyparsing._optimized_cache",
#         ["pyparsing/_optimized_cache.pyx"]
#     )
# ]
# module = cythonize(extensions, language_level=3)
# extensions = cythonize(py_files, compiler_directives=base_compiler_directives)
# setup(
#     name="pyparsing",
#     version="3.1.4",
#     # ext_modules=extensions,
#     ext_modules=module,
#     # cmdclass={"build_ext": build_ext},
# )


# setup(
#     name="pyparsing",
#     version="3.1.4",
#     # ext_modules=cythonize(extensions),
#     ext_modules=extensions,
#     # packages=["pyparsing"],
#     # package_dir={"pyparsing": "pyparsing"},
#     # package_data={"pyparsing": ["*.pyx"]},
#     # other setup arguments
# )


# if __name__ == '__main__':
#     main()

extensions = [
    Extension("pyparsing._optimized_cache", ["pyparsing/_optimized_cache.pyx"])
]

setup(
    name="pyparsing",
    version="3.1.4",
    ext_modules=cythonize(
        extensions, compiler_directives=base_compiler_directives, language="c++"
    ),
    cmdclass={"build_ext": build_ext},
    # packages=["pyparsing"],
    # package_dir={"pyparsing": "pyparsing"},
    # package_data={"pyparsing": ["*.pyx"]},
    # other setup arguments
)
