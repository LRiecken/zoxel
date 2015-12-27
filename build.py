#!/usr/bin/env python

import os
import platform
import shutil
from optparse import OptionParser


def main():
    parser = OptionParser(description="build tool for Zoxel")
    parser.add_option("-s", "--start", dest="start", action="store_true", help="start Zoxel after building it)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="print status messages to stdout")
    if platform.system() == "Windows":
        parser.add_option("-e", "--with-exe", action="store_true", dest="exe", help="generates a .exe")
        parser.add_option("-d", "--dist", dest="dist", default="dist", help="path of generated .exe (default to dist)")
    elif platform.system() == "Darwin":
        parser.add_option("-a", "--with-app", action="store_true", dest="app", help="generates an .app")
    (options, args) = parser.parse_args()

    src_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
    if platform.system() == "Windows":
        from distutils.sysconfig import get_python_lib
        site_packages_path = get_python_lib()
        pyside_rcc_path = os.path.join(site_packages_path, "PySide", "pyside-rcc.exe")
        cx_freeze_path = os.path.join(os.path.dirname(os.path.dirname(site_packages_path)), "Scripts", "cxfreeze")
        dist = os.path.expanduser(options.dist)
    else:
        pyside_rcc_path = "pyside-rcc"

    if options.verbose:
        print("Compiling PySide resources ...")
        os.system(pyside_rcc_path + " -o \"" + os.path.join(src_path, "resources_rc.py") + "\" \"" +
                  os.path.join(src_path, "resources.qrc") + "\"")

    if options.verbose:
        print("Generating PySide ui code ...")
    for r in os.listdir(src_path):
        if r.endswith(".ui"):
            ui = os.path.join(src_path, r)
            out = "ui_" + os.path.splitext(r)[0] + ".py"
            os.system("pyside-uic -o \"" + os.path.join(src_path, out) + "\" \"" + ui + "\"")
            if options.verbose:
                print("Generated " + out)

    if options.verbose:
        print("Completed building Zoxel!")

    if platform.system() == "Windows" and options.exe:
        if options.verbose:
            print("Generating Zoxel Windows binary to " + dist + " ...")

        if os.path.exists(dist):
            if options.verbose:
                print("Removing existing dist directory")
            shutil.rmtree(dist)

        if options.verbose:
            print("Launching cx_freeze ...")
        os.system("python " + cx_freeze_path + " \"" + os.path.join(src_path, "zoxel.py") + "\" --target-dir=\"" +
                  dist + ("\" --base-name=Win32GUI --include-modules atexit,PySide.QtNetwork,PySide.QtWebKit,OpenGL,"
                          "OpenGL.platform.win32,OpenGL.arrays.nones,OpenGL.arrays.lists,OpenGL.arrays.strings,"
                          "OpenGL.arrays.numbers,OpenGL.arrays.ctypesarrays,OpenGL.arrays.ctypesparameters,"
                          "OpenGL.arrays.ctypespointers --include-path \"") + src_path + "\"")

        if options.verbose:
            print("Zoxel Windows binary build completed!")

    if platform.system() == "Darwin" and options.app:
        dist = os.path.join(src_path, "dist")
        if options.verbose:
            print("Generating Zoxel OS X App to " + dist + "/zoxel.app ...")

        if os.path.exists(dist):
            if options.verbose:
                print("Removing existing dist directory")
            shutil.rmtree(dist)

        if options.verbose:
            print("Launching Py2App ...")
        os.chdir(src_path)
        os.system("python setup.py py2app")

        if os.environ.get('TRAVIS_TAG'):
            if options.verbose:
                print("Creating .tar.gz from App ...")

            os.chdir(dist)
            os.system("tar czf zoxel-" + os.environ['TRAVIS_TAG'] + "-osx.tar.gz zoxel.app")

        if options.verbose:
            print("Zoxel OS X App build completed!")

    if options.start:
        if options.verbose:
            print("starting Zoxel ...\n")

        os.chdir(src_path)
        os.system("python zoxel.py")


if __name__ == "__main__":
    main()
