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

from ..global_functions import tag_format, global_functions

from ..file_tag.file_scenario.h1.build_asset import build_asset as build_h1_scenario
from ..file_tag.file_scenario.h2.build_asset import build_asset as build_h2_scenario
from ..file_tag.file_shader.build_asset import build_asset as build_h2_shader
from ..file_tag.file_bitmap.h2.build_asset import build_asset as build_h2_bitmap
from ..file_tag.file_animation.h1.build_asset import build_asset as build_h1_animation
from ..file_tag.file_scenario.h1.upgrade_h2_scenario import upgrade_h2_scenario as upgrade_h1_h2_scenario
from ..file_tag.file_shader_environment.upgrade_h2_shader import upgrade_h2_shader as upgrade_h1_h2_shader
from ..file_tag.file_bitmap.h1.process_file_retail import process_file_retail as process_h1_bitmap
from ..file_tag.file_bitmap.h1.upgrade_h2_bitmap import upgrade_h2_bitmap as upgrade_h1_h2_bitmap
from ..file_tag.file_scenario.h1.process_file_retail import process_file_retail as process_h1_scenario
from ..file_tag.file_shader_environment.process_file_retail import process_file_retail as process_h1_shader
from ..file_tag.file_structure_bsp.h1.process_file_retail import process_file_retail as process_h1_structure_bsp
from ..file_tag.file_actor_variant.process_file_retail import process_file_retail as process_actor_variant
from ..file_tag.file_animation.h1.process_file_retail import process_file_retail as process_h1_animation_retail
from ..file_tag.file_animation.h1.animation_utilities import animation_rename
from ..file_tag.file_animation.h1.animation_utilities import animation_settings_transfer

from ..file_tag import import_tag

def convert_tag(context, input_file, source_game_title, target_game_title, patch_txt_path, report):
    path_basename = os.path.basename(input_file)
    path_dirname = os.path.dirname(input_file)
    filename_no_ext = path_basename.rsplit('.', 1)[0]
    file_path = os.path.join(path_dirname, filename_no_ext)
    input_stream = open(input_file, 'rb')
    if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
        input_stream.close()
        report({'ERROR'}, "File size does not meet the minimum amount required. File is either not a tag or corrupted")

        return {'CANCELLED'}

    is_big_endian = True
    if not source_game_title == "halo1":
        is_big_endian = False

    tag_group, group_is_valid = tag_format.check_group(input_stream, is_big_endian)
    if not group_is_valid:
        input_stream.close()
        report({'ERROR'}, "File does not have a valid tag class. Make sure you are importing a tag supported by the toolset")

        return {'CANCELLED'}

    if source_game_title == "halo1":
        if tag_group == "scnr":
            H1_ASSET = process_h1_scenario(input_stream, tag_format, report)

            if target_game_title == "halo2":
                output_stream = open(file_path + "_blender" + ".scenario", 'wb')

                H2_ASSET = upgrade_h1_h2_scenario(H1_ASSET, patch_txt_path, tag_format, report)
                build_h2_scenario(output_stream, H2_ASSET, tag_format, report)

                output_stream.close()

            else:
                input_stream.close()
                report({'ERROR'}, "Not implemented")

        elif tag_group == "senv":
            input_stream.close()
            if target_game_title == "halo2":
                shader_directory = os.path.dirname(file_path)
                output_path = os.path.join(shader_directory, "output")
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                for file_item in os.listdir(shader_directory):
                    input_file = os.path.join(shader_directory, file_item)
                    if os.path.isfile(input_file):
                        input_stream = open(input_file, 'rb')
                        if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
                            input_stream.close()
                            report({'ERROR'}, "File %s size does not meet the minimum amount required. File is either not a tag or corrupted" % file_item)

                            continue

                        tag_group, group_is_valid = tag_format.check_group(input_stream, is_big_endian)
                        if not group_is_valid:
                            input_stream.close()
                            report({'ERROR'}, "File %s does not have a valid tag class. Make sure you are importing a tag supported by the toolset" % file_item)

                            continue

                        if tag_group == "senv":
                            H1_ASSET = process_h1_shader(input_stream, tag_format, report)

                            file_name = file_item.rsplit('.', 1)[0].replace(" ", "_")
                            new_path = os.path.join(output_path, "%s.shader" % file_name)

                            output_stream = open(new_path, 'wb')

                            H2_ASSET = upgrade_h1_h2_shader(H1_ASSET, patch_txt_path, tag_format, report)
                            build_h2_shader(output_stream, tag_format, H2_ASSET, report)

                            output_stream.close()
                            input_stream.close()

            else:
                input_stream.close()
                report({'ERROR'}, "Not implemented")

        elif tag_group == "bitm":
            if target_game_title == "halo2":
                bitmap_directory = os.path.dirname(file_path)
                output_path = os.path.join(bitmap_directory, "output")
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                for file_item in os.listdir(bitmap_directory):
                    input_file = os.path.join(bitmap_directory, file_item)
                    if os.path.isfile(input_file):
                        input_stream = open(input_file, 'rb')
                        if tag_format.check_file_size(input_stream) < 64: # Size of the header for all tags
                            input_stream.close()
                            report({'ERROR'}, "File %s size does not meet the minimum amount required. File is either not a tag or corrupted" % file_item)

                            continue

                        tag_group, group_is_valid = tag_format.check_group(input_stream, is_big_endian)
                        if not group_is_valid:
                            input_stream.close()
                            report({'ERROR'}, "File %s does not have a valid tag header. Make sure you are importing a tag supported by the toolset" % file_item)

                            continue

                        if tag_group == "bitm":
                            input_file = os.path.join(bitmap_directory, file_item)
                            input_stream = open(input_file, 'rb')

                            H1_ASSET = process_h1_bitmap(input_stream, tag_format, report)

                            file_name = file_item.rsplit('.', 1)[0].replace(" ", "_")
                            new_path = os.path.join(output_path, "%s.bitmap" % file_name)

                            output_stream = open(new_path, 'wb')

                            H2_ASSET = upgrade_h1_h2_bitmap(H1_ASSET, patch_txt_path, tag_format, report)
                            build_h2_bitmap(output_stream, H2_ASSET, tag_format, report)

                            output_stream.close()
                            input_stream.close()

            else:
                input_stream.close()
                report({'ERROR'}, "Not implemented")

        elif tag_group == "actv":
            H1_ASSET = process_actor_variant(input_stream, tag_format, report)

        elif tag_group == "antr":
            H1_ASSET = process_h1_animation_retail(input_stream, global_functions, tag_format, report)
            if target_game_title == "halo1":
                output_path = os.path.join(path_dirname, "output")
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                output_stream = open(os.path.join(output_path, path_basename), 'wb')

                if "settings_transfer" in patch_txt_path:
                    donor_file = r""
                    donor_stream = open(donor_file, 'rb')
                    DONOR_TAG = process_h1_animation_retail(donor_stream, global_functions, tag_format, report)
                    H1_ASSET = animation_settings_transfer(H1_ASSET, DONOR_TAG, patch_txt_path, tag_format, report)

                else:
                    H1_ASSET = animation_rename(H1_ASSET, patch_txt_path, tag_format, report)

                build_h1_animation(output_stream, H1_ASSET, tag_format, report)

                output_stream.close()
                input_stream.close()

            else:
                input_stream.close()
                report({'ERROR'}, "Not implemented")

        else:
            input_stream.close()
            report({'ERROR'}, "Not implemented")

    else:
        input_stream.close()
        report({'ERROR'}, "Not implemented")

    return {'FINISHED'}