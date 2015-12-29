# tool_drag.py
# Model moving tool.
# Copyright (c) 2013, Graham R King, Lennart Riecken
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


class DragTool(Tool):

    def __init__(self, api):
        super(DragTool, self).__init__(api)
        # Create our action / icon
        self.action = QtGui.QAction(
            QtGui.QPixmap(":/images/gfx/icons/arrow-in-out.png"),
            "Move Model", None)
        self.action.setStatusTip("Move Model")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+4"))
        # Register the tool
        self.api.register_tool(self)
        self._stamp = []
        self._lastdraw = []
        self._original = []
        self.xdir = True
        self.ydir = True
        self.zdir = True
        self.pastoffset = 0
        self.fixeddirection = False
        self.keeporiginal = False

        self._mouse = ()

    def check_free_space(self, data, dx, dy, dz, keeporiginal=False):
        for x, y, z, col in self._stamp:
            newx = (x + dx) % data.voxels.width
            newy = (y + dy) % data.voxels.height
            newz = (z + dz) % data.voxels.depth
            if data.voxels.get(newx, newy, newz) != 0 and (not (newx, newy, newz) in data.voxels._selection or
                                                               (keeporiginal and (newx, newy, newz) in self._original)):
                return False
        return True

    def drawstamp(self, data, dx, dy, dz, keeporiginal=False):
        if self.check_free_space(data, dx, dy, dz, keeporiginal):
            thisdraw = []
            data.voxels.clear_selection()
            for x, y, z, col in self._stamp:
                newx = (x + dx) % data.voxels.width
                newy = (y + dy) % data.voxels.height
                newz = (z + dz) % data.voxels.depth
                data.voxels.set(newx, newy, newz, col, True, 1)
                thisdraw.append((newx, newy, newz))
                data.voxels.select(newx, newy, newz)
            for x, y, z in self._lastdraw:
                if not (x, y, z) in thisdraw:
                    if not keeporiginal or not (x, y, z) in self._original:
                        data.voxels.set(x, y, z, 0, True, 1)
            self._lastdraw = thisdraw
            data.voxels.completeUndoFill()
        else:
            pass

    # Color the targeted voxel
    def on_drag_start(self, target):
        self.keeporiginal = not not target.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier
        self._mouse = (target.mouse_x, target.mouse_y)
        if len(target.voxels._selection) > 0:
            self._stamp = []
            self._lastdraw = []
            for x, y, z in target.voxels._selection:
                col = target.voxels.get(x, y, z)
                self._stamp.append((x, y, z, col))
                self._lastdraw.append((x, y, z))
                self._original.append((x, y, z))
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

    # Drag the model in voxel space
    def on_drag(self, target):
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

        if len(target.voxels._selection) == 0:
            if self.fixeddirection:
                if self.xdir:
                    if tx != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        target.voxels.translate(tx, 0, 0)
                elif self.ydir:
                    if ty != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        target.voxels.translate(0, ty, 0)
                elif self.zdir:
                    if tz != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        target.voxels.translate(0, 0, tz)
            else:
                target.voxels.translate(tx, ty, tz)
        else:
            if self.fixeddirection:
                if self.xdir:
                    if tx != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        self.pastoffset += tx
                        self.drawstamp(target, self.pastoffset, 0, 0, self.keeporiginal)
                elif self.ydir:
                    if ty != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        self.pastoffset += ty
                        self.drawstamp(target, 0, self.pastoffset, 0, self.keeporiginal)
                elif self.zdir:
                    if tz != 0:
                        self._mouse = (target.mouse_x, target.mouse_y)
                        self.pastoffset += tz
                        self.drawstamp(target, 0, 0, self.pastoffset, self.keeporiginal)
            else:
                if tx != 0 and self.xdir and (not self.ydir or (abs(tdx) > abs(tdy) and abs(tdx) > abs(tdz))):
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.ydir = False
                    self.zdir = False
                    self.pastoffset += tx
                    self.drawstamp(target, self.pastoffset, 0, 0, self.keeporiginal)
                elif ty != 0 and self.ydir and (not self.zdir or abs(tdy) > abs(tdz)):
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.xdir = False
                    self.zdir = False
                    self.pastoffset += ty
                    self.drawstamp(target, 0, self.pastoffset, 0, self.keeporiginal)
                elif tz != 0 and self.zdir:
                    self._mouse = (target.mouse_x, target.mouse_y)
                    self.xdir = False
                    self.ydir = False
                    self.pastoffset += tz
                    self.drawstamp(target, 0, 0, self.pastoffset, self.keeporiginal)


register_plugin(DragTool, "Drag Tool", "1.0")
