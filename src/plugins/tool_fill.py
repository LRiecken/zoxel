# Simple tool for flood fill.
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
from PySide2 import QtGui, QtWidgets
from tool import Tool, EventData, MouseButtons, KeyModifiers, Face
from plugin_api import register_plugin


class FillTool(Tool):

    def __init__(self, api):
        super(FillTool, self).__init__(api)
        # Create our action / icon
        self.action = QtWidgets.QAction(QtGui.QPixmap(":/images/gfx/icons/paint-can.png"), "Fill", None)
        self.action.setStatusTip("Flood fill with color")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+6"))
        # Register the tool
        self.priority = 6
        self.api.register_tool(self)

    # Fill all connected voxels of the same color with a new color
    def on_mouse_click(self, data):
        data.voxels.clear_selection()
        # We need to have a selected voxel
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if not voxel:
            return
        # Grab the target color
        search_color = voxel
        # Don't allow invalid fills
        c = self.color.getRgb()
        fill_color = c[0] << 24 | c[1] << 16 | c[2] << 8 | 0xff
        if search_color == fill_color:
            return
        # Initialise our search list
        search = set()
        search.add((data.world_x, data.world_y, data.world_z))
        # Keep iterating over the search list until no more to do
        while len(search):
            x, y, z = search.pop()
            voxel = data.voxels.get(x, y, z)
            if not voxel or voxel != search_color:
                continue
            # Add all likely neighbours into our search list
            if data.voxels.get(x - 1, y, z) == search_color:
                search.add((x - 1, y, z))
            if data.voxels.get(x + 1, y, z) == search_color:
                search.add((x + 1, y, z))
            if data.voxels.get(x, y + 1, z) == search_color:
                search.add((x, y + 1, z))
            if data.voxels.get(x, y - 1, z) == search_color:
                search.add((x, y - 1, z))
            if data.voxels.get(x, y, z + 1) == search_color:
                search.add((x, y, z + 1))
            if data.voxels.get(x, y, z - 1) == search_color:
                search.add((x, y, z - 1))
            # Set the color of the current voxel
            data.voxels.set(x, y, z, self.color, True, 1)
        data.voxels.completeUndoFill()

register_plugin(FillTool, "Fill Tool", "1.0")
