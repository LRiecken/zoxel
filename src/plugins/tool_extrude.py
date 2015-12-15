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
        self.xdir = True
        self.ydir = True
        self.zdir = True
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
        # Work out translation for x,y
        ax, ay = self.api.mainwindow.display.view_axis()
        tx = 0
        ty = 0
        tz = 0
        if ax == self.api.mainwindow.display.X_AXIS:
            if dx > 0:
                tx = 1
            elif dx < 0:
                tx = -1
        if ax == self.api.mainwindow.display.Y_AXIS:
            if dx > 0:
                ty = 1
            elif dx < 0:
                ty = -1
        if ax == self.api.mainwindow.display.Z_AXIS:
            if dx > 0:
                tz = 1
            elif dx < 0:
                tz = -1
        if ay == self.api.mainwindow.display.X_AXIS:
            if dy > 0:
                tx = 1
            elif dy < 0:
                tx = -1
        if ay == self.api.mainwindow.display.Y_AXIS:
            if dy > 0:
                ty = -1
            elif dy < 0:
                ty = 1
        if ay == self.api.mainwindow.display.Z_AXIS:
            if dy > 0:
                tz = 1
            elif dy < 0:
                tz = -1

        if ty != 0 or tx != 0 or tz != 0:
            self._mouse = (target.mouse_x, target.mouse_y)
        if tx != 0 and self.xdir:
            self.ydir = False
            self.zdir = False
            self.pastoffset += tx
            self.drawstamp(target, self.pastoffset, 0, 0)
        if ty != 0 and self.ydir:
            self.xdir = False
            self.zdir = False
            self.pastoffset += ty
            self.drawstamp(target, 0, self.pastoffset, 0)
        if tz != 0 and self.zdir:
            self.xdir = False
            self.ydir = False
            self.pastoffset += tz
            self.drawstamp(target, 0, 0, self.pastoffset)
                  
register_plugin(ExtrudeTool, "Extrude Tool", "1.0")
