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
    "name" : "RandomButton Uti",
    "author" : "Miko Mikarro",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

from email.policy import default
import bpy

from . plugin_panel import HelloWorldPanel
from . plugin_operator import AssetImporter
from bpy.props import StringProperty
from bpy.types import Scene

classes = [
    HelloWorldPanel,
    AssetImporter,
]

def register():

    for new_class in classes:
        bpy.utils.register_class(new_class)
    
    Scene.path_to_assets = StringProperty(name="Assets", subtype="FILE_PATH", default=r'C:\Users\lopez\Desktop\Universidad\5b\Gases\ProyectoGases2023Q2\data.yml')

def unregister():
    
    for registered_class in classes:
        bpy.utils.unregister_class(registered_class)
    del Scene.path_to_assets

if __name__ == "__main__":
    register()