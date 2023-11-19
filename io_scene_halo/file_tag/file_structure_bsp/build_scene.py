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

from math import radians
from mathutils import Vector, Matrix, Euler
from .h1.format_retail import ClusterPortalFlags, SurfaceFlags as H1SurfaceFlags
from .h2.format_retail import SurfaceFlags as H2SurfaceFlags

def get_triangle_info(part_list, strip_indices):
    part_points_sets = []
    for part in part_list:
        part_points = set()

        strip_length = part.strip_length
        strip_start = part.strip_start_index

        triangle_indices = strip_indices[strip_start : (strip_start + strip_length)]
        index_count = len(triangle_indices)
        for idx in range(index_count - 2):
            part_points.add(triangle_indices[idx])
            part_points.add(triangle_indices[idx + 1])
            part_points.add(triangle_indices[idx + 2])

        part_points_sets.append(part_points)

    return part_points_sets

def build_scene(context, LEVEL, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format, collection_override=None, cluster_collection_override=None):
    collection = context.collection
    if not collection_override == None:
        collection = collection_override

    if cluster_collection_override == None:
        cluster_collection_override = collection

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        collection.objects.link(level_root)

    level_root.hide_set(True)
    level_root.hide_render = True
    mesh_processing.select_object(context, level_root)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.mode_set(mode='OBJECT')
    if game_title == "halo1":
        if len(LEVEL.lightmaps) > 0:
            surfaces = LEVEL.surfaces
            for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
                if len(lightmap.materials) > 0:
                    cluster_name = "cluster_%s" % lightmap_idx
                    full_mesh = bpy.data.meshes.new(cluster_name)
                    object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
                    object_mesh.tag_view.data_type_enum = '1'
                    object_mesh.tag_view.lightmap_index = lightmap.bitmap_index

                    object_mesh.parent = level_root
                    cluster_collection_override.objects.link(object_mesh)
                    bm = bmesh.new()

                    for material_idx, material in enumerate(lightmap.materials):
                        has_lightmap = False
                        if material.vertices_count == material.lightmap_vertices_count:
                            has_lightmap = True

                        material_name = "material_%s" % material_idx
                        mesh = bpy.data.meshes.new(material_name)

                        triangles = []
                        start_index = material.surfaces

                        triangle_indices = []
                        triangles = []
                        vertices = [vertex.translation for vertex in material.uncompressed_render_vertices]
                        normals = [vertex.normal for vertex in material.uncompressed_render_vertices]

                        for idx in range(material.surface_count):
                            surface_idx = start_index + idx
                            triangles.append([surfaces[surface_idx].v2, surfaces[surface_idx].v1, surfaces[surface_idx].v0]) # Reversed order to fix facing normals

                        mesh.from_pydata(vertices, [], triangles)
                        mesh.normals_split_custom_set_from_vertices(normals)
                        for tri_idx, poly in enumerate(mesh.polygons):
                            poly.use_smooth = True

                        for triangle_idx, triangle in enumerate(triangles):
                            if material.shader_tag_ref.name_length > 0:
                                permutation_index = ""
                                if not material.shader_permutation == 0:
                                    permutation_index = "%s" % material.shader_permutation

                                material_name = "%s%s" % (os.path.basename(material.shader_tag_ref.name), permutation_index)

                            else:
                                material_name = "invalid_material_%s" % material_idx

                            mat = bpy.data.materials.get(material_name)
                            if mat is None:
                                mat = bpy.data.materials.new(name=material_name)
                                if material.shader_tag_ref.name_length > 0:
                                    if game_title == "halo1":
                                        mesh_processing.generate_shader(mat, material.shader_tag_ref, material.shader_permutation, tag_format, report)

                            if not material_name in object_mesh.data.materials.keys():
                                object_mesh.data.materials.append(mat)

                            mat.diffuse_color = random_color_gen.next()
                            material_index = object_mesh.data.materials.keys().index(material_name)
                            mesh.polygons[triangle_idx].material_index = material_index

                            render_vertex_list = [material.uncompressed_render_vertices[triangle[0]], material.uncompressed_render_vertices[triangle[1]], material.uncompressed_render_vertices[triangle[2]]]
                            for vertex_idx, vertex in enumerate(render_vertex_list):
                                loop_index = (3 * triangle_idx) + vertex_idx
                                uv_name = 'UVMap_%s' % 0
                                layer_uv = mesh.uv_layers.get(uv_name)
                                if layer_uv is None:
                                    layer_uv = mesh.uv_layers.new(name=uv_name)

                                U = vertex.UV[0]
                                V = vertex.UV[1]

                                layer_uv.data[loop_index].uv = (U, 1 - V)

                            if has_lightmap:
                                lightmap_vertex_list = [material.uncompressed_lightmap_vertices[triangle[0]], material.uncompressed_lightmap_vertices[triangle[1]], material.uncompressed_lightmap_vertices[triangle[2]]]
                                for vertex_idx, vertex in enumerate(lightmap_vertex_list):
                                    loop_index = (3 * triangle_idx) + vertex_idx
                                    uv_lightmap_name = 'UVMap_Lightmap_%s' % 0

                                    layer_uv_lightmap = mesh.uv_layers.get(uv_lightmap_name)
                                    if layer_uv_lightmap is None:
                                        layer_uv_lightmap = mesh.uv_layers.new(name=uv_lightmap_name)

                                    U_L = vertex.UV[0]
                                    V_L = vertex.UV[1]

                                    layer_uv_lightmap.data[loop_index].uv = (U_L, V_L)

                        bm.from_mesh(mesh)
                        bpy.data.meshes.remove(mesh)

                    bm.to_mesh(full_mesh)
                    bm.free()

        if len(LEVEL.cluster_portals) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            portal_object.parent = level_root
            collection.objects.link(portal_object)
            portal_object.hide_set(True)
            portal_object.hide_render = True
            for cluster in LEVEL.clusters:
                for portal in cluster.portals:
                    vert_indices = []
                    cluster_portal = LEVEL.cluster_portals[portal]
                    for vertex in cluster_portal.vertices:
                        vert_indices.append(portal_bm.verts.new(vertex.translation))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster.portals):
                    cluster_portal = LEVEL.cluster_portals[portal]
                    material_list = []

                    material_name = "+portal"
                    if ClusterPortalFlags.ai_cant_hear_through_this in ClusterPortalFlags(cluster_portal.flags):
                        material_name = "+portal&"

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in portal_object.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        portal_object.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    portal_bm.faces[portal_idx].material_index = material_index

                    cluster_portal = LEVEL.cluster_portals[portal]
                    poly = portal_bm.faces[portal_idx]
                    plane = LEVEL.collision_bsps[0].planes[cluster_portal.plane_index]
                    if poly.normal.dot(plane.point_3d) < 0:
                        poly.flip()

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

        for marker in LEVEL.markers:
            object_name_prefix = '#%s' % marker.name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker.name):
                marker_name_override = marker.name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)
            object_mesh.hide_set(True)
            object_mesh.hide_render = True

            object_mesh.ass_jms.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            mesh_processing.select_object(context, object_mesh)
            mesh_processing.select_object(context, level_root)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

            matrix_translate = Matrix.Translation(marker.translation)
            matrix_rotation = marker.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)
            object_mesh.select_set(False)
            level_root.select_set(False)

        if False: # MEK does this for some reason but lens flare markers are generated by settings in the shader. Enable if you need them for some reason.
            for lens_flare_marker in LEVEL.lens_flare_markers:
                lens_flare = LEVEL.lens_flares[lens_flare_marker.lens_flare_index]
                lens_flare_name = os.path.basename(lens_flare.name)
                object_name_prefix = '#%s' % lens_flare_name
                marker_name_override = ""
                if context.scene.objects.get('#%s' % lens_flare_name):
                    marker_name_override = lens_flare_name

                mesh = bpy.data.meshes.new(object_name_prefix)
                object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
                collection.objects.link(object_mesh)

                object_mesh.ass_jms.name_override = marker_name_override

                bm = bmesh.new()
                bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
                bm.to_mesh(mesh)
                bm.free()

                mesh_processing.select_object(context, object_mesh)
                mesh_processing.select_object(context, level_root)
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

                matrix_translate = Matrix.Translation(lens_flare_marker.position)
                lens_flare_euler = Euler((lens_flare_marker.direction_i_compenent / 128, lens_flare_marker.direction_j_compenent / 128, lens_flare_marker.direction_k_compenent / 128))
                matrix_rotation = lens_flare_euler.to_matrix().to_4x4()

                transform_matrix = matrix_translate @ matrix_rotation
                if fix_rotations:
                    transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

                object_mesh.matrix_world = transform_matrix
                object_mesh.data.ass_jms.Object_Type = 'SPHERE'
                object_mesh.dimensions = (2, 2, 2)
                object_mesh.select_set(False)
                level_root.select_set(False)

        if len(LEVEL.fog_planes) > 0:
            fog_planes_bm = bmesh.new()
            fog_planes_mesh = bpy.data.meshes.new("level_fog_planes")
            fog_planes_object = bpy.data.objects.new("level_fog_planes", fog_planes_mesh)
            fog_planes_object.parent = level_root
            collection.objects.link(fog_planes_object)
            fog_planes_object.hide_set(True)
            fog_planes_object.hide_render = True
            for fog_plane in LEVEL.fog_planes:
                vert_indices = []
                for vertex in fog_plane.vertices:
                    vert_indices.append(fog_planes_bm.verts.new(vertex.translation))

                fog_planes_bm.faces.new(vert_indices)

            fog_planes_bm.verts.ensure_lookup_table()
            fog_planes_bm.faces.ensure_lookup_table()

            material_list = []

            material_name = "+unused$"
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            for slot in fog_planes_object.material_slots:
                material_list.append(slot.material)

            if not mat in material_list:
                material_list.append(mat)
                fog_planes_object.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()

            fog_planes_bm.to_mesh(fog_planes_mesh)
            fog_planes_bm.free()

        #if len(LEVEL.weather_polyhedras) > 0:

    else:
        if len(LEVEL.clusters) > 0:
            material_count = len(LEVEL.materials)
            for cluster_idx, cluster in enumerate(LEVEL.clusters):
                cluster_name = "cluster_%s" % cluster_idx
                full_mesh = bpy.data.meshes.new(cluster_name)
                object_mesh = bpy.data.objects.new(cluster_name, full_mesh)
                object_mesh.parent = level_root
                bm = bmesh.new()
                for cluster_data in cluster.cluster_data:
                    triangles = get_triangle_info(cluster_data.parts, cluster_data.strip_indices)
                    vertices = [raw_vertex.position for raw_vertex in cluster_data.raw_vertices]

                    mesh = bpy.data.meshes.new("part")

                    mesh.from_pydata(vertices, [], triangles)
                    for poly in mesh.polygons:

                        poly.use_smooth = True

                    bm.from_mesh(mesh)
                    bpy.data.meshes.remove(mesh)

                    bm.to_mesh(full_mesh)
                    bm.free()

                    cluster_collection_override.objects.link(object_mesh)

        if len(LEVEL.cluster_portals) > 0:
            portal_bm = bmesh.new()
            portal_mesh = bpy.data.meshes.new("level_portals")
            portal_object = bpy.data.objects.new("level_portals", portal_mesh)
            collection.objects.link(portal_object)
            for cluster in LEVEL.clusters:
                for portal in cluster.portals:
                    vert_indices = []
                    cluster_portal = LEVEL.cluster_portals[portal]
                    for vertex in cluster_portal.vertices:
                        vert_indices.append(portal_bm.verts.new((vertex * 100)))

                    portal_bm.faces.new(vert_indices)

                portal_bm.verts.ensure_lookup_table()
                portal_bm.faces.ensure_lookup_table()

                for portal_idx, portal in enumerate(cluster.portals):
                    cluster_portal = LEVEL.cluster_portals[portal]
                    material_list = []

                    material_name = "+portal"
                    if ClusterPortalFlags.ai_cant_hear_through_this in ClusterPortalFlags(cluster_portal.flags):
                        material_name = "+portal&"

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in portal_object.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        portal_object.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    portal_bm.faces[portal_idx].material_index = material_index

            portal_bm.to_mesh(portal_mesh)
            portal_bm.free()

            mesh_processing.select_object(context, portal_object)
            mesh_processing.select_object(context, level_root)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            portal_object.select_set(False)
            level_root.select_set(False)

    for bsp_idx, bsp in enumerate(LEVEL.collision_bsps):
        collision_name = "level_collision"
        collision_bm = bmesh.new()

        collision_mesh = bpy.data.meshes.new(collision_name)
        collision_object = bpy.data.objects.new(collision_name, collision_mesh)
        collection.objects.link(collision_object)
        collision_object.hide_set(True)
        collision_object.hide_render = True
        for surface_idx, surface in enumerate(bsp.surfaces):
            edge_index = surface.first_edge
            surface_edges = []
            vert_indices = []
            while edge_index not in surface_edges:
                surface_edges.append(edge_index)
                edge = bsp.edges[edge_index]
                if edge.left_surface == surface_idx:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.start_vertex].translation))
                    edge_index = edge.forward_edge

                else:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.end_vertex].translation))
                    edge_index = edge.reverse_edge

            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if not is_invalid and len(vert_indices) >= 3:
                collision_bm.faces.new(vert_indices)

        collision_bm.verts.ensure_lookup_table()
        collision_bm.faces.ensure_lookup_table()
        surface_idx = 0
        for surface in bsp.surfaces:
            is_invalid = False
            if game_title == "halo2" and H2SurfaceFlags.invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if not is_invalid:
                ngon_material_index = surface.material
                if not ngon_material_index == -1:
                    mat = LEVEL.collision_materials[ngon_material_index]

                if not ngon_material_index == -1:
                    if game_title == "halo1":
                        shader = mat.shader_tag_ref
                    else:
                        shader = mat.new_shader

                    material_name = os.path.basename(shader.name)
                    if game_title == "halo1":
                        if H1SurfaceFlags.two_sided in H1SurfaceFlags(surface.flags):
                            material_name += "%"

                        if H1SurfaceFlags.invisible in H1SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H1SurfaceFlags.climbable in H1SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H1SurfaceFlags.breakable in H1SurfaceFlags(surface.flags):
                            material_name += "-"

                    else:
                        if H2SurfaceFlags.two_sided in H2SurfaceFlags(surface.flags):
                            material_name += "%"

                        if H2SurfaceFlags.invisible in H2SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H2SurfaceFlags.climbable in H2SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H2SurfaceFlags.breakable in H2SurfaceFlags(surface.flags):
                            material_name += "-"

                        if H2SurfaceFlags.conveyor in H2SurfaceFlags(surface.flags):
                            material_name += ">"

                else:
                    material_name = "+sky"

                material_list = []
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)
                    if not ngon_material_index == -1:
                        if game_title == "halo1":
                            mesh_processing.generate_shader(mat, shader, 0, tag_format, report)

                for slot in collision_object.material_slots:
                    material_list.append(slot.material)

                if not mat in material_list:
                    material_list.append(mat)
                    collision_object.data.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = material_list.index(mat)
                collision_bm.faces[surface_idx].material_index = material_index
                surface_idx += 1

        collision_bm.to_mesh(collision_mesh)
        collision_bm.free()

        collision_object.parent = level_root
