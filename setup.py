import os
from os.path import join as pjoin
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from distutils.extension import Extension
from distutils.command.build_ext import build_ext
import subprocess
import numpy

def find_in_path(name, path):
    "Find a file in a search path"
    #adapted fom http://code.activestate.com/recipes/52224-find-a-file-given-a-search-path/
    for dir in path.split(os.pathsep):
        binpath = pjoin(dir, name)
        if os.path.exists(binpath):
            return os.path.abspath(binpath)
    return None


def locate_cuda():
    """Locate the CUDA environment on the system

    Returns a dict with keys 'home', 'nvcc', 'include', and 'lib'
    and values giving the absolute path to each directory.

    Starts by looking for the CUDAHOME env variable. If not found, everything
    is based on finding 'nvcc' in the PATH.
    """

    # first check if the CUDAHOME env variable is in use
    if 'CUDAHOME' in os.environ:
        home = os.environ['CUDAHOME']
        nvcc = pjoin(home, 'bin', 'nvcc')
        libdir = pjoin(home, 'lib64')
    else:
        # otherwise, search the PATH for NVCC
        nvcc = find_in_path('nvcc', os.environ['PATH'])
        if nvcc is None:
            raise EnvironmentError('The nvcc binary could not be '
                'located in your $PATH. Either add it to your path, or set $CUDAHOME')
        home = os.path.dirname(os.path.dirname(nvcc))
        print(home)
        #proc = subprocess.Popen("dirname $(ldconfig -p | grep libcudart.so | awk '{print $4}' | head -n 1)", shell=True, stdout=subprocess.PIPE)
        #out, err = proc.communicate()
        #libdir = out.decode('ascii').rstrip()

    cudaconfig = {'home':home, 'nvcc':nvcc,
                  'include': pjoin(home, 'include'),
                  'lib': pjoin(home,'lib64')}
    for k, v in cudaconfig.items():
        if not os.path.exists(v):
            raise EnvironmentError('The CUDA %s path could not be located in %s' % (k, v))

    return cudaconfig

CUDA = locate_cuda()

# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()


ext = Extension(
    'lprec._lpRgpu',
    swig_opts=['-c++', '-outdir', 'lprec', '-Isrc'],
    sources=[
        'src/callerr.cu',
        'src/gridStorage.cu',
        'src/lpRgpu.cu',
        'src/lpRgpu.i',
        'src/params.cu',
    ],
    library_dirs=[CUDA['lib']],
    libraries=['cudart', 'cufft'],
    runtime_library_dirs=[CUDA['lib']],
    # this syntax is specific to this build system
    # we're only going to use certain compiler args with nvcc and not with gcc
    # the implementation of this trick is in customize_compiler() below
    extra_compile_args={'gcc': [],
                        'nvcc': ['--compiler-options', "'-fPIC'"]},
    include_dirs=[numpy_include, CUDA['include'], 'src'],)


def customize_compiler_for_nvcc(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.

    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""

    # tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    super = self._compile

    # now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[1] == '.cu':
            # use the cuda for .cu files
            self.set_executable('compiler_so', CUDA['nvcc'])
            # use only a subset of the extra_postargs, which are 1-1 translated
            # from the extra_compile_args in the Extension class
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']

        super(obj, src, ext, cc_args, postargs, pp_opts)
        # reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    # inject our redefined _compile method into the class
    self._compile = _compile


class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)


class build_py(_build_py):
    """Do build_ext first so SWIG python module is copied after creation."""
    def run(self):
        self.run_command("build_ext")
        return super().run()


setup(
    name='lprec',
    author='Viktor Nikitin',
    version='1.0.0',
    packages=['lprec'],
    ext_modules=[ext],
    # inject our custom trigger
    cmdclass={
        'build_py': build_py,
        'build_ext': custom_build_ext,
    },
    # since the package has c code, the egg cannot be zipped
    zip_safe=False
)
