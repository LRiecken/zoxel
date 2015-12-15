# tool_extrude.py
# Extrusion tool.
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


class ExtrudeTool(Tool):

    def __init__(self, api):
        super(ExtrudeTool, self).__init__(api)
        # Create our action / icon
        self.action = QtGui.QAction(
            QtGui.QPixmap(":/images/gfx/icons/border-bottom-thick.png"),
            "Extrude", None)
        self.action.setStatusTip("Extude region")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+9"))
        # Register the tool
        self.api.register_tool(self)
        # Area tool helper
        self.regionstart = None
        self.regionend = None

    def regionvalid(self):
        if self.regionstart is None or self.regionend is None:
            return 0, False
        r = []
        if self.regionstart[0] == self.regionend[0]:
            r.append(0)  # Plane is on yz
        if self.regionstart[1] == self.regionend[1]:
            r.append(1)  # Plane is on xz
        if self.regionstart[2] == self.regionend[2]:
            r.append(2)  # Plane is on xy
        if len(r) == 1:  # If plane and not line or point
            return r.pop(), True
        return 0, False

    def do_extrude(self, target, value, region):
        xpos = self.regionstart[0]
        ypos = self.regionstart[1]
        zpos = self.regionstart[2]
        xdelt = 1
        ydelt = 1
        zdelt = 1
        if region == 0:
            if value < 0:
                xdelt = -1
            if self.regionstart[1] > self.regionend[1]:
                ydelt = -1
            if self.regionstart[2] > self.regionend[2]:
                zdelt = -1
            for xidx in range(abs(value)):
                for yidx in range(abs(self.regionstart[1] - self.regionend[1]) + 1):
                    for zidx in range(abs(self.regionstart[2] - self.regionend[2]) + 1):
                        src = target.voxels.get(xpos, ypos + (yidx * ydelt), zpos + (zidx * zdelt))
                        tgt = target.voxels.get(xpos + (xidx * xdelt) + xdelt, ypos +
                                                (yidx * ydelt), zpos + (zidx * zdelt))
                        if tgt == 0:
                            target.voxels.set(xpos + (xidx * xdelt) + xdelt, ypos +
                                              (yidx * ydelt), zpos + (zidx * zdelt), src, True, 1)
            target.voxels.completeUndoFill()
            return True
        if region == 1:
            if self.regionstart[0] > self.regionend[0]:
                xdelt = -1
            if value < 0:
                ydelt = -1
            if self.regionstart[2] > self.regionend[2]:
                zdelt = -1
            for yidx in range(abs(value)):
                for xidx in range(abs(self.regionstart[0] - self.regionend[0]) + 1):
                    for zidx in range(abs(self.regionstart[2] - self.regionend[2]) + 1):
                        src = target.voxels.get(xpos + (xidx * xdelt), ypos, zpos + (zidx * zdelt))
                        tgt = target.voxels.get(xpos + (xidx * xdelt), ypos +
                                                (yidx * ydelt) + ydelt, zpos + (zidx * zdelt))
                        if tgt == 0:
                            target.voxels.set(xpos + (xidx * xdelt), ypos + (yidx * ydelt) +
                                              ydelt, zpos + (zidx * zdelt), src, True, 1)
            target.voxels.completeUndoFill()
            return True
        if region == 2:
            if self.regionstart[0] > self.regionend[0]:
                xdelt = -1
            if self.regionstart[1] > self.regionend[1]:
                ydelt = -1
            if value < 0:
                zdelt = -1
            for zidx in range(abs(value)):
                for xidx in range(abs(self.regionstart[0] - self.regionend[0]) + 1):
                    for yidx in range(abs(self.regionstart[1] - self.regionend[1]) + 1):
                        src = target.voxels.get(xpos + (xidx * xdelt), ypos + (yidx * ydelt), zpos)
                        tgt = target.voxels.get(xpos + (xidx * xdelt), ypos + (yidx * ydelt),
                                                zpos + (zidx * zdelt) + zdelt)
                        if tgt == 0:
                            target.voxels.set(xpos + (xidx * xdelt), ypos + (yidx * ydelt),
                                              zpos + (zidx * zdelt) + zdelt, src, True, 1)
            target.voxels.completeUndoFill()
            return True
        return False

    def on_mouse_click(self, data):
        shift_down = not not (data.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier)
        if shift_down and self.regionstart is None:
            self.regionstart = [data.world_x, data.world_y, data.world_z]
        elif self.regionstart is not None:
            self.regionend = [data.world_x, data.world_y, data.world_z]
            region, valid = self.regionvalid()
            if valid:
                if region == 0:
                    directionHint = "\nPositive values mean to the right, negative mean to the left."
                    min = -1 * data.world_x
                    max = data.voxels.width - data.world_x - 1
                if region == 1:
                    directionHint = "\nPositive values mean up, negative mean down."
                    min = -1 * data.world_y
                    max = data.voxels.height - data.world_y - 1
                if region == 2:
                    directionHint = "\nPositive values mean to the back, negative mean to the front."
                    min = -1 * data.world_z
                    max = data.voxels.depth - data.world_z - 1
                value, ret = QtGui.QInputDialog.getInt(QtGui.QApplication.instance().mainwindow, "Extrude",
                                                       "Extrude region: " + str(self.regionstart) + " - " +
                                                       str(self.regionend) + directionHint, 0, min, max)
                if ret:
                    self.do_extrude(data, value, region)
            else:
                QtGui.QMessageBox.warning(QtGui.QApplication.instance().mainwindow, "Extrude",
                                          ("The region you selected is invalid. Try again.\n"
                                           "Make sure that they are on a plane in any direction.\n"
                                           "Extrusion can only be done in straigt directions. "
                                           "Top, bottom, left, right, back and front."), QtGui.QMessageBox.Ok)
            self.regionstart = None
            self.regionend = None
        else:
            QtGui.QMessageBox.warning(QtGui.QApplication.instance().mainwindow, "Extrude",
                                      ("You have not selected a region yet. "
                                       "Hold shift and click on two voxels that are on a flat plane in any direction."),
                                      QtGui.QMessageBox.Ok)


register_plugin(ExtrudeTool, "Extrude Tool", "1.0")
