#!/usr/bin/env python

import os
import platform
import shutil
from optparse import OptionParser


def main():
    class MyParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog
    parser = MyParser(epilog="""\nExamples:\nbuild and run:\t./build.py -vs\n""")
    parser.add_option("-s", "--start", dest="start", action="store_true", help="start Zoxel after building it)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="print status messages to stdout")
    if platform.system() == "Windows":
        parser.add_option("-e", "--with-exe", action="store_true", dest="exe", help="generates a .exe (Windows only)")
        parser.add_option("-d", "--dist", dest="dist", default="dist", help="path of generated .exe (default to dist)")
        parser.add_option("-m", "--with-msi", action="store_true", dest="msi", help="generates a .msi (Windows only)")
    elif platform.system() == "Darwin":
        parser.add_option("-a", "--with-app", action="store_true", dest="app", help="generates an .app (OS X only)")
        parser.add_option("-i", "--with-dmg", action="store_true", dest="dmg", help="generates an .dmg (OS X only)")
    (options, args) = parser.parse_args()

    build_path = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(build_path, "src")
    if platform.system() == "Windows":
        from distutils.sysconfig import get_python_lib
        pyside_rcc_path = os.path.join(get_python_lib(), "PySide", "pyside-rcc.exe")
        dist = os.path.abspath(os.path.expanduser(options.dist))
    else:
        pyside_rcc_path = "pyside-rcc"
        dist = os.path.join(src_path, "dist")
        build = os.path.join(src_path, "build")

    if options.verbose:
        print "Compiling PySide resources ..."
        os.system(pyside_rcc_path + " -o \"" + os.path.join(src_path, "resources_rc.py") + "\" \"" +
                  os.path.join(src_path, "resources.qrc") + "\"")

    if options.verbose:
        print "Generating PySide ui code ..."
    for r in os.listdir(src_path):
        if r.endswith(".ui"):
            ui = os.path.join(src_path, r)
            out = "ui_" + os.path.splitext(r)[0] + ".py"
            os.system("pyside-uic -o \"" + os.path.join(src_path, out) + "\" \"" + ui + "\"")
            if options.verbose:
                print "Generated " + out

    if options.verbose:
        print "Completed building Zoxel!"

    if platform.system() == "Windows" and options.exe:
        if options.verbose:
            print "Generating Zoxel Windows binary to " + dist + " ..."

        if os.path.exists(dist):
            if options.verbose:
                print "Removing existing dist directory"
            shutil.rmtree(dist)

        if options.verbose:
            print "Launching cx_freeze ..."
        os.chdir(src_path)
        os.system("python setup.py build_exe -b \"" + dist + "\"")

        if os.environ.get("APPVEYOR_REPO_TAG_NAME"):
            if options.verbose:
                print "Zipping Windows binary ..."

            os.chdir(build_path)
            os.system("7z a zoxel-" + os.environ["APPVEYOR_REPO_TAG_NAME"] + "-" + os.environ["PYTHON_ARCH"] +
                      ".zip -r \"" + dist + "\*\"")

        if options.verbose:
            print "Zoxel Windows binary build completed!"

    if platform.system() == "Windows" and options.msi:
        if options.verbose:
            print "Generating Zoxel Windows MSI installer to " + src_path + "\\dist\\ ..."

        build_path = os.path.join(src_path, "build")
        if os.path.exists(build_path):
            if options.verbose:
                print "Removing existing build directory"
            shutil.rmtree(build_path)

        dist_path = os.path.join(src_path, "dist")
        if os.path.exists(dist_path):
            if options.verbose:
                print "Removing existing dist directory"
            shutil.rmtree(dist_path)

        if options.verbose:
            print "Launching cx_freeze ..."
        os.chdir(src_path)
        os.system("python setup.py bdist_msi")

        if options.verbose:
            print "Zoxel Windows MSI installer build completed!"

    if platform.system() == "Darwin" and options.app:
        if options.verbose:
            print "Generating Zoxel OS X App to " + dist + "/zoxel.app ..."

        if os.path.exists(dist):
            if options.verbose:
                print "Removing existing dist directory"
            shutil.rmtree(dist)

        if os.path.exists(build):
            if options.verbose:
                print "Removing existing build directory"
            shutil.rmtree(build)

        if options.verbose:
            print "Launching Py2App ..."
        os.chdir(src_path)
        os.system("python setup.py py2app")

        if os.environ.get('TRAVIS_TAG'):
            if options.verbose:
                print "Creating .tar.gz from App ..."

            os.chdir(dist)
            os.system("tar czf zoxel-" + os.environ["TRAVIS_TAG"] + "-osx.tar.gz Zoxel.app")

        if options.verbose:
            print "Zoxel OS X App build completed!"

        if options.dmg:
            if options.verbose:
                print "Generating Zoxel OS X dmg installer to " + dist + "/ ..."

            os.chdir(src_path)
            os.system("dmgbuild -s dmgConfig.py Zoxel \"" + dist + "/Zoxel-osx.dmg\"")

    if options.start:
        if options.verbose:
            print "starting Zoxel ...\n"

        os.chdir(src_path)
        if options.verbose:
            os.system("python zoxel.py")
        elif platform.system() == "Windows":
            os.system("start /B python zoxel.py > NUL")
        else:
            os.system("python zoxel.py > /dev/null 2>&1 &")


if __name__ == "__main__":
    main()
