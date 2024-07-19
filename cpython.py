# Based on https://github.com/code-demigod/Building-and-Breaking-a-Python-Sandbox/blob/master/Language%20Level%20Sandboxing%20using%20pysandbox.md

from ctypes import pythonapi, POINTER, py_object
_get_dict = pythonapi._PyObject_GetDictPtr
_get_dict.restype = POINTER(py_object)
_get_dict.argtypes = [py_object]
del pythonapi, POINTER, py_object
def dictionary_of(ob):
    dptr = _get_dict(ob)
    return dptr.contents.value
