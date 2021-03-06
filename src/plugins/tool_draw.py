# tool_draw.py
# Simple drawing tool.
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
from PySide2 import QtGui, QtCore, QtWidgets
from tool import Tool, EventData, MouseButtons, KeyModifiers, Face
from plugin_api import register_plugin


class DrawingTool(Tool):

    def __init__(self, api):
        super(DrawingTool, self).__init__(api)
        # Create our action / icon
        self.action = QtWidgets.QAction(QtGui.QPixmap(":/images/gfx/icons/pencil.png"), "Draw", None)
        self.action.setStatusTip("Draw Voxels")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+1"))
        # Register the tool
        self.priority = 1
        self.api.register_tool(self, True)
        # Area tool helper
        self.first_voxel = None

    # Tries to plot a new voxel at target location.
    # param choosen_target: The place where the new voxel should be inserted.
    # returns A Target object indicating the actual place where the voxel were
    # inserted. Returns None when no insertion was made.
    def _draw_voxel(self, data, shift_down, erase):
        # Works out where exactly the new voxel goes. It can collide with an existing voxel
        # or with the bottom of the 'y' plane, in which case, pos will be different than None.
        color = self.color
        if erase:
            color = 0
        else:
            pos = data.get_neighbour()
            if pos:
                data.world_x = pos[0]
                data.world_y = pos[1]
                data.world_z = pos[2]

        if shift_down and self.first_voxel is None:
            self.first_voxel = (data.world_x, data.world_y, data.world_z)
        elif self.first_voxel is None:
            if data.voxels.set(data.world_x, data.world_y, data.world_z, color):
                return data
            else:
                return None
        else:
            dx = 1 if data.world_x < self.first_voxel[0] else -1
            for x in xrange(data.world_x, self.first_voxel[0] + dx, dx):
                dy = 1 if data.world_y < self.first_voxel[1] else -1
                for y in xrange(data.world_y, self.first_voxel[1] + dy, dy):
                    dz = 1 if data.world_z < self.first_voxel[2] else -1
                    for z in xrange(data.world_z, self.first_voxel[2] + dz, dz):
                        data.voxels.set(x, y, z, color, True, 1)
            data.voxels.completeUndoFill()
            self.first_voxel = None
        return None

    def _get_valid_sequence_faces(self, face):
        if face in Face.COLLIDABLE_FACES_PLANE_X:
            return Face.COLLIDABLE_FACES_PLANE_Y + Face.COLLIDABLE_FACES_PLANE_Z
        elif face in Face.COLLIDABLE_FACES_PLANE_Y:
            return Face.COLLIDABLE_FACES_PLANE_X + Face.COLLIDABLE_FACES_PLANE_Z
        elif face in Face.COLLIDABLE_FACES_PLANE_Z:
            return Face.COLLIDABLE_FACES_PLANE_X + Face.COLLIDABLE_FACES_PLANE_Y
        else:
            return None

    # Draw a new voxel next to the targeted face
    def on_mouse_click(self, data):
        data.voxels.clear_selection()
        shift_down = not not data.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier
        self._first_target = self._draw_voxel(data, shift_down, data.mouse_button == MouseButtons.RIGHT)

    # Start a drag
    def on_drag_start(self, data):
        data.voxels.clear_selection()
        self._first_target = data

    # When dragging, Draw a new voxel next to the targeted face
    def on_drag(self, data):
        # In case the first click has missed a valid target.
        if self._first_target is None:
            return
        valid_faces = self._get_valid_sequence_faces(self._first_target.face)
        if (not valid_faces) or (data.face not in valid_faces):
            return
        self._draw_voxel(data, False, False)

register_plugin(DrawingTool, "Drawing Tool", "1.0")
