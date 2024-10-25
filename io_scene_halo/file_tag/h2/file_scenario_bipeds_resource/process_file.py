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

from xml.dom import minidom
from ....global_functions import tag_format
from ..file_scenario import process_file as process_scenario
from .format import ScenarioAsset

XML_OUTPUT = False

def read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENARIO.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENARIO.skies_tag_block = TAG.TagBlock()
    SCENARIO.object_names_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object names"))
    SCENARIO.environment_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment objects"))
    SCENARIO.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))
    SCENARIO.biped_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bipeds palette"))
    SCENARIO.bipeds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bipeds"))
    SCENARIO.next_object_id_salt = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "next object id salt"))
    SCENARIO.editor_folders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor folders"))

def read_bipeds(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    process_scenario.palette_helper(input_stream, SCENARIO.biped_palette_tag_block.count, "bipeds palette", SCENARIO.biped_palette_header, SCENARIO.biped_palette, tag_node, TAG)
    if SCENARIO.bipeds_tag_block.count > 0:
        SCENARIO.bipeds_header = TAG.TagBlockHeader().read(input_stream, TAG)
        biped_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.bipeds_tag_block.count, tag_node, "name", "bipeds")
        for biped_idx in range(SCENARIO.bipeds_tag_block.count):
            biped_element_node = None
            if XML_OUTPUT:
                biped_element_node = TAG.xml_doc.createElement('element')
                biped_element_node.setAttribute('index', str(biped_idx))
                biped_node.appendChild(biped_element_node)

            SCENARIO.bipeds.append(process_scenario.get_units(input_stream, SCENARIO, TAG, biped_element_node, SCENARIO.biped_palette_tag_block.count, "scenario_biped_palette_block"))

        for biped_idx, biped in enumerate(SCENARIO.bipeds):
            biped_element_node = None
            if XML_OUTPUT:
                biped_element_node = biped_node.childNodes[biped_idx]

            biped.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            biped.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            biped.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if biped.variant_name_length > 0:
                biped.variant_name = TAG.read_variable_string_no_terminator(input_stream, biped.variant_name_length, TAG, tag_format.XMLData(biped_element_node, "variant name"))

            biped.sunt_header = TAG.TagBlockHeader().read(input_stream, TAG)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False
    TAG.big_endian = False
    tag_node = None
    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    process_scenario.initilize_scenario(SCENARIO)
    read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

    process_scenario.read_environment_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_object_names(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_bipeds(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_editor_folders(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENARIO.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENARIO
