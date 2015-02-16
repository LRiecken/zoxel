from setuptools import setup

APP = ['zoxel.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True, 'iconfile': 'gfx/icons/icon.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
