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
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+0"))
        # Register the tool
        self.api.register_tool(self)
        # Area tool helper
        self._mouse = None
        self._stamp = []
        self.xdir = True
        self.ydir = True
        self.zdir = True
        self.pastoffset = 0
        self.fixeddirection = False

    def drawstamp(self, data, dx, dy, dz):
        for x, y, z, col in self._stamp:
            tgt = data.voxels.get(x + dx, y + dy, z + dz)
            if tgt == 0:
                data.voxels.set(x + dx, y + dy, z + dz, col, True, 1)
        data.voxels.completeUndoFill()

    def on_drag_start(self, target):
        if len(target.voxels._selection) > 0:
            self._stamp = []
            for x, y, z in target.voxels._selection:
                col = target.voxels.get(x, y, z)
                self._stamp.append((x, y, z, col))
        self._mouse = (target.mouse_x, target.mouse_y)
        if QtCore.Qt.Key_X in target.keys:
            self.xdir = True
            self.ydir = False
            self.zdir = False
            self.fixeddirection = True
        elif QtCore.Qt.Key_Y in target.keys:
            self.xdir = False
            self.ydir = True
            self.zdir = False
            self.fixeddirection = True
        elif QtCore.Qt.Key_Z in target.keys:
            self.xdir = False
            self.ydir = False
            self.zdir = True
            self.fixeddirection = True
        else:
            self.xdir = True
            self.ydir = True
            self.zdir = True
            self.fixeddirection = False
        self.pastoffset = 0

    # When dragging, create the selection
    def on_drag(self, target):
        # In case the first click has missed a valid target.
        if self._mouse is None or len(self._stamp) == 0:
            return
        dx = target.mouse_x - self._mouse[0]
        dy = target.mouse_y - self._mouse[1]
        # Work out some sort of vague translation between screen and voxels
        sx = self.api.mainwindow.width() / target.voxels.width
        sy = self.api.mainwindow.height() / target.voxels.height
        dx = int(round(dx / float(sx)))
        dy = int(round(dy / float(sy)))
        if dx == 0 and dy == 0:
            return
        # Work out translation for x,y
        ax, ay = self.api.mainwindow.display.view_axis()
        tx = 0
        ty = 0
        tz = 0
        tdx = 0
        tdy = 0
        tdz = 0
        if ax == self.api.mainwindow.display.X_AXIS:
            tdx = dx
            if dx > 0:
                tx = 1
            elif dx < 0:
                tx = -1
        elif ax == self.api.mainwindow.display.Y_AXIS:
            tdy = dx
            if dx > 0:
                ty = 1
            elif dx < 0:
                ty = -1
        elif ax == self.api.mainwindow.display.Z_AXIS:
            tdz = dx
            if dx > 0:
                tz = 1
            elif dx < 0:
                tz = -1
        if ay == self.api.mainwindow.display.X_AXIS:
            tdx = dy
            if dy > 0:
                tx = 1
            elif dy < 0:
                tx = -1
        elif ay == self.api.mainwindow.display.Y_AXIS:
            tdy = dy
            if dy > 0:
                ty = -1
            elif dy < 0:
                ty = 1
        elif ay == self.api.mainwindow.display.Z_AXIS:
            tdz = dy
            if dy > 0:
                tz = 1
            elif dy < 0:
                tz = -1

        if self.fixeddirection:
            if self.xdir:
                if tx != 0:
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.pastoffset += tx
                    self.drawstamp(target, self.pastoffset, 0, 0)
            elif self.ydir:
                if ty != 0:
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.pastoffset += ty
                    self.drawstamp(target, 0, self.pastoffset, 0)
            elif self.zdir:
                if tz != 0:
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.pastoffset += tz
                    self.drawstamp(target, 0, 0, self.pastoffset)
        else:
            if tx != 0 and self.xdir and (not self.ydir or (abs(tdx) > abs(tdy) and abs(tdx) > abs(tdz))):
                self._mouse = (target.mouse_x, target.mouse_y)
                self.ydir = False
                self.zdir = False
                self.pastoffset += tx
                self.drawstamp(target, self.pastoffset, 0, 0)
            elif ty != 0 and self.ydir and (not self.zdir or abs(tdy) > abs(tdz)):
                self._mouse = (target.mouse_x, target.mouse_y)
                self.xdir = False
                self.zdir = False
                self.pastoffset += ty
                self.drawstamp(target, 0, self.pastoffset, 0)
            elif tz != 0 and self.zdir:
                self._mouse = (target.mouse_x, target.mouse_y)
                self.xdir = False
                self.ydir = False
                self.pastoffset += tz
                self.drawstamp(target, 0, 0, self.pastoffset)

    def on_drag_end(self, data):
        data.voxels.clear_selection()
        dx = self.xdir and self.pastoffset or 0
        dy = self.ydir and self.pastoffset or 0
        dz = self.zdir and self.pastoffset or 0
        for x, y, z, col in self._stamp:
            data.voxels.select(x + dx, y + dy, z + dz)

register_plugin(ExtrudeTool, "Extrude Tool", "1.0")
