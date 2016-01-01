# mainwindow.py
# Zoxel - A Voxel Editor
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

import sys
import traceback
from PySide import QtGui
from mainwindow import MainWindow


def exception_handler(type, value, tb):
    traceback.print_exception(type, value, tb)
    msg = ""
    for line in traceback.format_exception(type, value, tb):
        msg += line
    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Zoxel has crashed!", "Sorry, Zoxel has just crashed. " +
                               "Please report the following error so it can be fixed:", QtGui.QMessageBox.Close)
    dialog.setDetailedText(msg)
    dialog.exec_()

sys.excepthook = exception_handler


def main():
    # create application
    app = QtGui.QApplication(sys.argv)

    # create mainWindow
    mainwindow = MainWindow()
    mainwindow.show()

    # Remember our main window
    app.mainwindow = mainwindow

    # Load system plugins
    mainwindow.load_plugins()

    # run main loop
    sys.exit(app.exec_())

# call main function
if __name__ == '__main__':
    main()
