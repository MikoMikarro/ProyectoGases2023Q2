import tempfile, os
import bpy
from bpy.types import Operator
from math import sin, cos, pi
from random import random, randint, choice
import numpy as np
import yaml

def create_cylinder(x_positions, radii, temperatures):
    # Set the number of segments to create a smooth cylinder
    segments = 32

    # Create a new mesh object
    #bpy.ops.object.select_all(action='DESELECT')
    #bpy.ops.object.select_by_type(type='MESH')
    #bpy.ops.object.delete()

    circles = []

    for i, (x, radius) in enumerate(zip(x_positions, radii)):
        if (i == len(x_positions)) -1 or (i == 0):
            bpy.ops.mesh.primitive_circle_add(
                fill_type='NOTHING',
                vertices=segments,
                radius=radius,
                location=(x, 0, 0),
                rotation=(0, pi/2,0)
            )
        else:
            bpy.ops.mesh.primitive_circle_add(
                fill_type='NOTHING',
                vertices=segments,
                radius=radius,
                location=(x, 0, 0),
                rotation=(0, pi/2,0)
            )
            
        circle = bpy.context.active_object
        circle.name = f"Circle_{i}"
        circles.append(circle)
        
    # Join all the circles into a single object
    bpy.ops.object.select_all(action='DESELECT')
    for circle in circles:
        circle.select_set(True)
    bpy.context.view_layer.objects.active = circles[0]
    bpy.ops.object.join()

    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')

    # Bridge the edge loops to create the cylinder
    bpy.ops.mesh.bridge_edge_loops()

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()

    material_name = "MyMaterial"
    material = bpy.data.materials.new(name=material_name)

    obj = bpy.context.active_object
    obj.data.materials.append(material)

    material.use_nodes = True  # Enable the use of node-based material editing
    princpled_bsdf = material.node_tree.nodes["Principled BSDF"]
    tree = material.node_tree
    tree.nodes.remove(princpled_bsdf) 
    new_volume_node = tree.nodes.new(type="ShaderNodeVolumePrincipled")
    output_node = tree.nodes["Material Output"]
    tree.links.new(new_volume_node.outputs["Volume"], output_node.inputs["Volume"])
    new_volume_node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    new_volume_node.inputs[8].default_value = 1
    bpy.context.scene.render.engine = 'CYCLES'

    
    texture_coordinates = tree.nodes.new(type="ShaderNodeTexCoord")
    mapping = tree.nodes.new(type="ShaderNodeMapping")
    separate_xyz = tree.nodes.new(type="ShaderNodeSeparateXYZ")

    tree.links.new(texture_coordinates.outputs["Generated"], mapping.inputs["Vector"])
    tree.links.new(mapping.outputs["Vector"], separate_xyz.inputs["Vector"])

    min_temperature = min(temperatures)
    max_temperature = max(temperatures)
    normalized_temperatures = [(i - min_temperature)/(max_temperature - min_temperature) for i in temperatures]

    color_ramp = tree.nodes.new(type="ShaderNodeValToRGB")

    # Decimete temperature values to be only 30
    temperatures = [temperatures[int(i*len(temperatures)/30)] for i in range(30)]
    
    # Set the color ramp to interpoalte between temperatures
    for i in range(len(temperatures)):

        color_ramp.color_ramp.elements.new(position=float(i+1)/len(temperatures))
        color_ramp.color_ramp.elements[i+1].color = (normalized_temperatures[i+1], normalized_temperatures[i+1], normalized_temperatures[i+1], 1)
    
    ## add the start and end color
    color_ramp.color_ramp.elements[0].color = (normalized_temperatures[0], normalized_temperatures[0], normalized_temperatures[0], 1)
    color_ramp.color_ramp.elements[-1].color = (normalized_temperatures[-1], normalized_temperatures[-1], normalized_temperatures[-1], 1)

    tree.links.new(separate_xyz.outputs["Z"], color_ramp.inputs["Fac"])

    map_range = tree.nodes.new(type="ShaderNodeMapRange")
    map_range.inputs["From Min"].default_value = 0
    map_range.inputs["From Max"].default_value = 1
    map_range.inputs["To Min"].default_value = min_temperature*4
    map_range.inputs["To Max"].default_value = max_temperature*4

    tree.links.new(color_ramp.outputs["Color"], map_range.inputs["Value"])
    tree.links.new(map_range.outputs["Result"], new_volume_node.inputs["Temperature"])




class AssetImporter(Operator):
    bl_idname = "asset.import_assets"
    bl_label = "Import Assets"
    bl_description = "This is the hello world operator"


    @classmethod
    def poll(cls, context):
        if context.scene.path_to_assets != "":
            return True
        return False

    def execute(self, context):
        fname = context.scene.path_to_assets
        with open(fname) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        x_positions = data['x_position']
        radii = data['radius_interior_fluid']
        temperatures = data['T_interior_fluid']

        create_cylinder(x_positions, radii, temperatures)


        
        return {'FINISHED'}