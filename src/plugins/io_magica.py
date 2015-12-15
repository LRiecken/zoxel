# io_magica.py
# MagicaVoxel (.vox) Binary File IO
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

# http://voxel.codeplex.com/wikipage?title=VOX%20Format&referringTitle=MagicaVoxel%20Editor


class MagicaFile(object):

    # Description of file type
    description = "MagicaVoxel Files"

    # File type filter
    filetype = "*.vox"

    def __init__(self, api):
        self.api = api
        # Register our exporter
        self.api.register_file_handler(self)
        self.default_palette = [0xffffffff, 0xffccffff, 0xff99ffff, 0xff66ffff, 0xff33ffff, 0xff00ffff, 0xffffccff,
                                0xffccccff, 0xff99ccff, 0xff66ccff, 0xff33ccff, 0xff00ccff, 0xffff99ff, 0xffcc99ff,
                                0xff9999ff, 0xff6699ff, 0xff3399ff, 0xff0099ff, 0xffff66ff, 0xffcc66ff, 0xff9966ff,
                                0xff6666ff, 0xff3366ff, 0xff0066ff, 0xffff33ff, 0xffcc33ff, 0xff9933ff, 0xff6633ff,
                                0xff3333ff, 0xff0033ff, 0xffff00ff, 0xffcc00ff, 0xff9900ff, 0xff6600ff, 0xff3300ff,
                                0xff0000ff, 0xffffffcc, 0xffccffcc, 0xff99ffcc, 0xff66ffcc, 0xff33ffcc, 0xff00ffcc,
                                0xffffcccc, 0xffcccccc, 0xff99cccc, 0xff66cccc, 0xff33cccc, 0xff00cccc, 0xffff99cc,
                                0xffcc99cc, 0xff9999cc, 0xff6699cc, 0xff3399cc, 0xff0099cc, 0xffff66cc, 0xffcc66cc,
                                0xff9966cc, 0xff6666cc, 0xff3366cc, 0xff0066cc, 0xffff33cc, 0xffcc33cc, 0xff9933cc,
                                0xff6633cc, 0xff3333cc, 0xff0033cc, 0xffff00cc, 0xffcc00cc, 0xff9900cc, 0xff6600cc,
                                0xff3300cc, 0xff0000cc, 0xffffff99, 0xffccff99, 0xff99ff99, 0xff66ff99, 0xff33ff99,
                                0xff00ff99, 0xffffcc99, 0xffcccc99, 0xff99cc99, 0xff66cc99, 0xff33cc99, 0xff00cc99,
                                0xffff9999, 0xffcc9999, 0xff999999, 0xff669999, 0xff339999, 0xff009999, 0xffff6699,
                                0xffcc6699, 0xff996699, 0xff666699, 0xff336699, 0xff006699, 0xffff3399, 0xffcc3399,
                                0xff993399, 0xff663399, 0xff333399, 0xff003399, 0xffff0099, 0xffcc0099, 0xff990099,
                                0xff660099, 0xff330099, 0xff000099, 0xffffff66, 0xffccff66, 0xff99ff66, 0xff66ff66,
                                0xff33ff66, 0xff00ff66, 0xffffcc66, 0xffcccc66, 0xff99cc66, 0xff66cc66, 0xff33cc66,
                                0xff00cc66, 0xffff9966, 0xffcc9966, 0xff999966, 0xff669966, 0xff339966, 0xff009966,
                                0xffff6666, 0xffcc6666, 0xff996666, 0xff666666, 0xff336666, 0xff006666, 0xffff3366,
                                0xffcc3366, 0xff993366, 0xff663366, 0xff333366, 0xff003366, 0xffff0066, 0xffcc0066,
                                0xff990066, 0xff660066, 0xff330066, 0xff000066, 0xffffff33, 0xffccff33, 0xff99ff33,
                                0xff66ff33, 0xff33ff33, 0xff00ff33, 0xffffcc33, 0xffcccc33, 0xff99cc33, 0xff66cc33,
                                0xff33cc33, 0xff00cc33, 0xffff9933, 0xffcc9933, 0xff999933, 0xff669933, 0xff339933,
                                0xff009933, 0xffff6633, 0xffcc6633, 0xff996633, 0xff666633, 0xff336633, 0xff006633,
                                0xffff3333, 0xffcc3333, 0xff993333, 0xff663333, 0xff333333, 0xff003333, 0xffff0033,
                                0xffcc0033, 0xff990033, 0xff660033, 0xff330033, 0xff000033, 0xffffff00, 0xffccff00,
                                0xff99ff00, 0xff66ff00, 0xff33ff00, 0xff00ff00, 0xffffcc00, 0xffcccc00, 0xff99cc00,
                                0xff66cc00, 0xff33cc00, 0xff00cc00, 0xffff9900, 0xffcc9900, 0xff999900, 0xff669900,
                                0xff339900, 0xff009900, 0xffff6600, 0xffcc6600, 0xff996600, 0xff666600, 0xff336600,
                                0xff006600, 0xffff3300, 0xffcc3300, 0xff993300, 0xff663300, 0xff333300, 0xff003300,
                                0xffff0000, 0xffcc0000, 0xff990000, 0xff660000, 0xff330000, 0xff0000ee, 0xff0000dd,
                                0xff0000bb, 0xff0000aa, 0xff000088, 0xff000077, 0xff000055, 0xff000044, 0xff000022,
                                0xff000011, 0xff00ee00, 0xff00dd00, 0xff00bb00, 0xff00aa00, 0xff008800, 0xff007700,
                                0xff005500, 0xff004400, 0xff002200, 0xff001100, 0xffee0000, 0xffdd0000, 0xffbb0000,
                                0xffaa0000, 0xff880000, 0xff770000, 0xff550000, 0xff440000, 0xff220000, 0xff110000,
                                0xffeeeeee, 0xffdddddd, 0xffbbbbbb, 0xffaaaaaa, 0xff888888, 0xff777777, 0xff555555,
                                0xff444444, 0xff222222, 0xff111111]

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

    def save(self, filename):
        # grab the voxel data
        voxels = self.api.get_voxel_data()

        data = [0x20584f56, 150, 0x4e49414d, 0]
        sizeChunk = [0x455a4953, 12, 0, voxels.width, voxels.depth, voxels.height]

        voxelChunk = []
        paletteChunk = [0x41424752, 1024, 0]
        helpPalette = {}
        for z in xrange(voxels.height):
            for y in xrange(voxels.depth):
                for x in xrange(voxels.width):
                    vox = voxels.get(x, z, y)
                    if vox != 0:
                        if vox not in helpPalette:
                            r = (vox & 0xff000000) >> 24
                            g = (vox & 0x00ff0000) >> 16
                            b = (vox & 0x0000ff00) >> 8
                            paletteChunk.append(r | g << 8 | b << 16 | 0xff << 24)
                            helpPalette[vox] = len(paletteChunk) - 3
                        voxelChunk.append(((helpPalette[vox]) << 24) | (z << 16) | (y << 8) | x)
        while len(paletteChunk) < 259:
            paletteChunk.append(0xffffffff)
        data.append(1076 + 4 * len(voxelChunk))
        data += sizeChunk
        data += [0x495a5958, 4 * len(voxelChunk) + 4, 0, len(voxelChunk)]
        data += voxelChunk
        data += paletteChunk

        # Open our file
        f = open(filename, "wb")
        for i in data:
            self.uint32(f, i)

        # Tidy up
        f.close()

    def load(self, filename):
        # grab the voxel data
        voxels = self.api.get_voxel_data()

        # Open our file
        f = open(filename, "rb")

        meta = f.read(4)
        if meta != "VOX ":
            raise Exception("Expected Magica Voxel header not found")

        version = self.uint32(f)

        mainChunkId = f.read(4)
        if mainChunkId != "MAIN":
            raise Exception("Didn't found main Chunk as expected")

        mainChunkSize = self.uint32(f)
        mainChunkChildSize = self.uint32(f)

        chunkPointer = 20 + mainChunkSize
        sizeBegin = voxelBegin = paletteBegin = paletteLength = -1

        while chunkPointer < 20 + mainChunkSize + mainChunkChildSize:
            f.seek(chunkPointer)
            chunkId = f.read(4)
            chunkSize = self.uint32(f)
            chunkChildSize = self.uint32(f)
            if chunkId == "SIZE":
                sizeBegin = chunkPointer + 12
            elif chunkId == "XYZI":
                voxelBegin = chunkPointer + 12
            elif chunkId == "RGBA":
                paletteBegin = chunkPointer + 12
                paletteLength = chunkSize
            chunkPointer += 12 + chunkSize + chunkChildSize
        if sizeBegin == -1 or voxelBegin == -1:
            raise Exception("missing chunks")

        # read size chunk
        f.seek(sizeBegin)
        x = self.uint32(f)
        y = self.uint32(f)
        z = self.uint32(f)
        voxels.resize(x, z, y)

        # read palette chunk
        palette = []
        if paletteBegin == -1 or paletteLength == -1:
            palette = self.default_palette
        else:
            f.seek(paletteBegin)
            for i in xrange(0, paletteLength / 4):
                palette.append(self.uint32(f))

        # read voxel chunk
        f.seek(voxelBegin)
        voxelCount = self.uint32(f)
        for i in xrange(0, voxelCount):
            vox = self.uint32(f)
            ix = (vox & 0x000000ff) >> 0
            iy = (vox & 0x0000ff00) >> 8
            iz = (vox & 0x00ff0000) >> 16
            ip = (vox & 0xff000000) >> 24
            b = (palette[ip - 1] & 0x00ff0000) >> 16
            g = (palette[ip - 1] & 0x0000ff00) >> 8
            r = (palette[ip - 1] & 0x000000ff) >> 0
            voxels.set(ix, iz, iy, (r << 24) | (g << 16) | (b << 8) | 0xff)
        f.close()

register_plugin(MagicaFile, "Magica Voxel (.vox) file format IO", "1.0")
