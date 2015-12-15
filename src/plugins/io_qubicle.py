# io_qubicle.py
# Qubicle Constructor Binary File IO
# Copyright (c) 2014, Graham R King
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
from plugin_api import register_plugin
from PySide.QtGui import QMessageBox
from struct import unpack

# http://www.minddesk.com/wiki/index.php?title=Qubicle_Constructor_1:Data_Exchange_With_Qubicle_Binary


class QubicleFile(object):

    # Description of file type
    description = "Qubicle Files"

    # File type filter
    filetype = "*.qb"

    def __init__(self, api):
        self.api = api
        # Register our exporter
        self.api.register_file_handler(self)

    # Helper function to read/write uint32
    def uint32(self, f, value=None):
        if value is not None:
            # Write
            data = bytearray()
            data.append((value & 0xff))
            data.append((value & 0xff00) >> 8)
            data.append((value & 0xff0000) >> 16)
            data.append((value & 0xff000000) >> 24)
            f.write(data)
        else:
            # Read
            x = bytearray(f.read(4))
            if len(x) == 4:
                return x[0] | x[1] << 8 | x[2] << 16 | x[3] << 24
            return 0

    def int32(self, f):
        return unpack('i', f.read(4))[0]

    # Called when we need to save. Should raise an exception if there is a
    # problem saving.
    def save(self, filename):
        # grab the voxel data
        voxels = self.api.get_voxel_data()

        # Open our file
        f = open(filename, "wb")

        # Version
        self.uint32(f, 0x00000101)
        # Color format RGBA
        self.uint32(f, 0)
        # Left handed coords
        self.uint32(f, 0)
        # Uncompressed
        self.uint32(f, 0)
        # Visability mask
        self.uint32(f, 0)
        # Matrix count
        self.uint32(f, 1)

        # Model name length
        name = "Model"
        f.write(str(chr(len(name))))
        # Model name
        f.write(name)

        # X, Y, Z dimensions
        self.uint32(f, voxels.width)
        self.uint32(f, voxels.height)
        self.uint32(f, voxels.depth)

        # Matrix position
        self.uint32(f, 0)
        self.uint32(f, 0)
        self.uint32(f, 0)

        # Data
        for z in xrange(voxels.depth):
            for y in xrange(voxels.height):
                for x in xrange(voxels.width - 1, -1, -1):
                    vox = voxels.get(x, y, z)
                    alpha = 0xff
                    if not vox:
                        alpha = 0x00
                    r = (vox & 0xff000000) >> 24
                    g = (vox & 0xff0000) >> 16
                    b = (vox & 0xff00) >> 8
                    vox = r | g << 8 | b << 16 | alpha << 24
                    self.uint32(f, vox)

        # Tidy up
        f.close()

    # sets alpha to ff and converts brga to rgba if format
    def formatVox(self, vox, format):
        r = (vox & 0x000000ff) >> 0
        g = (vox & 0x0000ff00) >> 8
        b = (vox & 0x00ff0000) >> 16
        if format:
            return (b << 24) | (g << 16) | (r << 8) | 0xff
        return (r << 24) | (g << 16) | (b << 8) | 0xff

    # Load a Qubicle Constructor binary file
    def load(self, filename):
        # grab the voxel data
        voxels = self.api.get_voxel_data()

        # Open our file
        f = open(filename, "rb")

        # Version
        version = self.uint32(f)
        # Color format 0 for RGBA and 1 for BRGA
        format = self.uint32(f)
        # Left handed coords
        coords = self.uint32(f)
        # Uncompressed
        compression = self.uint32(f)
        # Visability mask
        mask = self.uint32(f)
        # Matrix count
        matrix_count = self.uint32(f)

        # Warn about multiple matrices
        if matrix_count > 1:
            self.api.warning("Qubicle files with more than 1 matrix"
                             " are not yet properly supported. All "
                             " matrices will be (badly) merged.")

        max_width = 0
        max_height = 0
        max_depth = 0

        for i in xrange(matrix_count):

            # Name length
            namelen = int(ord(f.read(1)))
            name = f.read(namelen)

            # X, Y, Z dimensions
            width = self.uint32(f)
            height = self.uint32(f)
            depth = self.uint32(f)

            # Don't allow huge models
            if width > 127 or height > 127 or depth > 127:
                raise Exception("Model to large - max 127x127x127")

            if width > max_width:
                max_width = width
            if height > max_height:
                max_height = height
            if depth > max_depth:
                max_depth = depth

            voxels.resize(max_width, max_height, max_depth)

            # Matrix position - FIXME not yet supported
            dx = self.int32(f)
            dy = self.int32(f)
            dz = self.int32(f)

            # Data
            if compression:
                for z in xrange(depth):
                    index = 0
                    while True:
                        data = self.uint32(f)
                        if data == 6:
                            break
                        elif data == 2:
                            count = self.uint32(f)
                            vox = self.uint32(f)
                            if (vox & 0xff000000) >> 24:
                                vox = self.formatVox(vox, format)
                                for j in xrange(count):
                                    x = index % width
                                    y = index / width
                                    index += 1
                                    iz = z
                                    if coords == 1:
                                        iz = depth - z - 1
                                    voxels.set((width - x - 1), y, iz, vox)
                            else:
                                index += count
                        else:
                            x = index % width
                            y = index / width
                            index += 1
                            if (data & 0xff000000) >> 24:
                                iz = z
                                if coords == 1:
                                    iz = depth - z - 1
                                voxels.set((width - x - 1), y, iz, self.formatVox(data, format))
            else:
                for z in xrange(depth):
                    for y in xrange(height):
                        for x in xrange(width):
                            vox = self.uint32(f)
                            if (vox & 0xff000000) >> 24:
                                iz = z
                                if coords == 1:
                                    iz = depth - z - 1
                                voxels.set((width - x - 1), y, iz, self.formatVox(vox, format))
            # restore attachment point
            if matrix_count == 1 and dx <= 0 and dy <= 0 and dz <= 0 and (dx < 0 or dy < 0 or dz < 0):
                t = "It looks like your are opening a voxel model exported by Trove.\
                     Should we try to restore the attachment point out of the .qb's metadata for you?"
                r = QMessageBox.question(None, "Restore attachment point?", t, QMessageBox.No, QMessageBox.Yes)
                if r == QMessageBox.Yes:
                    voxels.set((max_width + dx - 1), -dy, -dz, 0xff00ffff)

        f.close()


register_plugin(QubicleFile, "Qubicle Constructor file format IO", "1.0")
