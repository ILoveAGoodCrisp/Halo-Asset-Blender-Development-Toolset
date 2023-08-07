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

from .process_scene import process_scene
from ..global_functions.global_functions import get_directory, get_true_extension, ModelTypeEnum

DECIMAL_POINT = "6"
DECIMAL_1 = '\n%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_2 = '\n%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_3 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_4 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)

def write_header_16394(file, JMA):
    #write header
    file.write(
        '%s' % (JMA.version) +
        '\n%s' % (JMA.node_checksum) +
        '\n%s' % (JMA.frame_count) +
        '\n%s' % (JMA.frame_rate) +
        '\n%s' % (len(JMA.actor_names)) +
        '\n%s' % (JMA.actor_names[0]) +
        '\n%s' % (JMA.node_count)
        )

def write_header_16390(file, JMA):
    #write header
    file.write(
        '%s' % (JMA.version) +
        '\n%s' % (JMA.frame_count) +
        '\n%s' % (JMA.frame_rate) +
        '\n%s' % (len(JMA.actor_names)) +
        '\n%s' % (JMA.actor_names[0]) +
        '\n%s' % (JMA.node_count) +
        '\n%s' % (JMA.node_checksum)
        )

def write_nodes_16394(file, JMA):
    for node in JMA.nodes:
        file.write(
            '\n%s' % (node.name) +
            '\n%s' % (node.parent)
            )

def write_nodes_16392(file, JMA):
    for node in JMA.nodes:
        file.write(
            '\n%s' % (node.name) +
            '\n%s' % (node.child) +
            '\n%s' % (node.sibling)
            )

def write_nodes_16391(file, JMA):
    for node in JMA.nodes:
        file.write('\n%s' % (node.name))

def write_node_transforms_16390(file, JMA):
    #write transforms
    for node_transform in JMA.transforms:
        for node in node_transform:
            file.write(
                DECIMAL_3 % (node.translation[0], node.translation[1], node.translation[2]) +
                DECIMAL_4 % (node.rotation[0], node.rotation[1], node.rotation[2], node.rotation[3]) +
                DECIMAL_1 % (node.scale)
                )

def write_root_transforms_16395(file, JMA):
    #H2 specific biped controller data bool value.
    BIPED_CONTROLLER = False
    if len(JMA.biped_controller_transforms) > 0:
        BIPED_CONTROLLER = True

    file.write('\n%s' % (int(BIPED_CONTROLLER)))
    for biped_transform in JMA.biped_controller_transforms:
        file.write(
            DECIMAL_3 % (biped_transform.translation[0], biped_transform.translation[1], biped_transform.translation[2]) +
            DECIMAL_4 % (biped_transform.rotation[0], biped_transform.rotation[1], biped_transform.rotation[2], biped_transform.rotation[3]) +
            DECIMAL_1 % (biped_transform.scale)
            )

def update_decimal():
    global DECIMAL_POINT
    global DECIMAL_1
    global DECIMAL_2
    global DECIMAL_3
    global DECIMAL_4

    DECIMAL_POINT = "10"
    DECIMAL_1 = '\n%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_2 = '\n%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_3 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_4 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)

def build_asset(context, filepath, report, extension, jma_version, game_title, generate_checksum, folder_structure, fix_rotations, use_maya_sorting, frame_rate_value, scale_value):
    JMA = process_scene(context, extension, jma_version, game_title, generate_checksum, fix_rotations, use_maya_sorting, scale_value)
    JMA.version = jma_version
    JMA.frame_rate = frame_rate_value


    if jma_version >= 16395:
        update_decimal()

    filename = os.path.basename(filepath)

    root_directory = get_directory(context, game_title, ModelTypeEnum.animations, folder_structure, False, False, filepath)
    output_path = os.path.join(root_directory, "%s%s" % (filename, get_true_extension(filepath, extension, False)))
    file = open(output_path, 'w', encoding='utf_8')

    if jma_version >= 16395:
        write_header_16394(file, JMA)
        write_nodes_16394(file, JMA)
        write_node_transforms_16390(file, JMA)
        write_root_transforms_16395(file, JMA)

    elif jma_version == 16394:
        write_header_16394(file, JMA)
        write_nodes_16394(file, JMA)
        write_node_transforms_16390(file, JMA)

    elif jma_version >= 16392:
        write_header_16390(file, JMA)
        write_nodes_16392(file, JMA)
        write_node_transforms_16390(file, JMA)

    elif jma_version == 16391:
        write_header_16390(file, JMA)
        write_nodes_16391(file, JMA)
        write_node_transforms_16390(file, JMA)

    elif jma_version == 16390:
        write_header_16390(file, JMA)
        write_node_transforms_16390(file, JMA)

    file.write('\n')
    file.close()
