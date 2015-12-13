# io_png.py
# Zoxel png importer
# Copyright (c) 2015, Lennart Riecken
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
from plugin_api import register_plugin
from PySide import QtGui

class PngFile(object):

    # Description of file type
    description = "PNG Files"

    # File type filter
    filetype = "*.png"

    def __init__(self, api):
        self.api = api
        # Register our exporter
        self.api.register_file_handler(self)
        # File version format we support
        self._file_version = 1


    # Called when we need to load a file. Should raise an exception if there
    # is a problem.
    def load(self, filename):

        # load the png
        try:
            png = QtGui.QPixmap(filename)
        except Exception as Ex:
            raise Exception("This is not a valid png file: %s" % Ex)

        width = png.width()
        height = png.height()
        if width > 127 or height > 127:
            raise Exception("The image file is too large. Maximum width and height are 127 pixels.")
        depth = 1
        img = png.toImage()

        # grab the voxel data
        voxels = self.api.get_voxel_data()

        voxels.resize(width, height, depth)

        for x in range(width):
            for y in range(height):
                color = img.pixel(x,y)
                color = color << 8
                voxels.set(x,height-y-1,0, color)



register_plugin(PngFile, "Png file format Importer", "1.0")
