import platform
from constants import ZOXEL_TAG

if platform.system() == "Windows":
    from cx_Freeze import setup, Executable
    import os

    buildOptions = dict(packages=["plugins"], excludes=[], optimize=2,
                        includes=["atexit", "PySide.QtNetwork", "PySide.QtWebKit", "OpenGL", "OpenGL.platform.win32",
                                  "OpenGL.arrays.nones", "OpenGL.arrays.lists", "OpenGL.arrays.strings",
                                  "OpenGL.arrays.numbers", "OpenGL.arrays.ctypesarrays",
                                  "OpenGL.arrays.ctypesparameters", "OpenGL.arrays.ctypespointers"])
    idir = '[ProgramFiles64Folder]\Zoxel' if os.environ.get("PYTHON_ARCH") == "win64" else '[ProgramFilesFolder]\Zoxel'
    msiOptions = dict(upgrade_code="{2E7A6F78-3332-6269-7432-5A6F78656C06}", add_to_path=False, initial_target_dir=idir)
    executables = [Executable("zoxel.py", base="Win32GUI", icon="gfx\\icons\\icon.ico",
                              shortcutName="Zoxel", shortcutDir="ProgramMenuFolder")]
    version = ZOXEL_TAG
    if ZOXEL_TAG != os.environ.get("APPVEYOR_REPO_TAG_NAME"):
        version += "b" + (os.environ.get("APPVEYOR_BUILD_NUMBER") or "1")
    setup(
          name="Zoxel", version=version, url="https://github.com/chrmoritz/zoxel", license="GPL-3.0",
          description="a cross-platform editor for small voxel models",
          long_description="a cross-platform editor for small voxel models",
          options={"build_exe": buildOptions, "bdist_msi": msiOptions},
          executables=executables
    )

elif platform.system() == "Darwin":
    from setuptools import setup

    OPTIONS = {'argv_emulation': True, 'iconfile': 'gfx/icons/icon.icns', 'packages': 'plugins', 'optimize': 2}
    setup(
          name="Zoxel", version=ZOXEL_TAG,
          app=['zoxel.py'], data_files=[], setup_requires=['py2app'],
          options={'py2app': OPTIONS},
    )
