# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "tobera_blender",
    "author" : "tobera_blender",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy


class MyAddonProperties(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(subtype="FILE_PATH")


class MyAddonOperator(bpy.types.Operator):
    bl_idname = "object.my_addon_operator"
    bl_label = "My Addon Operator"

    # Define properties
    path: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        # Perform your procedure with the selected path
        print("Path:", self.path)
        # Add your procedure code here

        return {'FINISHED'}

    def invoke(self, context, event):
        # Open the file selector
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes = (MyAddonProperties, MyAddonOperator)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyAddonProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_addon_props


if __name__ == "__main__":
    register()
