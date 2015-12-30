# tool_colorpick.py
# Simple color picking tool.
# Copyright (c) 2013, Graham R King
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
from PySide import QtGui
from tool import Tool
from plugin_api import register_plugin


class ColorPickTool(Tool):

    def __init__(self, api):
        super(ColorPickTool, self).__init__(api)
        # Create our action / icon
        self.action = QtGui.QAction(QtGui.QPixmap(":/images/gfx/icons/pipette.png"), "Color Pick", None)
        self.action.setStatusTip("Choose a color from an existing voxel.")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+5"))
        # Register the tool
        self.api.register_tool(self)

    # Grab the color of the selected voxel
    def on_mouse_click(self, data):
        # If we have a voxel at the target, color it
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if voxel:
            self.api.set_palette_color(voxel)

register_plugin(ColorPickTool, "Color Picking Tool", "1.0")
