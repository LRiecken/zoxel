# about_dialog.py
# A basic About dialog.
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
from ui_dialog_about import Ui_AboutDialog
from constants import ZOXEL_VERSION


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # Initialise the UI
        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.ver_label.setText("Version %s" % ZOXEL_VERSION)
