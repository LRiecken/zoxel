# tool_select.py
# Selection tool.
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
from PySide import QtGui, QtCore
from tool import Tool, EventData, MouseButtons, KeyModifiers, Face
from plugin_api import register_plugin


class SelectionTool(Tool):

    def __init__(self, api):
        super(SelectionTool, self).__init__(api)
        # Create our action / icon
        self.action = QtGui.QAction(
            QtGui.QPixmap(":/images/gfx/icons/border.png"),
            "Select", None)
        self.action.setStatusTip("Select voxels")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+9"))
        # Register the tool
        self.api.register_tool(self)
        # Area tool helper
        self._first_target = None

    def select(self, data, x, y, z, deselect=False):
        if self._first_target is None:
            return
        xpos = self._first_target[0]
        ypos = self._first_target[1]
        zpos = self._first_target[2]
        xdelt = 1
        ydelt = 1
        zdelt = 1
        if self._first_target[0] > x:
                xdelt = -1
        if self._first_target[1] > y:
                ydelt = -1
        if self._first_target[2] > z:
                zdelt = -1
        for xidx in range(abs(self._first_target[0] - x) + 1):
            for yidx in range(abs(self._first_target[1] - y) + 1):
                for zidx in range(abs(self._first_target[2] - z) + 1):
                    test = data.voxels.get(xpos + (xidx * xdelt), ypos + (yidx * ydelt), zpos + (zidx * zdelt))
                    if test != 0:
                        if not deselect:
                            data.voxels.select(xpos + (xidx * xdelt), ypos + (yidx * ydelt), zpos + (zidx * zdelt))
                        else:
                            data.voxels.deselect(xpos + (xidx * xdelt), ypos + (yidx * ydelt), zpos + (zidx * zdelt))

    def on_mouse_click(self, data):
        mouse_btn = data.mouse_button
        shift_down = not not data.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier
        ctrl_down = not not data.key_modifiers & QtCore.Qt.KeyboardModifier.ControlModifier
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if mouse_btn == 2:
            data.voxels.clear_selection()
            self._first_target = None
        else:
            if voxel != 0:
                if ctrl_down:
                    self.select(data, data.world_x, data.world_y, data.world_z, True)
                    self._first_target = (data.world_x, data.world_y, data.world_z)
                elif shift_down:
                    self.select(data, data.world_x, data.world_y, data.world_z)
                    self._first_target = (data.world_x, data.world_y, data.world_z)
                else:
                    self._first_target = (data.world_x, data.world_y, data.world_z)
                    if data.voxels.is_selected(data.world_x, data.world_y, data.world_z):
                        data.voxels.deselect(data.world_x, data.world_y, data.world_z)
                    else:
                        data.voxels.select(data.world_x, data.world_y, data.world_z)
                    
    
    # Start a drag
    def on_drag_start(self, data):
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if voxel != 0:
            self._first_target = (data.world_x, data.world_y, data.world_z)

    # When dragging, create the selection
    def on_drag(self, data):
        # In case the first click has missed a valid target.
        if self._first_target is None:
            return
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if voxel != 0:
            data.voxels.clear_selection()
            self.select(data, data.world_x, data.world_y, data.world_z)
            
register_plugin(SelectionTool, "Selection Tool", "1.0")
