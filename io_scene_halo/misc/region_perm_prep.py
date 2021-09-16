# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

import bpy

def string_empty_check(string):
    is_empty = False
    if len(string) == 0:
        is_empty = True
    elif string.isspace():
        is_empty = True

    return is_empty

def create_facemap(permutation_string, region_string):
    active_object = bpy.context.view_layer.objects.active
    facemap_name = ""
    #This doesn't matter for CE but for Halo 2/3 the region or permutation names can't have any whitespace.
    #Lets fix that here to make sure nothing goes wrong.
    if not string_empty_check(permutation_string):
        facemap_name += permutation_string.replace(' ', '_').replace('\t', '_')

    if not string_empty_check(region_string):
        if not string_empty_check(facemap_name):
            facemap_name += " "

        facemap_name += region_string.replace(' ', '_').replace('\t', '_')

    if not string_empty_check(facemap_name):
        active_object.face_maps.new(name=facemap_name)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.scale_model()