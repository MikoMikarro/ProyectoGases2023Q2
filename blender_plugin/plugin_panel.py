import bpy
from bpy.types import Panel

class HelloWorldPanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tobera Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        # ASSETS BOX
        box = layout.box()
        
        row = box.row()
        row.prop(scene, "path_to_assets")
        row = box.row()
        row.operator("asset.import_assets")
        


        
        
        
