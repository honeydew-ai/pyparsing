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


# from cpython.dict cimport PyDict_GetItem, PyDict_SetItem

# cdef class _CacheType:
#     """Optimized version of dict for caching purposes."""

#     cdef dict cache
#     # cdef threadlocal dict cache

#     def __cinit__(self):
#         self.cache = {}

#     def get(self, key, default=None):
#         cdef void* result = PyDict_GetItem(self.cache, key)
#         if result != NULL:
#             return <object>result
#         return default

#     def set(self, key, value):
#         PyDict_SetItem(self.cache, key, value)

#     def clear(self):
#         """Optimized version of clear by reinitializing the dictionary."""
#         self.cache = {}  # Faster reset of the cache
#         # setting the cache to None is faster than setting it to {}


# # Import necessary C++ libraries
# from libcpp.unordered_map cimport unordered_map
# from libcpp.string cimport string

# # Import required Python C API utilities
# from cpython.ref cimport Py_INCREF, Py_DECREF
# from cpython.object cimport PyObject

# cdef class _CacheType:
#     """Optimized version of cache using std::unordered_map instead of Python dict."""

#     # Declare the C++ unordered_map for caching (key: string, value: PyObject*)
#     cdef unordered_map[string, PyObject*] cache

#     def __cinit__(self):
#         """Constructor for the class."""
#         pass  # The unordered_map is automatically initialized

#     def get(self, key: str, default=None):
#         """Optimized version of get using std::unordered_map."""
#         cdef unordered_map[string, PyObject*].iterator it = self.cache.find(key)
#         if it != self.cache.end():
#             Py_INCREF(it[1])  # Increase the reference count of the found object
#             return <object>it[1]  # Cast the PyObject* to a Python object
#         return default  # Return the default value if key is not found

#     def set(self, key: str, value):
#         """Optimized version of set using std::unordered_map."""
#         cdef PyObject* value_ptr = <PyObject*>value  # Cast Python object to PyObject*
#         Py_INCREF(value_ptr)  # Increase reference count for the new object

#         # Find the key in the unordered_map
#         cdef unordered_map[string, PyObject*].iterator it = self.cache.find(key)
#         if it != self.cache.end():
#             Py_DECREF(it[1])  # Decrease reference count of the old object

#         # Insert the new key-value pair or update the existing one
#         self.cache[key] = value_ptr

#     def clear(self):
#         """Optimized version of clear using unordered_map."""
#         # Decrease reference counts for all stored objects
#         cdef unordered_map[string, PyObject*].iterator it = self.cache.begin()
#         while it != self.cache.end():
#             Py_DECREF(it[1])  # Decrease reference count of each object
#             it = self.cache.erase(it)  # Erase the current element and move to the next

#     def __dealloc__(self):
#         """Destructor for the class."""
#         self.clear()  # Clear all objects, ensuring proper memory management



# Import threading module to use thread-local storage
import threading
from cpython.dict cimport PyDict_Clear

cdef class _CacheType:
    """Cache with thread-local storage for each thread."""

    # Declare a thread-local object
    cdef object local_storage

    def __cinit__(self):
        """Constructor for the class, initializes thread-local storage."""
        self.local_storage = threading.local()
        if not hasattr(self.local_storage, 'cache'):
            self.local_storage.cache = {}

    def get(self, key, default=None):
        """Retrieve value from the thread-local cache."""
        return self.local_storage.cache.get(key, default)

    def set(self, key, value):
        """Set a value in the thread-local cache."""
        self.local_storage.cache[key] = value

    def clear(self):
        """Clear the thread-local cache."""
        PyDict_Clear(self.local_storage.cache)