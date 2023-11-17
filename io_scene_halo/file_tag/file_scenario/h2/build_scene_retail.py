# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import os
import bpy
import bmesh
import numpy as np

from enum import Flag, auto
from math import degrees, radians
from mathutils import Vector, Quaternion, Euler, Matrix
from .format_retail import DataTypesEnum
from io_scene_halo.file_tag.file_structure_bsp import build_scene as build_scene_level
from io_scene_halo.file_tag.file_structure_lightmap import build_scene as build_scene_lightmap

def generate_comments(context, level_root, comment_tag_block):
    comment_collection = bpy.data.collections.get("Comments")
    if comment_collection == None:
        comment_collection = bpy.data.collections.new("Comments")
        context.scene.collection.children.link(comment_collection)

    for comment_idx, comment_element in enumerate(comment_tag_block):
        font = bpy.data.curves.new(type="FONT", name="comment")
        font_ob = bpy.data.objects.new("comment_%s" % comment_idx, font)
        font_ob.data.body = comment_element.comment

        font_ob.parent = level_root
        font_ob.location = comment_element.position * 100
        comment_collection.objects.link(font_ob)

def get_data_type(collection_name, root, tag_path, element):
        if collection_name == "BSPs":
            root.tag_view.data_type_enum = str(DataTypesEnum.clusters.value)
            root.tag_view.lightmap_index = -1

        elif collection_name == "Scenery":
            root.tag_view.data_type_enum = str(DataTypesEnum.scenery.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Biped":
            root.lock_rotation[0] = True
            root.lock_rotation[1] = True

            root.tag_view.data_type_enum = str(DataTypesEnum.bipeds.value)
            #set_object_data(root, tag_path, element)
            #set_unit_data(root, element)

        elif collection_name == "Vehicle":
            root.tag_view.data_type_enum = str(DataTypesEnum.vehicles.value)
            #set_object_data(root, tag_path, element)
            #set_unit_data(root, element)
            #set_vehicle_data(root, element)

        elif collection_name == "Equipment":
            root.tag_view.data_type_enum = str(DataTypesEnum.equipment.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Weapons":
            root.tag_view.data_type_enum = str(DataTypesEnum.weapons.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Machines":
            root.tag_view.data_type_enum = str(DataTypesEnum.machines.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Controls":
            root.tag_view.data_type_enum = str(DataTypesEnum.controls.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Light Fixtures":
            root.tag_view.data_type_enum = str(DataTypesEnum.light_fixtures.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Sound Scenery":
            root.tag_view.data_type_enum = str(DataTypesEnum.sound_scenery.value)
            #set_object_data(root, tag_path, element)

        elif collection_name == "Player Starting Locations":
            root.tag_view.data_type_enum = str(DataTypesEnum.player_starting_locations.value)

        elif collection_name == "Netgame Flags":
            root.tag_view.data_type_enum = str(DataTypesEnum.netgame_flags.value)

        elif collection_name == "Netgame Equipment":
            root.tag_view.data_type_enum = str(DataTypesEnum.netgame_equipment.value)

def generate_object_elements(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen):
    objects_list = []
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    if collection_name == "Scenery":
        asset_collection.hide_render = False
    elif collection_name == "Biped":
        asset_collection.hide_render = True
    elif collection_name == "Vehicle":
        asset_collection.hide_render = True
    elif collection_name == "Equipment":
        asset_collection.hide_render = True
    elif collection_name == "Weapons":
        asset_collection.hide_render = True
    elif collection_name == "Machines":
        asset_collection.hide_render = True
    elif collection_name == "Controls":
        asset_collection.hide_render = True
    elif collection_name == "Light Fixtures":
        asset_collection.hide_render = True
    elif collection_name == "Sound Scenery":
        asset_collection.hide_render = True

    for palette_idx, palette_element in enumerate(palette):
        ob = None
        objects_list.append(ob)

    for element_idx, element in enumerate(tag_block):
        pallete_item = palette[element.palette_index]
        tag_name = os.path.basename(pallete_item.name)

        name = "%s_%s" % (tag_name, element_idx)

        ob = objects_list[element.palette_index]
        if not ob == None:
            root = bpy.data.objects.new(name, ob.data)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)
        
        root.parent = level_root
        root.location = element.position * 100

        get_data_type(collection_name, root, pallete_item.name, element)

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.rotation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.rotation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.rotation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)

        root.rotation_euler = rotation

    for ob in objects_list:
        if not ob == None:
            bpy.data.objects.remove(ob, do_unlink=True)

def generate_netgame_equipment_elements(level_root, tag_block, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen):
    asset_collection = bpy.data.collections.get("Netgame Equipment")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Netgame Equipment")
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = None
        object_name = "%s_%s" % (os.path.basename(element.item_vehicle_collection.name), element_idx)
        ASSET = element.item_vehicle_collection.parse_tag(tag_format, report, "halo2", "retail")
        #if not ASSET == None:
            #if len(ASSET.item_permutations) > 0:
                #item_perutation_element = ASSET.item_permutations[0]
                #ITEM = item_perutation_element.item.parse_tag(tag_format, report, "halo1", "retail")
                #if item_perutation_element.item.tag_group == "eqip":
                    #MODEL = ITEM.equipment_body.model.parse_tag(tag_format, report, "halo1", "retail")
                    #if not MODEL == None:
                        #ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
                #elif item_perutation_element.item.tag_group == "weap":
                    #MODEL = ITEM.weapon_body.model.parse_tag(tag_format, report, "halo1", "retail")
                    #if not MODEL == None:
                        #ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)

        if ob == None:
            ob = bpy.data.objects.new(object_name, None)
            ob.empty_display_type = 'ARROWS'
            asset_collection.objects.link(ob)

        get_data_type("Netgame Equipment", ob, element.item_vehicle_collection.name, element)

        ob.parent = level_root
        ob.location = element.position * 100

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.orientation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.orientation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.orientation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)

        ob.rotation_euler = rotation

def generate_empties(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new("%s_%s" % (collection_name, element_idx), None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

        asset_collection.objects.link(ob)

def generate_camera_flags(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new(element.name, None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.facing[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.facing[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)

        ob.rotation_euler = rotation

        asset_collection.objects.link(ob)

def generate_camera_points(context, level_root, tag_block):
    asset_collection = bpy.data.collections.get("Cutscene Cameras")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Cutscene Cameras")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        camera_data = bpy.data.cameras.new(name='Camera')
        ob = bpy.data.objects.new(element.name, camera_data)

        ob.parent = level_root
        ob.location = element.position * 100

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.orientation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.orientation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.orientation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)

        ob.rotation_euler = rotation
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        asset_collection.objects.link(ob)

def generate_trigger_volumes(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        mesh = bpy.data.meshes.new("part_%s" % element.name)
        ob = bpy.data.objects.new(element.name, mesh)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        bm.transform(Matrix.Translation((1, 1, 1)))
        bm.to_mesh(mesh)
        bm.free()

        ob.parent = level_root
        right = np.cross(element.up, element.forward)
        matrix_rotation = Matrix((element.forward, right, element.up))

        ob.matrix_world = matrix_rotation.to_4x4()
        ob.location = element.position * 100
        ob.dimensions = element.extents * 100

        asset_collection.objects.link(ob)

def generate_scenario_scene(context, H2_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = bpy.data.collections.get("BSPs")
    if levels_collection == None:
        levels_collection = bpy.data.collections.new("BSPs")
        context.scene.collection.children.link(levels_collection)

    for bsp_idx, bsp_element in enumerate(H2_ASSET.structure_bsps):
        bsp = bsp_element.structure_bsp
        lightmap = bsp_element.structure_lightmap
        SBSP_ASSET = bsp.parse_tag(tag_format, report, "halo2", "retail")
        LTMP_ASSET = lightmap.parse_tag(tag_format, report, "halo2", "retail")

        bsp_name = os.path.basename(bsp.name)
        collection_name = "%s_%s" % (bsp_name, bsp_idx)
        level_collection = bpy.data.collections.get(collection_name)
        if level_collection == None:
            level_collection = bpy.data.collections.new(collection_name)
            levels_collection.children.link(level_collection)

        if not SBSP_ASSET == None:
            cluster_name = "%s_clusters" % bsp_name
            clusters_collection = bpy.data.collections.get(cluster_name)
            if clusters_collection == None:
                clusters_collection = bpy.data.collections.new(cluster_name)
                level_collection.children.link(clusters_collection)

            build_scene_level.build_scene(context, SBSP_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format, level_collection, clusters_collection)

        if not LTMP_ASSET == None:
            lightmap_name = "%s_lightmaps" % bsp_name
            lightmap_collection = bpy.data.collections.get(lightmap_name)
            if lightmap_collection == None:
                lightmap_collection = bpy.data.collections.new(lightmap_name)
                level_collection.children.link(lightmap_collection)

            build_scene_lightmap.build_scene(context, LTMP_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format, level_collection, lightmap_collection)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        context.collection.objects.link(level_root)

#    if len(H2_ASSET.skies) > 0:
#        generate_skies(context, level_root, H2_ASSET.skies, tag_format, report)
    if len(H2_ASSET.comments) > 0:
        generate_comments(context, level_root, H2_ASSET.comments)
    if len(H2_ASSET.scenery) > 0:
        generate_object_elements(level_root, "Scenery", H2_ASSET.scenery_palette, H2_ASSET.scenery, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.bipeds) > 0:
        generate_object_elements(level_root, "Biped", H2_ASSET.biped_palette, H2_ASSET.bipeds, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.vehicles) > 0:
        generate_object_elements(level_root, "Vehicle", H2_ASSET.vehicle_palette, H2_ASSET.vehicles, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.equipment) > 0:
        generate_object_elements(level_root, "Equipment", H2_ASSET.equipment_palette, H2_ASSET.equipment, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.weapons) > 0:
        generate_object_elements(level_root, "Weapons", H2_ASSET.weapon_palette, H2_ASSET.weapons, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.device_machines) > 0:
        generate_object_elements(level_root, "Machines", H2_ASSET.device_machine_palette, H2_ASSET.device_machines, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.device_controls) > 0:
        generate_object_elements(level_root, "Controls", H2_ASSET.device_control_palette, H2_ASSET.device_controls, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.device_light_fixtures) > 0:
        generate_object_elements(level_root, "Light Fixtures", H2_ASSET.device_light_fixtures_palette, H2_ASSET.device_light_fixtures, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.sound_scenery) > 0:
        generate_object_elements(level_root, "Sound Scenery", H2_ASSET.sound_scenery_palette, H2_ASSET.sound_scenery, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.player_starting_locations) > 0:
        generate_empties(context, level_root, "Player Starting Locations", H2_ASSET.player_starting_locations)
    if len(H2_ASSET.netgame_flags) > 0:
        generate_empties(context, level_root, "Netgame Flags", H2_ASSET.netgame_flags)
    if len(H2_ASSET.netgame_equipment) > 0:
        generate_netgame_equipment_elements(level_root, H2_ASSET.netgame_equipment, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H2_ASSET.trigger_volumes) > 0:
        generate_trigger_volumes(context, level_root, "Trigger Volumes", H2_ASSET.trigger_volumes)
    if len(H2_ASSET.cutscene_flags) > 0:
        generate_camera_flags(context, level_root, "Cutscene Flags", H2_ASSET.cutscene_flags)
    if len(H2_ASSET.cutscene_camera_points) > 0:
        generate_camera_points(context, level_root, H2_ASSET.cutscene_camera_points)
