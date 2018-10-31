# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.10
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.


from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module(
                '_lpRgpu', [dirname(__file__)])
        except ImportError:
            import _lpRgpu
            return _lpRgpu
        if fp is not None:
            try:
                _mod = imp.load_module('_lpRgpu', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _lpRgpu = swig_import_helper()
    del swig_import_helper
else:
    import _lpRgpu
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError(name)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0


class lpRgpu(_object):
    __swig_setmethods__ = {}

    def __setattr__(self, name, value): return _swig_setattr(
        self, lpRgpu, name, value)
    __swig_getmethods__ = {}

    def __getattr__(self, name): return _swig_getattr(self, lpRgpu, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _lpRgpu.new_lpRgpu(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _lpRgpu.delete_lpRgpu

    def __del__(self): return None

    def printGlobalParameters(
        self): return _lpRgpu.lpRgpu_printGlobalParameters(self)

    def printFwdParameters(
        self): return _lpRgpu.lpRgpu_printFwdParameters(self)

    def printAdjParameters(
        self): return _lpRgpu.lpRgpu_printAdjParameters(self)

    def readGlobalParametersArr(
        self, *args): return _lpRgpu.lpRgpu_readGlobalParametersArr(self, *args)

    def readFwdParametersArr(
        self, *args): return _lpRgpu.lpRgpu_readFwdParametersArr(self, *args)

    def readAdjParametersArr(
        self, *args): return _lpRgpu.lpRgpu_readAdjParametersArr(self, *args)

    def printCurrentGPUMemory(
        self, str=None): return _lpRgpu.lpRgpu_printCurrentGPUMemory(self, str)

    def initFwd(self, *args): return _lpRgpu.lpRgpu_initFwd(self, *args)

    def initAdj(self, *args): return _lpRgpu.lpRgpu_initAdj(self, *args)

    def deleteFwd(self): return _lpRgpu.lpRgpu_deleteFwd(self)

    def deleteAdj(self): return _lpRgpu.lpRgpu_deleteAdj(self)

    def prefilter2D(
        self, *args): return _lpRgpu.lpRgpu_prefilter2D(self, *args)

    def execFwd(self): return _lpRgpu.lpRgpu_execFwd(self)

    def execAdj(self): return _lpRgpu.lpRgpu_execAdj(self)

    def execFwdMany(
        self, *args): return _lpRgpu.lpRgpu_execFwdMany(self, *args)

    def execAdjMany(
        self, *args): return _lpRgpu.lpRgpu_execAdjMany(self, *args)

    def execFwdManyPtr(
        self, *args): return _lpRgpu.lpRgpu_execFwdManyPtr(self, *args)

    def execAdjManyPtr(
        self, *args): return _lpRgpu.lpRgpu_execAdjManyPtr(self, *args)

    def applyFilter(self): return _lpRgpu.lpRgpu_applyFilter(self)

    def padding(self, *args): return _lpRgpu.lpRgpu_padding(self, *args)


lpRgpu_swigregister = _lpRgpu.lpRgpu_swigregister
lpRgpu_swigregister(lpRgpu)

# This file is compatible with both classic and new-style classes.
