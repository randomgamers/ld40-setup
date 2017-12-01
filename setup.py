from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=['ld40_setup', 'ld40_setup.resources', 'ld40_setup.resources.images', 'ld40_setup.resources.sounds'],
                    excludes = [],
                    include_files=[('ld40_setup/resources', 'ld40-setup/resources')]
                    )

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('sample.py', base=base)
]

setup(name='',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
