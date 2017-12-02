from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.

buildOptions = dict(
    packages=['ld40_setup', 'numpy'],
    excludes=[],
    include_files=[('ld40_setup/resources', 'ld40_setup/resources')]
)

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('sample.py', base=base)
]

setup(
    name='Sample',
    version='1.0',
    description='Sample',
    options=dict(build_exe=buildOptions),
    executables=executables
)
