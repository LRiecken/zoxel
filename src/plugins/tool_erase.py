# tool_erase.py
# Simple voxel removal tool
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
from PySide2 import QtGui, QtWidgets
from tool import Tool
from plugin_api import register_plugin


class EraseTool(Tool):

    def __init__(self, api):
        super(EraseTool, self).__init__(api)
        # Create our action / icon
        self.action = QtWidgets.QAction(QtGui.QPixmap(":/images/gfx/icons/shovel.png"), "Erase", None)
        self.action.setStatusTip("Erase voxels")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+3"))
        # Register the tool
        self.priority = 3
        self.api.register_tool(self)

    # Clear the targeted voxel
    def on_mouse_click(self, data):
        if len(data.voxels._selection) > 0:
            for x, y, z in data.voxels._selection:
                data.voxels.set(x, y, z, 0, True, 1)
            data.voxels.completeUndoFill()
            data.voxels.clear_selection()
        else:
            data.voxels.set(data.world_x, data.world_y, data.world_z, 0)

register_plugin(EraseTool, "Erasing Tool", "1.0")
