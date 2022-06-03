# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from mathutils import Vector, Euler

SALT_SIZE = 32

class ScenarioAsset():
    def __init__(self):
        self.header = None
        self.scenario_body_header = None
        self.scenario_body = None
        self.object_name_header = None
        self.object_names = None
        self.scenery_header = None
        self.scenery = None
        self.scenery_palette_header = None
        self.scenery_palette = None
        self.bipeds_header = None
        self.bipeds = None
        self.biped_palette_header = None
        self.biped_palette = None
        self.vehicles_header = None
        self.vehicles = None
        self.vehicle_palette_header = None
        self.vehicle_palette = None
        self.equipment_header = None
        self.equipment = None
        self.equipment_palette_header = None
        self.equipment_palette = None
        self.weapon_header = None
        self.weapons = None
        self.weapon_palette_header = None
        self.weapon_palette = None
        self.trigger_volumes_header = None
        self.trigger_volumes = None
        self.decals_header = None
        self.decals = None
        self.decal_palette_header = None
        self.decal_palette = None
        self.style_palette_header = None
        self.style_palette = None
        self.squad_groups_header = None
        self.squad_groups = None
        self.squads_header = None
        self.squads = None
        self.character_palette_header = None
        self.character_palette = None

    class ScenarioBody:
        def __init__(self, unused_tag_ref=None, skies_tag_block=None, scenario_type=0, scenario_flags=0, child_scenarios_tag_block=None, local_north=0.0, 
                     predicted_resources_tag_block=None, functions_tag_block=None, editor_scenario_data=0, comments_tag_block=None, environment_objects_tag_block=None, 
                     object_names_tag_block=None, scenery_tag_block=None, scenery_palette_tag_block=None, bipeds_tag_block=None, biped_palette_tag_block=None, 
                     vehicles_tag_block=None, vehicle_palette_tag_block=None, equipment_tag_block=None, equipment_palette_tag_block=None, weapons_tag_block=None, 
                     weapon_palette_tag_block=None, device_groups_tag_block=None, machines_tag_block=None, machine_palette_tag_block=None, controls_tag_block=None, 
                     control_palette_tag_block=None, light_fixtures_tag_block=None, light_fixtures_palette_tag_block=None, sound_scenery_tag_block=None, 
                     sound_scenery_palette_tag_block=None, light_volumes_tag_block=None, light_volume_palette_tag_block=None, player_starting_profile_tag_block=None, 
                     player_starting_locations_tag_block=None, trigger_volumes_tag_block=None, recorded_animations_tag_block=None, netgame_flags_tag_block=None, 
                     netgame_equipment_tag_block=None, starting_equipment_tag_block=None, bsp_switch_trigger_volumes_tag_block=None, decals_tag_block=None, 
                     decal_palette_tag_block=None, detail_object_collection_palette_tag_block=None, style_palette_tag_block=None, squad_groups_tag_block=None, 
                     squads_tag_block=None, zones_tag_block=None, mission_scenes_tag_block=None, character_palette_tag_block=None, ai_pathfinding_data_tag_block=None, 
                     ai_animation_references_tag_block=None, ai_script_references_tag_block=None, ai_recording_references_tag_block=None, ai_conversations_tag_block=None, 
                     script_syntax_data_tag_data=None, script_string_data_tag_data=None, scripts_tag_block=None, globals_tag_block=None, references_tag_block=None, 
                     source_files_tag_block=None, scripting_data_tag_block=None, cutscene_flags_tag_block=None, cutscene_camera_points_tag_block=None, 
                     cutscene_titles_tag_block=None, custom_object_names_tag_ref=None, chapter_title_text_tag_ref=None, hud_messages_tag_ref=None, 
                     structure_bsps_tag_block=None, scenario_resources_tag_block=None, old_structure_physics_tag_block=None, hs_unit_seats_tag_block=None, 
                     scenario_kill_triggers_tag_block=None, hs_syntax_datums_tag_block=None, orders_tag_block=None, triggers_tag_block=None, 
                     background_sound_palette_tag_block=None, sound_environment_palette_tag_block=None, weather_palette_tag_block=None, unused_0_tag_block=None, 
                     unused_1_tag_block=None, unused_2_tag_block=None, unused_3_tag_block=None, scavenger_hunt_objects_tag_block=None, scenario_cluster_data_tag_block=None, 
                     salt_array=None, spawn_data_tag_block=None, sound_effect_collection_tag_ref=None, crates_tag_block=None, crate_palette_tag_block=None, 
                     global_lighting_tag_ref=None, atmospheric_fog_palette_tag_block=None, planar_fog_palette_tag_block=None, flocks_tag_block=None, subtitles_tag_ref=None, 
                     decorators_tag_block=None, creatures_tag_block=None, creature_palette_tag_block=None, decorator_palette_tag_block=None, 
                     bsp_transition_volumes_tag_block=None, structure_bsp_lighting_tag_block=None, editor_folders_tag_block=None, level_data_tag_block=None, 
                     game_engine_strings_tag_ref=None, mission_dialogue_tag_block=None, objectives_tag_ref=None, interpolators_tag_block=None, shared_references_tag_block=None, 
                     screen_effect_references_tag_block=None, simulation_definition_table_tag_block=None):
            self.unused_tag_ref = unused_tag_ref
            self.skies_tag_block = skies_tag_block
            self.scenario_type = scenario_type
            self.scenario_flags = scenario_flags
            self.child_scenarios_tag_block = child_scenarios_tag_block
            self.local_north = local_north
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.functions_tag_block = functions_tag_block
            self.editor_scenario_data = editor_scenario_data
            self.comments_tag_block = comments_tag_block
            self.environment_objects_tag_block = environment_objects_tag_block
            self.object_names_tag_block = object_names_tag_block
            self.scenery_tag_block = scenery_tag_block
            self.scenery_palette_tag_block = scenery_palette_tag_block
            self.bipeds_tag_block = bipeds_tag_block
            self.biped_palette_tag_block = biped_palette_tag_block
            self.vehicles_tag_block = vehicles_tag_block
            self.vehicle_palette_tag_block = vehicle_palette_tag_block
            self.equipment_tag_block = equipment_tag_block
            self.equipment_palette_tag_block = equipment_palette_tag_block
            self.weapons_tag_block = weapons_tag_block
            self.weapon_palette_tag_block = weapon_palette_tag_block
            self.device_groups_tag_block = device_groups_tag_block
            self.machines_tag_block = machines_tag_block
            self.machine_palette_tag_block = machine_palette_tag_block
            self.controls_tag_block = controls_tag_block
            self.control_palette_tag_block = control_palette_tag_block
            self.light_fixtures_tag_block = light_fixtures_tag_block
            self.light_fixtures_palette_tag_block = light_fixtures_palette_tag_block
            self.sound_scenery_tag_block = sound_scenery_tag_block
            self.sound_scenery_palette_tag_block = sound_scenery_palette_tag_block
            self.light_volumes_tag_block = light_volumes_tag_block
            self.light_volume_palette_tag_block = light_volume_palette_tag_block
            self.player_starting_profile_tag_block = player_starting_profile_tag_block
            self.player_starting_locations_tag_block = player_starting_locations_tag_block
            self.trigger_volumes_tag_block = trigger_volumes_tag_block
            self.recorded_animations_tag_block = recorded_animations_tag_block
            self.netgame_flags_tag_block = netgame_flags_tag_block
            self.netgame_equipment_tag_block = netgame_equipment_tag_block
            self.starting_equipment_tag_block = starting_equipment_tag_block
            self.bsp_switch_trigger_volumes_tag_block = bsp_switch_trigger_volumes_tag_block
            self.decals_tag_block = decals_tag_block
            self.decal_palette_tag_block = decal_palette_tag_block
            self.detail_object_collection_palette_tag_block = detail_object_collection_palette_tag_block
            self.style_palette_tag_block = style_palette_tag_block
            self.squad_groups_tag_block = squad_groups_tag_block
            self.squads_tag_block = squads_tag_block
            self.zones_tag_block = zones_tag_block
            self.mission_scenes_tag_block = mission_scenes_tag_block
            self.character_palette_tag_block = character_palette_tag_block
            self.ai_pathfinding_data_tag_block = ai_pathfinding_data_tag_block
            self.ai_animation_references_tag_block = ai_animation_references_tag_block
            self.ai_script_references_tag_block = ai_script_references_tag_block
            self.ai_recording_references_tag_block = ai_recording_references_tag_block
            self.ai_conversations_tag_block = ai_conversations_tag_block
            self.script_syntax_data_tag_data = script_syntax_data_tag_data
            self.script_string_data_tag_data = script_string_data_tag_data
            self.scripts_tag_block = scripts_tag_block
            self.globals_tag_block = globals_tag_block
            self.references_tag_block = references_tag_block
            self.source_files_tag_block = source_files_tag_block
            self.scripting_data_tag_block = scripting_data_tag_block
            self.cutscene_flags_tag_block = cutscene_flags_tag_block
            self.cutscene_camera_points_tag_block = cutscene_camera_points_tag_block
            self.cutscene_titles_tag_block = cutscene_titles_tag_block
            self.custom_object_names_tag_ref = custom_object_names_tag_ref
            self.chapter_title_text_tag_ref = chapter_title_text_tag_ref
            self.hud_messages_tag_ref = hud_messages_tag_ref
            self.structure_bsps_tag_block = structure_bsps_tag_block
            self.scenario_resources_tag_block = scenario_resources_tag_block
            self.old_structure_physics_tag_block = old_structure_physics_tag_block
            self.hs_unit_seats_tag_block = hs_unit_seats_tag_block
            self.scenario_kill_triggers_tag_block = scenario_kill_triggers_tag_block
            self.hs_syntax_datums_tag_block = hs_syntax_datums_tag_block
            self.orders_tag_block = orders_tag_block
            self.triggers_tag_block = triggers_tag_block
            self.background_sound_palette_tag_block = background_sound_palette_tag_block
            self.sound_environment_palette_tag_block = sound_environment_palette_tag_block
            self.weather_palette_tag_block = weather_palette_tag_block
            self.unused_0_tag_block = unused_0_tag_block
            self.unused_1_tag_block = unused_1_tag_block
            self.unused_2_tag_block = unused_2_tag_block
            self.unused_3_tag_block = unused_3_tag_block
            self.scavenger_hunt_objects_tag_block = scavenger_hunt_objects_tag_block
            self.scenario_cluster_data_tag_block = scenario_cluster_data_tag_block
            self.salt_array = salt_array
            self.spawn_data_tag_block = spawn_data_tag_block
            self.sound_effect_collection_tag_ref = sound_effect_collection_tag_ref
            self.crates_tag_block = crates_tag_block
            self.crate_palette_tag_block = crate_palette_tag_block
            self.global_lighting_tag_ref = global_lighting_tag_ref
            self.atmospheric_fog_palette_tag_block = atmospheric_fog_palette_tag_block
            self.planar_fog_palette_tag_block = planar_fog_palette_tag_block
            self.flocks_tag_block = flocks_tag_block
            self.subtitles_tag_ref = subtitles_tag_ref
            self.decorators_tag_block = decorators_tag_block
            self.creatures_tag_block = creatures_tag_block
            self.creature_palette_tag_block = creature_palette_tag_block
            self.decorator_palette_tag_block = decorator_palette_tag_block
            self.bsp_transition_volumes_tag_block = bsp_transition_volumes_tag_block
            self.structure_bsp_lighting_tag_block = structure_bsp_lighting_tag_block
            self.editor_folders_tag_block = editor_folders_tag_block
            self.level_data_tag_block = level_data_tag_block
            self.game_engine_strings_tag_ref = game_engine_strings_tag_ref
            self.mission_dialogue_tag_block = mission_dialogue_tag_block
            self.objectives_tag_ref = objectives_tag_ref
            self.interpolators_tag_block = interpolators_tag_block
            self.shared_references_tag_block = shared_references_tag_block
            self.screen_effect_references_tag_block = screen_effect_references_tag_block
            self.simulation_definition_table_tag_block = simulation_definition_table_tag_block

    class ObjectName:
        def __init__(self, name="", object_type=0, placement_index=0):
            self.name = name
            self.object_type = object_type
            self.placement_index = placement_index

    class Object:
        def __init__(self, palette_index=0, name_index=0, placement_flags=0, position=Vector(), rotation=Euler(), scale=0.0, transform_flags=0, manual_bsp_flags=0, unique_id=0, 
                     origin_bsp_index=0, object_type=0, source=0, bsp_policy=0, editor_folder_index=0):
            self.palette_index = palette_index
            self.name_index = name_index
            self.placement_flags = placement_flags
            self.position = position
            self.rotation = rotation
            self.scale = scale
            self.transform_flags = transform_flags
            self.manual_bsp_flags = manual_bsp_flags
            self.unique_id = unique_id
            self.origin_bsp_index = origin_bsp_index
            self.object_type = object_type
            self.source = source
            self.bsp_policy = bsp_policy
            self.editor_folder_index = editor_folder_index

    class Scenery(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, sct3_header=None,variant_name_length=0, active_change_colors=0, primary_color_BGRA=(0.0, 0.0, 0.0, 1.0), 
                     secondary_color_BGRA=(0.0, 0.0, 0.0, 1.0), tertiary_color_BGRA=(0.0, 0.0, 0.0, 1.0), quaternary_color_BGRA=(0.0, 0.0, 0.0, 1.0), pathfinding_policy=0, 
                     lightmap_policy=0, valid_multiplayer_games=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.sct3_header = sct3_header
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.pathfinding_policy = pathfinding_policy
            self.lightmap_policy = lightmap_policy
            self.valid_multiplayer_games = valid_multiplayer_games

    class Unit(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, sunt_header=None,variant_name_length=0, active_change_colors=0, primary_color_BGRA=(0.0, 0.0, 0.0, 1.0), 
                     secondary_color_BGRA=(0.0, 0.0, 0.0, 1.0), tertiary_color_BGRA=(0.0, 0.0, 0.0, 1.0), quaternary_color_BGRA=(0.0, 0.0, 0.0, 1.0), body_vitality=0.0, 
                     flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.sunt_header = sunt_header
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.body_vitality = body_vitality
            self.flags = flags

    class Equipment(Object):
        def __init__(self, sobj_header=None, obj0_header=None, seqt_header=None, flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.seqt_header = seqt_header
            self.flags = flags

    class Weapon(Object):
        def __init__(self, sobj_header=None, obj0_header=None, sper_header=None, swpt_header=None, variant_name_length=0, active_change_colors=0, 
                     primary_color_BGRA=(0.0, 0.0, 0.0, 1.0), secondary_color_BGRA=(0.0, 0.0, 0.0, 1.0), tertiary_color_BGRA=(0.0, 0.0, 0.0, 1.0), 
                     quaternary_color_BGRA=(0.0, 0.0, 0.0, 1.0), rounds_left=0, rounds_loaded=0, flags=0):
            super().__init__()
            self.sobj_header = sobj_header
            self.obj0_header = obj0_header
            self.sper_header = sper_header
            self.swpt_header = swpt_header
            self.variant_name_length = variant_name_length
            self.active_change_colors = active_change_colors
            self.primary_color_BGRA = primary_color_BGRA
            self.secondary_color_BGRA = secondary_color_BGRA
            self.tertiary_color_BGRA = tertiary_color_BGRA
            self.quaternary_color_BGRA = quaternary_color_BGRA
            self.rounds_left = rounds_left
            self.rounds_loaded = rounds_loaded
            self.flags = flags

    class TriggerVolume():
        def __init__(self, name="", name_length=0, object_name_index=0, node_name="", node_name_length=0, forward=Vector(), up=Vector(), position=Vector(), extents=Vector(), 
                     kill_trigger_volume_index=0):
            self.name = name
            self.name_length = name_length
            self.object_name_index = object_name_index
            self.node_name = node_name
            self.node_name_length = node_name_length
            self.forward = forward
            self.up = up
            self.position = position
            self.extents = extents
            self.kill_trigger_volume_index = kill_trigger_volume_index

    class Decal():
        def __init__(self, palette_index=0, yaw=0, pitch=0, position=Vector()):
            self.palette_index = palette_index
            self.yaw = yaw
            self.pitch = pitch
            self.position = position

    class SquadGroups():
        def __init__(self, name="", parent_index=0, initial_order_index=0):
            self.name = name
            self.parent_index = parent_index
            self.initial_order_index = initial_order_index

    class Squad():
        def __init__(self, name="", flags=0, team=0, parent_squad_group_index=0, squad_delay_time=0.0, normal_difficulty_count=0, insane_difficulty_count=0, major_upgrade=0, 
                     vehicle_type_index=0, character_type_index=0, initial_zone_index=0, initial_weapon_index=0, initial_secondary_weapon_index=0, grenade_type=0, 
                     initial_order_index=0, vehicle_variant_length=0, starting_locations_tag_block=None, placement_script="", starting_locations_header=None, starting_locations=None):
            self.name = name
            self.flags = flags
            self.team = team
            self.parent_squad_group_index = parent_squad_group_index
            self.squad_delay_time = squad_delay_time
            self.normal_difficulty_count = normal_difficulty_count
            self.insane_difficulty_count = insane_difficulty_count
            self.major_upgrade = major_upgrade
            self.vehicle_type_index = vehicle_type_index
            self.character_type_index = character_type_index
            self.initial_zone_index = initial_zone_index
            self.initial_weapon_index = initial_weapon_index
            self.initial_secondary_weapon_index = initial_secondary_weapon_index
            self.grenade_type = grenade_type
            self.initial_order_index = initial_order_index
            self.vehicle_variant_length = vehicle_variant_length
            self.starting_locations_tag_block = starting_locations_tag_block
            self.placement_script = placement_script
            self.starting_locations_header = starting_locations_header
            self.starting_locations = starting_locations

    class StartingLocation():
        def __init__(self, name="", name_length=0, position=Vector(), reference_frame=0, facing_y=0.0, facing_p=0.0, flags=0, character_type_index=0, 
                     initial_weapon_index=0, initial_secondary_weapon_index=0, vehicle_type_index=0, seat_type=0, grenade_type=0, swarm_count=0, 
                     actor_variant_name_length=0, vehicle_variant_name_length=0, initial_movement_distance=0, emitter_vehicle_index=0, initial_movement_mode=0, 
                     placement_script=""):
            self.name = name
            self.name_length = name_length
            self.position = position
            self.reference_frame = reference_frame
            self.facing_y = facing_y
            self.facing_p = facing_p
            self.flags = flags
            self.character_type_index = character_type_index
            self.initial_weapon_index = initial_weapon_index
            self.initial_secondary_weapon_index = initial_secondary_weapon_index
            self.vehicle_type_index = vehicle_type_index
            self.seat_type = seat_type
            self.grenade_type = grenade_type
            self.swarm_count = swarm_count
            self.actor_variant_name_length = actor_variant_name_length
            self.vehicle_variant_name_length = vehicle_variant_name_length
            self.initial_movement_distance = initial_movement_distance
            self.emitter_vehicle_index = emitter_vehicle_index
            self.initial_movement_mode = initial_movement_mode
            self.placement_script = placement_script
