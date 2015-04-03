from base64 import b64encode
from struct import pack
from plugin_api import PluginAPI

class TroxelLink:

    def __init__(self):
        self.api = PluginAPI()

    def export(self):
        voxels = self.api.get_voxel_data()

        data = [voxels.width, voxels.height, voxels.depth, 0, 85, 0, 0]
        vox = []

        for z in xrange(voxels.depth - 1, -1, -1):
            for y in xrange(voxels.height):
                for x in xrange(voxels.width - 1, -1, -1):
                    v = voxels.get(x, y, z)
                    if v:
                        vox.append(((v & 0xff000000) >> 24, (v & 0xff0000) >> 16, (v & 0xff00) >> 8))
                    else:
                        vox.append(None)

        rcolors = dict()
        for v in vox:
            if v:
                hex = v[2] + 256 * v[1] + 65536 * v[0]
                data.extend((0, v[0], v[1], v[2], 255))
                rcolors[hex] = (len(data) - 7) // 5
        data[5] = (len(data) - 7) // 1280
        short = data[5] == 0
        data[6] = (len(data) - 7) // 5 % 256

        i = 0
        length = len(vox)
        while i < length:
            r = 1
            while r < 129:
                if (i + r < length) and (vox[i + r - 1] == vox[i + r]):
                    r += 1
                else:
                    break
            if r > 1:
                data.append(126 + r)
            if vox[i]:
                index = rcolors[ vox[i][2] + 256 * vox[i][1] + 65536 * vox[i][0] ]
                if short:
                    data.append(index)
                else:
                    data.extend((index // 256, index % 256))
            else:
                if short:
                    data.append(0)
                else:
                    data.extend((0, 0))
            i += r

        return "https://chrmoritz.github.io/Troxel/#m=" + b64encode(pack('B' * len(data), *data))
