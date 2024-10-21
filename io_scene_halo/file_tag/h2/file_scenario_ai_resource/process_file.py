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
from ..file_scenario.format import ScenarioAsset

XML_OUTPUT = False

def read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENARIO.scenario_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.scenario_kill_triggers_tag_block = TAG.TagBlock()
    SCENARIO.scenario_body.style_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "style palette"))
    SCENARIO.scenario_body.squad_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "squad groups"))
    SCENARIO.scenario_body.squads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "squads"))
    SCENARIO.scenario_body.zones_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "zones"))
    SCENARIO.scenario_body.character_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "character palette"))
    SCENARIO.scenario_body.ai_animation_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai animation references"))
    SCENARIO.scenario_body.ai_script_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai script references"))
    SCENARIO.scenario_body.ai_recording_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai recording references"))
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai conversations"))
    SCENARIO.scenario_body.scripting_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scripting data"))
    SCENARIO.scenario_body.orders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "orders"))
    SCENARIO.scenario_body.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "triggers"))
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon palette"))
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles palette"))
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles"))
    SCENARIO.scenario_body.mission_scenes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "mission scenes"))
    SCENARIO.scenario_body.flocks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "flocks"))
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "trigger volumes"))

def read_vehicles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    process_scenario.palette_helper(input_stream, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "vehicles palette", SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette, tag_node, TAG)
    if SCENARIO.scenario_body.vehicles_tag_block.count > 0:
        SCENARIO.vehicles_header = TAG.TagBlockHeader().read(input_stream, TAG)
        vehicle_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.vehicles_tag_block.count, tag_node, "name", "vehicles")
        for vehicle_idx in range(SCENARIO.scenario_body.vehicles_tag_block.count):
            vehicle_element_node = None
            if XML_OUTPUT:
                vehicle_element_node = TAG.xml_doc.createElement('element')
                vehicle_element_node.setAttribute('index', str(vehicle_idx))
                vehicle_node.appendChild(vehicle_element_node)

            SCENARIO.vehicles.append(process_scenario.get_units(input_stream, SCENARIO, TAG, vehicle_element_node, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))

        for vehicle_idx, vehicle in enumerate(SCENARIO.vehicles):
            vehicle_element_node = None
            if XML_OUTPUT:
                vehicle_element_node = vehicle_node.childNodes[vehicle_idx]

            vehicle.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            vehicle.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            vehicle.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if vehicle.variant_name_length > 0:
                vehicle.variant_name = TAG.read_variable_string_no_terminator(input_stream, vehicle.variant_name_length, TAG, tag_format.XMLData(vehicle_element_node, "variant name"))

            vehicle.sunt_header = TAG.TagBlockHeader().read(input_stream, TAG)

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

    process_scenario.read_style_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_squad_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_squads(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_zones(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_character_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_ai_animation_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_ai_script_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_ai_recording_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_ai_conversations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_scripting_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_orders(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_triggers(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.palette_helper(input_stream, SCENARIO.scenario_body.weapon_palette_tag_block.count, "weapon palette", SCENARIO.weapon_palette_header, SCENARIO.weapon_palette, tag_node, TAG)
    read_vehicles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_mission_scenes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_flocks(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    process_scenario.read_trigger_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

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
