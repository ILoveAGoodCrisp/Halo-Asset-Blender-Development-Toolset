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

from ..file_scenario.h1.build_scene_retail import generate_scenario_scene as generate_h1_scenerio_retail
from ..file_scenario.h2.build_scene_retail import generate_scenario_scene as generate_h2_scenerio_retail

def build_scene(context, ASSET, game_version, game_title, version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format):
    if game_title == "halo1":
        generate_h1_scenerio_retail(context, ASSET, game_version, game_title, version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format)

    else:
        generate_h2_scenerio_retail(context, ASSET, game_version, game_title, version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format)
