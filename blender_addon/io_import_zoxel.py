# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Zoxel importer",
    "author": "Lennart Riecken",
    "version": (0, 0, 1),
    "blender": (2, 76, 0),
    "location": "File > Import-Export",
    "description": "Import Zoxel files",
    "category": "Import-Export"}


import bpy
import collections
import os
import json


from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        EnumProperty,
        CollectionProperty
        )



class ImportZOXEL(bpy.types.Operator):
    """Load a zoxel file"""
    bl_idname = "import_scene.zoxel"
    bl_label = "Import Zoxel"
    #bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".zox"

    filter_glob = StringProperty(
        default="*.zox",
        options={'HIDDEN'}
        )

    x_off = 0.1
    y_off = 0.1
    z_off = 0.1

    files = CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    directory = StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    def execute(self, context):
        for file in self.files:
            self.doImport(self.directory, file.name)
        return {'FINISHED'}

    def draw(self, context):
        self.layout.operator('file.select_all_toggle')

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def doImport(self, directory, filename):
        file = os.path.join(directory, filename)
        print("Loading: "+file)

        json_string_data = open(file).read()
        data = json.loads(json_string_data)
        i = 1;
        while "frame"+str(i) in data.keys():
            framedata = data["frame"+str(i)]
            self.importFrame(framedata, filename)
            i = i+1


    def hasVoxel(self, frame, x,y,z):
        for data in frame:
            if data[0] == x and data[1] == y and data[2] == z:
                return True
        return False

    def importFrame(self, frame, name):
        verts = []
        faces = []
        colors = []
        for data in frame:
            x = data[0]
            z = data[1]
            y = data[2]
            color = data[3]
            blender_color = (((color>>8) // 256 // 256 % 256) / 255, ((color>>8) // 256 % 256) / 255 , ((color>>8) % 256) / 255 )
            numVertAdded = 0

            vertOff = len(verts)

            verts.append( (x*self.x_off, y*self.y_off, z*self.z_off) )
            verts.append( (x*self.x_off+self.x_off, y*self.y_off, z*self.z_off) )
            verts.append( (x*self.x_off+self.x_off, y*self.y_off+self.y_off, z*self.z_off) )
            verts.append( (x*self.x_off, y*self.y_off+self.y_off, z*self.z_off) )

            verts.append( (x*self.x_off, y*self.y_off, z*self.z_off+self.z_off) )
            verts.append( (x*self.x_off+self.x_off, y*self.y_off, z*self.z_off+self.z_off) )
            verts.append( (x*self.x_off+self.x_off, y*self.y_off+self.y_off, z*self.z_off+self.z_off) )
            verts.append( (x*self.x_off, y*self.y_off+self.y_off, z*self.z_off+self.z_off) )

            #Bottom
            if not self.hasVoxel(frame, x, z-1, y):
                faces.append( (0+vertOff, 3+vertOff, 2+vertOff, 1+vertOff) )
                numVertAdded = numVertAdded+4

            #Top
            if not self.hasVoxel(frame, x, z+1, y):
                faces.append( (4+vertOff, 5+vertOff, 6+vertOff, 7+vertOff) )
                numVertAdded = numVertAdded+4

            #Left
            if not self.hasVoxel(frame, x-1, z, y):
                faces.append( (0+vertOff, 4+vertOff, 7+vertOff, 3+vertOff) )
                numVertAdded = numVertAdded+4

            #Right
            if not self.hasVoxel(frame, x+1, z, y):
                faces.append( (1+vertOff, 2+vertOff, 6+vertOff, 5+vertOff) )
                numVertAdded = numVertAdded+4

            #Back
            if not self.hasVoxel(frame, x, z, y+1):
                faces.append( (3+vertOff, 7+vertOff, 6+vertOff, 2+vertOff) )
                numVertAdded = numVertAdded+4

            #Front
            if not self.hasVoxel(frame, x, z, y-1):
                faces.append( (0+vertOff, 1+vertOff, 5+vertOff, 4+vertOff) )
                numVertAdded = numVertAdded+4

            for i in range(numVertAdded):
                colors.append(blender_color)

        meshdata = bpy.data.meshes.new(name)
        meshdata.from_pydata(verts, [], faces)
        cl = meshdata.vertex_colors.new()
        for i in range(len(colors)):
            cl.data[i].color = colors[i]

        meshdata.update()

        obj = bpy.data.objects.new(name, meshdata)
        scene = bpy.context.scene
        mesh = obj.data

        scene.objects.link(obj)
        obj.select = True
        scene.update()

        bpy.context.scene.objects.active = bpy.data.objects[obj.name]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.select_loose()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')


def menu_func_import(self, context):
    self.layout.operator(ImportZOXEL.bl_idname, text="Zoxel (.zox)")

def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
