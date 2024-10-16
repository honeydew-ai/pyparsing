# distutils: language=c++


# # Import required components for working with Python objects
# from cpython.dict cimport PyDict_GetItem, PyDict_SetItem, PyDict_Clear

# cdef class _CacheType:
#     """Optimized version of dict for caching purposes."""

#     # Internal cache storage - same as Python dict
#     cdef dict cache

#     def __cinit__(self):
#         """Constructor for the class"""
#         self.cache = {}

#     def get(self, key, default=None):
#         """Optimized version of get"""
#         # Use PyDict_GetItem directly
#         cdef void* result = PyDict_GetItem(self.cache, key)
#         if result != NULL:  # C-level pointer comparison
#             return <object>result  # Cast to Python object
#         return default

#     def set(self, key, value):
#         """Optimized version of set"""
#         PyDict_SetItem(self.cache, key, value)

#     def clear(self):
#         """Optimized version of clear"""
#         # PyDict_Clear(self.cache)


from cpython.dict cimport PyDict_GetItem, PyDict_SetItem

cdef class _CacheType:
    """Optimized version of dict for caching purposes."""

    cdef dict cache

    def __cinit__(self):
        self.cache = {}

    def get(self, key, default=None):
        cdef void* result = PyDict_GetItem(self.cache, key)
        if result != NULL:
            return <object>result
        return default

    def set(self, key, value):
        PyDict_SetItem(self.cache, key, value)

    def clear(self):
        """Optimized version of clear by reinitializing the dictionary."""
        self.cache = {}  # Faster reset of the cache


# # Import required components for working with Python objects
# from cpython.dict cimport PyDict_GetItem, PyDict_SetItem, PyDict_Clear, PyDict_New
# from cpython.ref cimport Py_INCREF, Py_DECREF
# from cpython.object cimport PyObject

# cdef class _CacheType:
#     """Optimized version of dict for caching purposes."""

#     cdef dict cache  # The internal cache storage

#     def __cinit__(self):
#         """Constructor for the class."""
#         self.cache = PyDict_New()  # Initialize the dictionary with a new dict

#     def get(self, key, default=None):
#         """Optimized version of get."""
#         cdef PyObject* result = PyDict_GetItem(self.cache, key)
#         if result is not NULL:
#             Py_INCREF(result)  # Increase reference count
#             return <object>result  # Cast to Python object
#         return default

#     def set(self, key, value):
#         """Optimized version of set."""
#         PyDict_SetItem(self.cache, key, value)  # Set the item

#     def clear(self):
#         """Optimized version of clear using manual memory management."""
#         # Free the old cache before allocating a new one
#         cdef PyObject* old_cache = self.cache
#         self.cache = PyDict_New()  # Allocate a new dict
#         if old_cache is not NULL:
#             Py_DECREF(old_cache)  # Decrease reference count of the old dict

#     def __dealloc__(self):
#         """Destructor for the class."""
#         if self.cache is not NULL:
#             Py_DECREF(self.cache)  # Decrease reference count to free the dict