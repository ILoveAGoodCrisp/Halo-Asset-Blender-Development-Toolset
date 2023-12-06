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

from mathutils import Vector
from enum import Flag, Enum, auto

class ObjectFlags(Flag):
    does_not_cast_shadow = auto()
    search_cardinal_direction_lightmaps_on_failure = auto()
    unused = auto()
    not_a_pathfinding_obstacle = auto()
    extension_of_parent = auto()
    does_not_cause_collision_damage = auto()
    early_mover = auto()
    early_mover_localized_physics = auto()
    use_static_massive_lightmap_sample = auto()
    object_scales_attachments = auto()
    inherits_players_appearance = auto()
    dead_bipeds_cant_localize = auto()
    attach_to_clusters_dynamic_sphere = auto()
    effects_created_by_this_object_do_not_spawn_objects_in_multiplayer = auto()
    prophet_is_not_displayed_in_pegasus_builds = auto()

class LightmapShadowModeEnum(Enum):
    default = 0
    never = auto()
    always = auto()

class SweetenerSizeEnum(Enum):
    small = 0
    medium = auto()
    large = auto()

class ItemFlags(Flag):
    always_maintains_z_up = auto()
    destroyed_by_explosions = auto()
    unaffected_by_gravity = auto()

class PowerupTypeEnum(Enum):
    none = 0
    double_speed = auto()
    overshield = auto()
    active_camouflage = auto()
    full_spectrum_vision = auto()
    health = auto()
    grenade = auto()

class GrenadeTypeEnum(Enum):
    human_fragmentation = 0
    covenant_plasma = auto()

class EquipmentAsset():
    def __init__(self):
        self.header = None
        self.equipment_body_header = None
        self.equipment_body = None
        self.ai_properties_header = None
        self.ai_properties = None
        self.functions_header = None
        self.functions = None
        self.attachments_header = None
        self.attachments = None
        self.widgets_header = None
        self.widgets = None
        self.old_functions_header = None
        self.old_functions = None
        self.change_colors_header = None
        self.change_colors = None
        self.predicted_resources_header = None
        self.predicted_resources = None
        self.predicted_bitmaps_header = None
        self.predicted_bitmaps = None

    class EquipmentBody:
        def __init__(self, object_flags=0, bounding_radius=0.0, bounding_offset=Vector(), acceleration_scale=0.0, lightmap_shadow_mode=0, sweetner_size=0, 
                     dynamic_light_sphere_radius=0.0, dynamic_light_sphere_offset=Vector(), default_model_variant="", default_model_variant_length=0, model=None, crate_object=None, 
                     modifier_shader=None, creation_effect=None, material_effects=None, ai_properties_tag_block=None, functions_tag_block=None, apply_collision_damage_scale=0.0, 
                     min_game_acc=0.0, max_game_acc=0.0, min_game_scale=0.0, max_game_scale=0.0, min_abs_acc=0.0, max_abs_acc=0.0, min_abs_scale=0.0, max_abs_scale=0.0, 
                     hud_text_message_index=0, attachments_tag_block=None, widgets_tag_block=None, old_functions_tag_block=None, change_colors_tag_block=None, 
                     predicted_resources_tag_block=None, equipment_flags=0, old_message_index=0, sort_order=0, multiplayer_on_ground_scale=0.0, campaign_on_ground_scale=0.0, 
                     pickup_message="", pickup_message_length=0, swap_message="", swap_message_length=0, pickup_or_dual_message="", pickup_or_dual_message_length=0, 
                     swap_or_dual_message="", swap_or_dual_message_length=0, dual_only_message="", dual_only_message_length=0, picked_up_message="", picked_up_message_length=0, 
                     singluar_quantity_message="", singluar_quantity_message_length=0, plural_quantity_message="", plural_quantity_message_length=0, switch_to_message="", 
                     switch_to_message_length=0, switch_to_from_ai_message="", switch_to_from_ai_message_length=0, unused=None, collision_sound=None, 
                     predicted_bitmaps_tag_block=None, detonation_damage_effect=None, detonation_delay=(0.0, 0.0), detonating_effect=None, detonation_effect=None, powerup_type=0, 
                     grenade_type=0, powerup_time=0.0, pickup_sound=None):
            self.object_flags = object_flags
            self.bounding_radius = bounding_radius
            self.bounding_offset = bounding_offset
            self.acceleration_scale = acceleration_scale
            self.lightmap_shadow_mode = lightmap_shadow_mode
            self.sweetner_size = sweetner_size
            self.dynamic_light_sphere_radius = dynamic_light_sphere_radius
            self.dynamic_light_sphere_offset = dynamic_light_sphere_offset
            self.default_model_variant = default_model_variant
            self.default_model_variant_length = default_model_variant_length
            self.model = model
            self.crate_object = crate_object
            self.modifier_shader = modifier_shader
            self.creation_effect = creation_effect
            self.material_effects = material_effects
            self.ai_properties_tag_block = ai_properties_tag_block
            self.functions_tag_block = functions_tag_block
            self.apply_collision_damage_scale = apply_collision_damage_scale
            self.min_game_acc = min_game_acc
            self.max_game_acc = max_game_acc
            self.min_game_scale = min_game_scale
            self.max_game_scale = max_game_scale
            self.min_abs_acc = min_abs_acc
            self.max_abs_acc = max_abs_acc
            self.min_abs_scale = min_abs_scale
            self.max_abs_scale = max_abs_scale
            self.hud_text_message_index = hud_text_message_index
            self.attachments_tag_block = attachments_tag_block
            self.widgets_tag_block = widgets_tag_block
            self.old_functions_tag_block = old_functions_tag_block
            self.change_colors_tag_block = change_colors_tag_block
            self.predicted_resources_tag_block = predicted_resources_tag_block
            self.equipment_flags = equipment_flags
            self.old_message_index = old_message_index
            self.sort_order = sort_order
            self.multiplayer_on_ground_scale = multiplayer_on_ground_scale
            self.campaign_on_ground_scale = campaign_on_ground_scale
            self.pickup_message = pickup_message
            self.pickup_message_length = pickup_message_length
            self.swap_message = swap_message
            self.swap_message_length = swap_message_length
            self.pickup_or_dual_message = pickup_or_dual_message
            self.pickup_or_dual_message_length = pickup_or_dual_message_length
            self.swap_or_dual_message = swap_or_dual_message
            self.swap_or_dual_message_length = swap_or_dual_message_length
            self.dual_only_message = dual_only_message
            self.dual_only_message_length = dual_only_message_length
            self.picked_up_message = picked_up_message
            self.picked_up_message_length = picked_up_message_length
            self.singluar_quantity_message = singluar_quantity_message
            self.singluar_quantity_message_length = singluar_quantity_message_length
            self.plural_quantity_message = plural_quantity_message
            self.plural_quantity_message_length = plural_quantity_message_length
            self.switch_to_message = switch_to_message
            self.switch_to_message_length = switch_to_message_length
            self.switch_to_from_ai_message = switch_to_from_ai_message
            self.switch_to_from_ai_message_length = switch_to_from_ai_message_length
            self.unused = unused
            self.collision_sound = collision_sound
            self.predicted_bitmaps_tag_block = predicted_bitmaps_tag_block
            self.detonation_damage_effect = detonation_damage_effect
            self.detonation_delay = detonation_delay
            self.detonating_effect = detonating_effect
            self.detonation_effect = detonation_effect
            self.powerup_type = powerup_type
            self.grenade_type = grenade_type
            self.powerup_time = powerup_time
            self.pickup_sound = pickup_sound
