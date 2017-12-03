from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.

buildOptions = dict(
    packages=['saving_crying_bryan', 'numpy', 'psycopg2', 'sqlalchemy'],
    excludes=[],
    include_files=['saving_crying_bryan/resources']
)

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('saving_crying_bryan.py', base=base)
]

setup(
    name='Saving Crying Bryan',
    version='1.0',
    description='Saving Crying Bryan',
    options=dict(build_exe=buildOptions),
    executables=executables
)
