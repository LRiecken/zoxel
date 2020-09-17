# plugin_api.py
# API for system plugins.
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
from PySide2 import QtWidgets


class PluginManager(object):
    plugins = []


class PluginAPI(object):

    def __init__(self):
        # All plugins get a reference to our application
        self.application = QtWidgets.QApplication.instance()
        # And our main window
        self.mainwindow = self.application.mainwindow

    # Register a drawing tool with the system
    def register_tool(self, tool, activate=False):
        # Create an instance
        self.mainwindow.register_tool(tool, activate)

    # Register an importer/exporter with the system
    def register_file_handler(self, handler):
        self.mainwindow.register_file_handler(handler)

    # Get the currently selected color from the palette
    def get_palette_color(self):
        return self.mainwindow.display.voxel_color

    # Changee the GUI palette to the given color.
    # Accepts QColors and 32bit integer RGBA
    def set_palette_color(self, color):
        self.mainwindow.color_palette.color = color

    # Returns the current voxel data
    def get_voxel_data(self):
        return self.mainwindow.display.voxels

    # Returns the current voxel model mesh data
    # vertices, colors, normals
    def get_voxel_mesh(self):
        vert, col, norm, _, _ = self.mainwindow.display.voxels.get_vertices()
        return (vert, col, norm)

    # Get and set persistent config values. value can be any serialisable type.
    # name should be a hashable type, like a simple string.
    def set_config(self, name, value):
        self.api.mainwindow.set_setting(name, value)

    def get_config(self, name):
        return self.api.mainwindow.get_setting(name)

    # Display a warning message
    def warning(self, message):
        QtWidgets.QMessageBox.warning(self.mainwindow, "Warning", message)

# Plugin registration
# Plugins call this function to register with the system.  A plugin
# should pass the class which will be instaniated by the application,
# this constructor is passed an instance of the system plugin API.


def register_plugin(plugin_class, name, version):
    # Create an instance of the API to send to the plugin
    # Plugins access the main app via this API instance
    api = PluginAPI()
    plugin = plugin_class(api)
    PluginManager.plugins.append(plugin)
    return api
