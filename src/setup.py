import platform

if platform.system() == "Windows":
    from cx_Freeze import setup, Executable

    buildOptions = dict(packages=["plugins"], excludes=[], optimize=2,
                        includes=["atexit", "PySide.QtNetwork", "PySide.QtWebKit", "OpenGL", "OpenGL.platform.win32",
                                  "OpenGL.arrays.nones", "OpenGL.arrays.lists", "OpenGL.arrays.strings",
                                  "OpenGL.arrays.numbers", "OpenGL.arrays.ctypesarrays",
                                  "OpenGL.arrays.ctypesparameters", "OpenGL.arrays.ctypespointers"])
    executables = [Executable("zoxel.py", base="Win32GUI")]
    setup(options={"build_exe": buildOptions}, executables=executables)

elif platform.system() == "Darwin":

    from setuptools import setup

    APP = ['zoxel.py']
    DATA_FILES = []
    OPTIONS = {'argv_emulation': True, 'iconfile': 'gfx/icons/icon.icns', 'packages': 'plugins', 'optimize': 2}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
