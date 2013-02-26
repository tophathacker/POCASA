from distutils.core import setup, Extension

module1 = Extension('shift', sources = ['shiftModule.c'])

setup ( name = 'shiftModule',
        version = '1.0',
        description = 'This is for shifting out bits',
        ext_modules = [module1])
