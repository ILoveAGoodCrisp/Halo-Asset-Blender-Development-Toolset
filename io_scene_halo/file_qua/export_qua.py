# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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


from decimal import *
from mathutils import Vector, Matrix
from math import degrees, atan, radians
from ..global_functions import global_functions

class QUAScene(global_functions.HaloAsset):
    class Scene:
        def __init__(self, version, name):
            self.version = version
            self.name = name

    class Units:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class Scenery:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class EffectsScenery:
        def __init__(self, name, path, bit_0, bit_1, bit_2):
            self.name = name
            self.path = path
            self.bit_0 = bit_0
            self.bit_1 = bit_1
            self.bit_2 = bit_2

    class Shots:
        def __init__(self, frames, audio_data):
            self.frames = frames
            self.audio_data = audio_data

    class ExtraShots:
        def __init__(self, frames, audio_data):
            self.frames = frames
            self.audio_data = audio_data

    class Frames:
        def __init__(self, position, up, forward, fov, aperture, focal_length, depth_of_field, near_focal, far_focal, focal_depth, blur_amount):
            self.position = position
            self.up = up
            self.forward = forward
            self.fov = fov
            self.aperture = aperture
            self.focal_length = focal_length
            self.depth_of_field = depth_of_field
            self.near_focal = near_focal
            self.far_focal = far_focal
            self.focal_depth = focal_depth
            self.blur_amount = blur_amount

    class AudioData:
        def __init__(self, filepath, frame, name):
            self.filepath = filepath
            self.frame = frame
            self.name = name

    def __init__(self, context, version):
        object_list = list(context.scene.objects)
        blend_filename = bpy.path.basename(context.blend_data.filepath)
        scene_name = 'default'
        if len(blend_filename) > 0:
            scene_name = blend_filename.rsplit('.', 1)[0]

        self.version = version
        self.name = scene_name
        self.shots = []
        self.units = []
        self.scenery = []
        self.effects_scenery = []
        self.extra_cameras = []
        self.extra_shots = []

        first_frame = context.scene.frame_start
        last_frame = context.scene.frame_end + 1
        total_frame_count = context.scene.frame_end - first_frame + 1

        ubercam = bpy.data.objects.get("ubercam")

        for shot in range(1):
            transforms_for_frame = []
            for frame in range(first_frame, last_frame):
                context.scene.frame_set(frame)

                camera_matrix = global_functions.get_matrix(ubercam, ubercam, False, None, None, False, version, 'QUA', False, 1)
                mesh_dimensions = global_functions.get_dimensions(camera_matrix, ubercam, version, None, False, False, 'QUA', 1)
                position = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

                up_vector = camera_matrix.to_quaternion() @ Vector((0, 1, 0))
                forward_vector = camera_matrix.to_quaternion() @ Vector((0, 0, -1))

                up = (up_vector[0], up_vector[1], up_vector[2])
                forward = (forward_vector[0], forward_vector[1], forward_vector[2])
                fov = degrees(2 * atan(ubercam.data.sensor_width /(2 * ubercam.data.lens)))
                aperture = ubercam.data.dof.aperture_ratio
                focal_length = ubercam.data.lens
                depth_of_field = int(ubercam.data.dof.use_dof)
                near_focal = ubercam.data.clip_start
                far_focal = ubercam.data.clip_end
                focal_depth = ubercam.data.dof.focus_distance
                blur_amount = ubercam.data.dof.aperture_fstop

                transforms_for_frame.append(QUAScene.Frames(position, up, forward, fov, aperture, focal_length, depth_of_field, near_focal, far_focal, focal_depth, blur_amount))

            self.shots.append(QUAScene.Shots(transforms_for_frame, []))


def write_file(context, filepath, report, version):
    decimal_1 = '\n%s'
    decimal_2 = '\n%s %s'
    decimal_3 = '\n%s %s %s'
    decimal_4 = '\n%s %s %s %s'

    qua_scene = QUAScene(context, int(version))

    file = open(filepath, 'w', encoding="utf-8")

    file.write(
        ';### VERSION ###' +
        '\n%s\n' % (qua_scene.version)
    )

    file.write(
        '\n;### SCENE ###' +
        '\n;      <scene name (string)>' +
        '\n%s\n' % (qua_scene.name)
    )

    file.write(
        '\n;### SHOTS ###' +
        '\n%s\n' % (len(qua_scene.shots))
    )

    file.write(
        '\n;### UNITS ###' +
        '\n%s' % (len(qua_scene.units)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, unit in enumerate(qua_scene.units):
        file.write(
            '\n; UNIT %s' % (idx) +
            '\n%s' % (unit.name) +
            '\n%s' % (unit.path) +
            '\n%s %s %s\n' % (unit.bit_0, unit.bit_1 ,unit.bit_2)
        )

    file.write(
        '\n;### SCENERY ###' +
        '\n%s' % (len(qua_scene.scenery)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, scenery in enumerate(qua_scene.scenery):
        file.write(
            '\n; SCENERY %s' % (idx) +
            '\n%s' % (scenery.name) +
            '\n%s' % (scenery.path) +
            '\n%s %s %s\n' % (scenery.bit_0, scenery.bit_1 ,scenery.bit_2)
        )

    file.write(
        '\n;### EFFECTS_SCENERY ###' +
        '\n%s' % (len(qua_scene.effects_scenery)) +
        '\n;      <export name (string)>' +
        '\n;      <export path (string)>' +
        '\n;      <shots visible (bit mask - sorta)>\n'
    )

    for idx, effect_scenery in enumerate(qua_scene.effects_scenery):
        file.write(
            '\n; EFFECTS_SCENERY %s' % (idx) +
            '\n%s' % (effect_scenery.name) +
            '\n%s' % (effect_scenery.path) +
            '\n%s %s %s\n' % (effect_scenery.bit_0, effect_scenery.bit_1 ,effect_scenery.bit_2)
        )

    for idx, shot in enumerate(qua_scene.shots):
        file.write(
            '\n; ### SHOT %s ###' % (idx) +
            '\n;          <Ubercam position (vector)>' +
            '\n;          <Ubercam up (vector)>' +
            '\n;          <Ubercam forward (vector)>' +
            '\n;          <Horizontal field of view (float)>' +
            '\n;          <Horizontal film aperture (float, millimeters)>' +
            '\n;          <Focal Length (float)>' +
            '\n;          <Depth of Field (bool)>' +
            '\n;          <Near Focal Plane Distance (float)>' +
            '\n;          <Far Focal Plane Distance (float)>' +
            '\n;          <Focal Depth (float)>' +
            '\n;          <Blur Amount (float)>' +
            '\n%s' % (len(shot.frames))
        )

        for idx, frame in enumerate(shot.frames):
            file.write(
                '\n; FRAME %s' % (idx) +
                decimal_3 % (frame.position) +
                decimal_3 % (frame.up) +
                decimal_3 % (frame.forward) +
                decimal_1 % (frame.fov) +
                decimal_1 % (frame.aperture) +
                decimal_1 % (frame.focal_length) +
                '\n%s' % (frame.depth_of_field) +
                decimal_1 % (frame.near_focal) +
                decimal_1 % (frame.far_focal) +
                decimal_1 % (frame.focal_depth) +
                decimal_1 % (frame.blur_amount) +
                '\n'
            )

        file.write(
            '\n;*** SHOT 1 AUDIO DATA ***' +
            '\n%s' % (len(shot.audio_data)) +
            '\n;          <Audio filename (string)>' +
            '\n;          <Frame number (int)>' +
            '\n;          <Character (string)>\n'
        )

        for idx, audio in enumerate(shot.audio_data):
            file.write(
                '\n; AUDIO %s' % (idx) +
                '\n%s' % (audio.filepath) +
                '\n%s' % (audio.frame) +
                '\n%s\n' % (audio.name)
            )

    file.write(
        '\n;### EXTRA CAMERAS ###' +
        '\n%s' % (len(qua_scene.extra_cameras)) +
        '\n;          <Camera name (string)>' +
        '\n;          <Camera type (string)>\n'
    )

    for idx, extra_camera in enumerate(qua_scene.extra_cameras):
        file.write(
            '\n;### CAMERA %s ###' % (idx) +
            '\n%s' % (extra_camera.name) +
            '\n%s\n' % (extra_camera.type)
        )

    for idx, extra_shot in enumerate(qua_scene.extra_shots):
        file.write(
            '\n; ### SHOT %s ###' % (idx) +
            '\n;          <Ubercam position (vector)>' +
            '\n;          <Ubercam up (vector)>' +
            '\n;          <Ubercam forward (vector)>' +
            '\n;          <Horizontal field of view (float)>' +
            '\n;          <Horizontal film aperture (float, millimeters)>' +
            '\n;          <Focal Length (float)>' +
            '\n;          <Depth of Field (bool)>' +
            '\n;          <Near Focal Plane Distance (float)>' +
            '\n;          <Far Focal Plane Distance (float)>' +
            '\n;          <Focal Depth (float)>' +
            '\n;          <Blur Amount (float)>' +
            '\n%s' % (len(extra_shot.frames))
        )

        for idx, frame in enumerate(extra_shot):
            file.write(
                '\n; FRAME %s' % (idx) +
                decimal_3 % (frame.position) +
                decimal_3 % (frame.up) +
                decimal_3 % (frame.forward) +
                decimal_1 % (frame.fov) +
                decimal_1 % (frame.aperture) +
                decimal_1 % (frame.focal_length) +
                '\n%s' % (frame.depth_of_field) +
                decimal_1 % (frame.near_focal) +
                decimal_1 % (frame.far_focal) +
                decimal_1 % (frame.focal_depth) +
                decimal_1 % (frame.blur_amount) +
                '\n'
            )

    file.close()
    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.qua()
