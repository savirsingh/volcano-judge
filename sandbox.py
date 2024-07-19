# Based on https://github.com/code-demigod/Building-and-Breaking-a-Python-Sandbox/blob/master/Language%20Level%20Sandboxing%20using%20pysandbox.md

builtins_whitelist = set((
 # exceptions
 'ArithmeticError', 'AssertionError', 'AttributeError', 'BufferError', 'BytesWarning', 'DeprecationWarning', 'EOFError',
 'EnvironmentError', 'Exception', 'FloatingPointError','FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
 'ImportWarning', 'IndentationError', 'IndexError', 'KeyError','LookupError', 'MemoryError', 'NameError', 'NotImplemented',
 'NotImplementedError', 'OSError', 'OverflowError','PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'TabError', 'TypeError',
 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError','UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning',
 # constants
 'False', 'None', 'True', '__doc__', '__name__', '__package__', 'copyright', 'license', 'credits',
 # types
 'basestring', 'bytearray', 'bytes', 'complex', 'dict', 'float', 'frozenset', 'int', 'list', 'long', 'object', 'set', 'str',
 'tuple', 'unicode',
 # functions
 '__import__', 'abs', 'all', 'any', 'apply', 'bin', 'bool', 'buffer', 'callable', 'chr', 'classmethod', 'cmp', 'coerce',
 'compile', 'delattr', 'dir', 'divmod', 'enumerate', 'filter', 'format', 'hasattr', 'hash', 'hex', 'id',
 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print', 'property',
 'range', 'reduce', 'input', 'globals', 'repr', 'reversed', 'round', 'setattr', 'slice', 'sorted', 'staticmethod', 'sum', 'super', 'type', 'unichr', 'xrange', 'zip', 'getattr', 'len', 'sort'))

module_whitelist = set((
 # exceptions
 'itertools', 'sys', 'math'
 ))

def _safe_import(__import__, module_whitelist):
    def safe_import(module_name, globals={}, locals={}, fromlist=[], level=-1):
        if module_name in module_whitelist:
            return __import__(module_name, globals, locals, fromlist, level)
        else:
            raise ImportError("Blocked import of %s" % (module_name,))
    return safe_import

class ReadOnlyBuiltins(dict):
 def clear(self):
    ValueError("Read-only!")
    def __delitem__(self, key):
        ValueError("Read-only!")
    def pop(self, key, default=None):
        ValueError("Read-only!")
    def popitem(self):
        ValueError("Read-only!")
    def setdefault(self, key, value):
        ValueError("Read-only!")
    def __setitem__(self, key, value):
        ValueError("Read-only!")
    def update(self, dict, **kw):
        ValueError("Read-only!")
class Sandbox(object):
    def __init__(self):
        import sys
        from types import FunctionType
        from cpython import dictionary_of
        original_builtins = sys.modules["__main__"].__dict__["__builtins__"].__dict__
        for builtin in list(original_builtins):
            if builtin not in builtins_whitelist:
                del sys.modules["__main__"].__dict__["__builtins__"].__dict__[builtin]
        original_builtins["__import__"] = _safe_import(__import__, module_whitelist)
        safe_builtins = ReadOnlyBuiltins(original_builtins)
        sys.modules["__main__"].__dict__["__builtins__"] = safe_builtins
        type_dict = dictionary_of(type)
        del type_dict["__bases__"]
        del type_dict["__subclasses__"]
        function_dict = dictionary_of(FunctionType)
        def execute(self, code_string):
            exec(code_string)

