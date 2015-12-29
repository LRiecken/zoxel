# Zoxel [![Build Status](https://travis-ci.org/chrmoritz/zoxel.svg?branch=master)](https://travis-ci.org/chrmoritz/zoxel) [![Build status](https://ci.appveyor.com/api/projects/status/twi20wjoblu78uec/branch/master?svg=true)](https://ci.appveyor.com/project/chrmoritz/zoxel/branch/master) [![Codacy Badge](https://api.codacy.com/project/badge/grade/7fb6eaf821a54587804afe792033531b)](https://www.codacy.com/app/chrmoritz/zoxel)

A cross-platform editor for small voxel models.
Copyright (c) 2013-2015, Graham R King, Christian Moritz, Eddie Pantridge, Bruno Canella, Lennart Riecken.
https://github.com/chrmoritz/zoxel

This is a fork of the original project hosted at https://github.com/grking/zoxel or http://zoxel.blogspot.co.uk/.

## Download

Prebuild binaries for Windows 32-bit and 64-bit (v0.5.15+) and OS X can be found together with a detailed changelog in the [Github Releases section](https://github.com/chrmoritz/zoxel/releases). You can always download the latest stable release from here: https://github.com/chrmoritz/zoxel/releases/latest

#### Nightlies

Nightly binaries for Windows from the latest unstable indevelopment version can be downloaded from the Appveyor build bot. Simply go to the latest [Appveyor Windows build](https://ci.appveyor.com/project/chrmoritz/zoxel/branch/master), choose the build matching your architecture (win32 or win64) and download the latest snapshot from the Artifacts tab.

Other platfroms have to build from source as descriped in the steps below:

## Building from source

### Prerequisites

* Python 2.7
* Qt 4 (if not included with PySide)
* these Python modules
  * PySide
  * PyOpenGL
  * PyOpenGL_accelerate (recommended)

#### Windows:

* Download and install Python 2.7 (Python 3 is not supported) from: https://www.python.org/downloads/
* install the required Python modules via pip: `pip install -U PySide PyOpenGL PyOpenGL_accelerate`
* optional (for creating Windows binaries): `pip install -U cx_freeze`

#### OS X:

* install Homebrew from brew.sh: http://brew.sh/
* recommended: install the latest python 2.7 version: `brew install python`
* install PySide and Qt from Homebrew: `brew install pyside pyside-tools`
* install the remaining Python modules via pip: `pip install -U PyOpenGL PyOpenGL_accelerate`
* optional (for creating a OS X .app): `pip install -U py2app`

### Building and running Zoxel

* Get the latest unstable indevelopment version from git or grab a source archive from the [Releases page](https://github.com/chrmoritz/zoxel/releases) and change your current working directory to the extracted sources
* To build and start Zoxel run: `python build.py -vs` (assuming a python executable from Python 2.7 is in your PATH)
  * for a list of additional available command line options run `python build.py -h`

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
