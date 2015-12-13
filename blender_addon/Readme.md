# Zoxel importer

This is a blender plugin for importing Zoxel files.
Zoxel is a free and open-source Voxel Editor.

You can download it here: https://github.com/grking/zoxel
You can find more information about it here: http://zoxel.blogspot.de/

Since the original development for Zoxel has halted you can find an improved fork
of Zoxel here: https://github.com/chrmoritz/zoxel

# Installing

To install this plugin clone this git repository or download the file:
io_import_zoxel.py
Open Blender and select: File / User Preferences / Add-ons
Click "Install from File..." and open the io_import_zoxel.py
Select the category "Import-Export" and activate the Zoxel importer plugin.

# Using

The plugin adds the option "Zoxel" to File / Import.
Select your zoxel file \(*.zox\) and select "Import Zoxel"

The Plugin will generate a new object for every frame in the zoxel file.
The color information will be imported as Vertex Colors.
You can render the color information with Cycles using the Attribute node.
You can view the color information in your viewport by selecting
View / Properties in your 3D View. Then under Shading activate "Textured Solid"

The plugin will not generate faces for voxels that have an adjacent voxel at the given side.
It will however generate interior faces if there is a "hole" in your voxel file.

# Copying

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
