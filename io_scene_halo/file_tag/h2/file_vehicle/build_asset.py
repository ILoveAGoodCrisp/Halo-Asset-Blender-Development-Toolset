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

import struct

from math import radians
from ....global_functions import tag_format, shader_processing
from ....file_tag.h2.file_shader.format import FunctionTypeEnum
from ..file_object.build_asset import (
    write_ai_properties,
    write_functions,
    write_attachments,
    write_tag_ref,
    write_old_functions,
    write_change_colors,
    write_predicted_resources
    )
from ..file_unit.build_asset import (
    write_postures,
    write_dialogue_variant,
    write_powered_seats,
    write_seats
    )

def write_body(output_stream, TAG, VEHICLE):
    VEHICLE.vehicle_body_header.write(output_stream, TAG, True)
    output_stream.write(struct.pack('<H', 1))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.object_flags))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.bounding_radius))
    output_stream.write(struct.pack('<fff', *VEHICLE.vehicle_body.bounding_offset))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.acceleration_scale))
    output_stream.write(struct.pack('<h', VEHICLE.vehicle_body.lightmap_shadow_mode))
    output_stream.write(struct.pack('<h', VEHICLE.vehicle_body.sweetner_size))
    output_stream.write(struct.pack('<4x'))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.dynamic_light_sphere_radius))
    output_stream.write(struct.pack('<fff', *VEHICLE.vehicle_body.dynamic_light_sphere_offset))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.default_model_variant)))
    VEHICLE.vehicle_body.model.write(output_stream, False, True)
    VEHICLE.vehicle_body.crate_object.write(output_stream, False, True)
    VEHICLE.vehicle_body.modifier_shader.write(output_stream, False, True)
    VEHICLE.vehicle_body.creation_effect.write(output_stream, False, True)
    VEHICLE.vehicle_body.material_effects.write(output_stream, False, True)
    VEHICLE.vehicle_body.ai_properties_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.functions_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.apply_collision_damage_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.min_game_acc))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.max_game_acc))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.min_game_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.max_game_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.min_abs_acc))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.max_abs_acc))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.min_abs_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.max_abs_scale))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.hud_text_message_index))
    output_stream.write(struct.pack('<2x'))
    VEHICLE.vehicle_body.attachments_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.widgets_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.old_functions_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.change_colors_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.predicted_resources_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<I', VEHICLE.vehicle_body.unit_flags))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.default_team))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.constant_sound_volume))
    VEHICLE.vehicle_body.integrated_light_toggle.write(output_stream, False, True)
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.camera_field_of_view)))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.camera_stiffness))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.camera_marker_name)))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.camera_submerged_marker_name)))
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.pitch_auto_level)))
    output_stream.write(struct.pack('<ff', radians(VEHICLE.vehicle_body.pitch_range[0]), radians(VEHICLE.vehicle_body.pitch_range[1])))
    VEHICLE.vehicle_body.camera_tracks_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<fff', *VEHICLE.vehicle_body.acceleration_range))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.acceleration_action_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.acceleration_attach_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.soft_ping_threshold))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.soft_ping_interrupt_time))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.hard_ping_threshold))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.hard_ping_interrupt_time))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.hard_death_threshold))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.feign_death_threshold))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.feign_death_time))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.distance_of_evade_anim))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.distance_of_dive_anim))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.stunned_movement_threshold))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.feign_death_chance))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.feign_repeat_chance))
    VEHICLE.vehicle_body.spawned_turret_actor.write(output_stream, False, True)
    output_stream.write(struct.pack('<hh', *VEHICLE.vehicle_body.spawned_actor_count))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.spawned_velocity))
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.aiming_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.aiming_acceleration_maximum)))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.casual_aiming_modifier))
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.looking_velocity_maximum)))
    output_stream.write(struct.pack('<f', radians(VEHICLE.vehicle_body.looking_acceleration_maximum)))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.right_hand_node)))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.left_hand_node)))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.preferred_gun_node)))
    VEHICLE.vehicle_body.melee_damage.write(output_stream, False, True)
    VEHICLE.vehicle_body.boarding_melee_damage.write(output_stream, False, True)
    VEHICLE.vehicle_body.boarding_melee_response.write(output_stream, False, True)
    VEHICLE.vehicle_body.landing_melee_damage.write(output_stream, False, True)
    VEHICLE.vehicle_body.flurry_melee_damage.write(output_stream, False, True)
    VEHICLE.vehicle_body.obstacle_smash_damage.write(output_stream, False, True)
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.motion_sensor_blip_size))
    output_stream.write(struct.pack('<B', VEHICLE.vehicle_body.unit_type))
    output_stream.write(struct.pack('<B', VEHICLE.vehicle_body.unit_class))
    VEHICLE.vehicle_body.postures_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.new_hud_interfaces_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.dialogue_variants_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.grenade_velocity))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.grenade_type))
    output_stream.write(struct.pack('<h', VEHICLE.vehicle_body.grenade_count))
    VEHICLE.vehicle_body.powered_seats_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.weapons_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.seats_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.boost_peak_power))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.boost_rise_power))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.boost_peak_time))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.boost_fall_power))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.dead_time))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.attack_weight))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.decay_weight))
    output_stream.write(struct.pack('<I', VEHICLE.vehicle_body.vehicle_flags))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.vehicle_type))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.vehicle_control))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_forward_speed))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_reverse_speed))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.speed_acceleration))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.speed_deceleration))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_left_turn))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_right_turn))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.wheel_circumference))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.turn_rate))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.blur_speed))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.specific_type))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.player_training_vehicle_type))
    output_stream.write(struct.pack('>I', len(VEHICLE.vehicle_body.flip_message)))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.turn_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.speed_turn_penalty_power))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.speed_turn_penalty))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_left_slide))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_right_slide))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.slide_acceleration))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.slide_deceleration))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.minimum_flipping_angular_velocity))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.maximum_flipping_angular_velocity))
    output_stream.write(struct.pack('<H', VEHICLE.vehicle_body.vehicle_size))
    output_stream.write(struct.pack('<2x'))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.fixed_gun_yaw))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.fixed_gun_pitch))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.overdampen_cusp_angle))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.overdampen_exponent))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.crouch_transition_time))
    output_stream.write(struct.pack('<f', 1000))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.engine_moment))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.engine_max_angular_velocity))
    VEHICLE.vehicle_body.gears_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.flying_torque_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.seat_enterance_acceleration_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.seat_exit_acceleration_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.air_friction_deceleration))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.thrust_scale))
    VEHICLE.vehicle_body.suspension_sound.write(output_stream, False, True)
    VEHICLE.vehicle_body.crash_sound.write(output_stream, False, True)
    VEHICLE.vehicle_body.unused.write(output_stream, False, True)
    VEHICLE.vehicle_body.special_effect.write(output_stream, False, True)
    VEHICLE.vehicle_body.unused_effect.write(output_stream, False, True)
    output_stream.write(struct.pack('<I', VEHICLE.vehicle_body.physics_flags))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_fricton))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_depth))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_damp_factor))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_moving_friction))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_maximum_slope_0))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.ground_maximum_slope_1))
    output_stream.write(struct.pack('<16x'))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.anti_gravity_bank_lift))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.steering_bank_reaction_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.gravity_scale))
    output_stream.write(struct.pack('<f', VEHICLE.vehicle_body.radius))
    VEHICLE.vehicle_body.anti_gravity_point_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.friction_points_tag_block.write(output_stream, False)
    VEHICLE.vehicle_body.phantom_shapes_tag_block.write(output_stream, False)

def write_gears(output_stream, TAG, gears, gears_header):
    if len(gears) > 0:
        gears_header.write(output_stream, TAG, True)
        for gear_element in gears:
            output_stream.write(struct.pack('<f', gear_element.a_min_torque))
            output_stream.write(struct.pack('<f', gear_element.a_max_torque))
            output_stream.write(struct.pack('<f', gear_element.a_peak_torque_scale))
            output_stream.write(struct.pack('<f', gear_element.a_past_peak_torque_exponent))
            output_stream.write(struct.pack('<f', gear_element.a_torque_at_max_angular_velocity))
            output_stream.write(struct.pack('<f', gear_element.a_torque_at_2x_max_angular_velocity))
            output_stream.write(struct.pack('<f', gear_element.b_min_torque))
            output_stream.write(struct.pack('<f', gear_element.b_max_torque))
            output_stream.write(struct.pack('<f', gear_element.b_peak_torque_scale))
            output_stream.write(struct.pack('<f', gear_element.b_past_peak_torque_exponent))
            output_stream.write(struct.pack('<f', gear_element.b_torque_at_max_angular_velocity))
            output_stream.write(struct.pack('<f', gear_element.b_torque_at_2x_max_angular_velocity))
            output_stream.write(struct.pack('<f', gear_element.min_time_to_upshift))
            output_stream.write(struct.pack('<f', gear_element.engine_up_shift_scale))
            output_stream.write(struct.pack('<f', gear_element.gear_ratio))
            output_stream.write(struct.pack('<f', gear_element.min_time_to_downshift))
            output_stream.write(struct.pack('<f', gear_element.engine_down_shift_scale))

        for gear_element in gears:
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("trcv", True), 0, 1, 24))
            output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("trcv", True), 0, 1, 24))

def write_anti_gravity_point(output_stream, TAG, anti_gravity_point, anti_gravity_point_header):
    if len(anti_gravity_point) > 0:
        anti_gravity_point_header.write(output_stream, TAG, True)
        for anti_gravity_point_element in anti_gravity_point:
            output_stream.write(struct.pack('>I', len(anti_gravity_point_element.marker_name)))
            output_stream.write(struct.pack('<I', anti_gravity_point_element.flags))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_strength))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_offset))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_height))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_damp_factor))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_normal_k1))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.antigrav_normal_k0))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.radius))
            output_stream.write(struct.pack('<16x'))
            output_stream.write(struct.pack('>I', len(anti_gravity_point_element.damage_source_region_name)))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.default_state_error))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.minor_damage_error))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.medium_damage_error))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.major_damage_error))
            output_stream.write(struct.pack('<f', anti_gravity_point_element.destroyed_state_error))

        for anti_gravity_point_element in anti_gravity_point:
            marker_name_length = len(anti_gravity_point_element.marker_name)
            if marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % marker_name_length, TAG.string_to_bytes(anti_gravity_point_element.marker_name, False)))

            damage_source_region_name_length = len(anti_gravity_point_element.damage_source_region_name)
            if damage_source_region_name_length > 0:
                output_stream.write(struct.pack('<%ss' % damage_source_region_name_length, TAG.string_to_bytes(anti_gravity_point_element.damage_source_region_name, False)))

def write_friction_points(output_stream, TAG, friction_points, friction_points_header):
    if len(friction_points) > 0:
        friction_points_header.write(output_stream, TAG, True)
        for friction_point_element in friction_points:
            output_stream.write(struct.pack('>I', len(friction_point_element.marker_name)))
            output_stream.write(struct.pack('<I', friction_point_element.flags))
            output_stream.write(struct.pack('<f', friction_point_element.fraction_of_total_mass))
            output_stream.write(struct.pack('<f', friction_point_element.radius))
            output_stream.write(struct.pack('<f', friction_point_element.damaged_radius))
            output_stream.write(struct.pack('<H', friction_point_element.friction_type))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<f', friction_point_element.moving_friction_velocity_diff))
            output_stream.write(struct.pack('<f', friction_point_element.e_brake_moving_friction))
            output_stream.write(struct.pack('<f', friction_point_element.e_brake_friction))
            output_stream.write(struct.pack('<f', friction_point_element.e_brake_moving_friction_vel_dif))
            output_stream.write(struct.pack('<20x'))
            output_stream.write(struct.pack('>I', len(friction_point_element.collision_global_material_name)))
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<H', friction_point_element.model_state_destroyed))
            output_stream.write(struct.pack('>I', len(friction_point_element.region_name)))
            output_stream.write(struct.pack('<4x'))

        for friction_point_element in friction_points:
            marker_name_length = len(friction_point_element.marker_name)
            if marker_name_length > 0:
                output_stream.write(struct.pack('<%ss' % marker_name_length, TAG.string_to_bytes(friction_point_element.marker_name, False)))

            collision_global_material_name_length = len(friction_point_element.collision_global_material_name)
            if collision_global_material_name_length > 0:
                output_stream.write(struct.pack('<%ss' % collision_global_material_name_length, TAG.string_to_bytes(friction_point_element.collision_global_material_name, False)))

            region_name_length = len(friction_point_element.region_name)
            if region_name_length > 0:
                output_stream.write(struct.pack('<%ss' % region_name_length, TAG.string_to_bytes(friction_point_element.region_name, False)))

def write_phantom_shapes(output_stream, TAG, phantom_shapes, phantom_shapes_header):
    if len(phantom_shapes) > 0:
        phantom_shapes_header.write(output_stream, TAG, True)
        for phantom_shape_element in phantom_shapes:
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', phantom_shape_element.size))
            output_stream.write(struct.pack('<h', phantom_shape_element.count))
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('<i', phantom_shape_element.child_shapes_size))
            output_stream.write(struct.pack('<i', phantom_shape_element.child_shapes_capacity))
            output_stream.write(struct.pack('<32x'))
            output_stream.write(struct.pack('<i', phantom_shape_element.multisphere_count))
            output_stream.write(struct.pack('<I', phantom_shape_element.flags))
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('<f', phantom_shape_element.x0))
            output_stream.write(struct.pack('<f', phantom_shape_element.x1))
            output_stream.write(struct.pack('<f', phantom_shape_element.y0))
            output_stream.write(struct.pack('<f', phantom_shape_element.y1))
            output_stream.write(struct.pack('<f', phantom_shape_element.z0))
            output_stream.write(struct.pack('<f', phantom_shape_element.z1))
            for sphere_element in phantom_shape_element.spheres:
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<h', sphere_element.size))
                output_stream.write(struct.pack('<h', sphere_element.count))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<i', sphere_element.num_spheres))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_0))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_1))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_2))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_3))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_4))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_5))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_6))
                output_stream.write(struct.pack('<4x'))
                output_stream.write(struct.pack('<fff', *sphere_element.sphere_7))
                output_stream.write(struct.pack('<4x'))

def build_asset(output_stream, VEHICLE, report):
    TAG = tag_format.TagAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    VEHICLE.header.write(output_stream, False, True)
    write_body(output_stream, TAG, VEHICLE)

    default_model_variant_name_length = len(VEHICLE.vehicle_body.default_model_variant)
    if default_model_variant_name_length > 0:
        output_stream.write(struct.pack('<%ss' % default_model_variant_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.default_model_variant, False)))

    model_name_length = len(VEHICLE.vehicle_body.model.name)
    if model_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % model_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.model.name, False)))

    crate_object_name_length = len(VEHICLE.vehicle_body.crate_object.name)
    if crate_object_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % crate_object_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.crate_object.name, False)))

    modifier_shader_name_length = len(VEHICLE.vehicle_body.modifier_shader.name)
    if modifier_shader_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % modifier_shader_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.modifier_shader.name, False)))

    creation_effect_name_length = len(VEHICLE.vehicle_body.creation_effect.name)
    if creation_effect_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % creation_effect_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.creation_effect.name, False)))

    material_effects_name_length = len(VEHICLE.vehicle_body.material_effects.name)
    if material_effects_name_length > 0:
        output_stream.write(struct.pack('<%ssx' % material_effects_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.material_effects.name, False)))

    write_ai_properties(output_stream, TAG, VEHICLE.ai_properties, VEHICLE.ai_properties_header)
    write_functions(output_stream, TAG, VEHICLE.functions, VEHICLE.functions_header)
    write_attachments(output_stream, TAG, VEHICLE.attachments, VEHICLE.attachments_header)
    write_tag_ref(output_stream, TAG, VEHICLE.widgets, VEHICLE.widgets_header)
    write_old_functions(output_stream, TAG, VEHICLE.old_functions, VEHICLE.old_functions_header)
    write_change_colors(output_stream, TAG, VEHICLE.change_colors, VEHICLE.change_colors_header)
    write_predicted_resources(output_stream, TAG, VEHICLE.predicted_resources, VEHICLE.predicted_resources_header)

    integrated_light_toggle_length = len(VEHICLE.vehicle_body.integrated_light_toggle.name)
    if integrated_light_toggle_length > 0:
        output_stream.write(struct.pack('<%ssx' % integrated_light_toggle_length, TAG.string_to_bytes(VEHICLE.vehicle_body.integrated_light_toggle.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uncs", True), 0, 1, 32))

    camera_marker_name_length = len(VEHICLE.vehicle_body.camera_marker_name)
    if camera_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_marker_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.camera_marker_name, False)))

    camera_submerged_marker_name_length = len(VEHICLE.vehicle_body.camera_submerged_marker_name)
    if camera_submerged_marker_name_length > 0:
        output_stream.write(struct.pack('<%ss' % camera_submerged_marker_name_length, TAG.string_to_bytes(VEHICLE.vehicle_body.camera_submerged_marker_name, False)))

    write_tag_ref(output_stream, TAG, VEHICLE.camera_tracks, VEHICLE.camera_tracks_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("usas", True), 0, 1, 20))

    spawned_turret_actor_length = len(VEHICLE.vehicle_body.spawned_turret_actor.name)
    if spawned_turret_actor_length > 0:
        output_stream.write(struct.pack('<%ssx' % spawned_turret_actor_length, TAG.string_to_bytes(VEHICLE.vehicle_body.spawned_turret_actor.name, False)))

    right_hand_node_length = len(VEHICLE.vehicle_body.right_hand_node)
    if right_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % right_hand_node_length, TAG.string_to_bytes(VEHICLE.vehicle_body.right_hand_node, False)))

    left_hand_node_length = len(VEHICLE.vehicle_body.left_hand_node)
    if left_hand_node_length > 0:
        output_stream.write(struct.pack('<%ss' % left_hand_node_length, TAG.string_to_bytes(VEHICLE.vehicle_body.left_hand_node, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("uHnd", True), 1, 1, 4))

    preferred_gun_node_length = len(VEHICLE.vehicle_body.preferred_gun_node)
    if preferred_gun_node_length > 0:
        output_stream.write(struct.pack('<%ss' % preferred_gun_node_length, TAG.string_to_bytes(VEHICLE.vehicle_body.preferred_gun_node, False)))

    melee_damage_length = len(VEHICLE.vehicle_body.melee_damage.name)
    if melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % melee_damage_length, TAG.string_to_bytes(VEHICLE.vehicle_body.melee_damage.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("ubms", True), 1, 1, 80))

    boarding_melee_damage_length = len(VEHICLE.vehicle_body.boarding_melee_damage.name)
    if boarding_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_damage_length, TAG.string_to_bytes(VEHICLE.vehicle_body.boarding_melee_damage.name, False)))

    boarding_melee_response_length = len(VEHICLE.vehicle_body.boarding_melee_response.name)
    if boarding_melee_response_length > 0:
        output_stream.write(struct.pack('<%ssx' % boarding_melee_response_length, TAG.string_to_bytes(VEHICLE.vehicle_body.boarding_melee_response.name, False)))

    landing_melee_damage_length = len(VEHICLE.vehicle_body.landing_melee_damage.name)
    if landing_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % landing_melee_damage_length, TAG.string_to_bytes(VEHICLE.vehicle_body.landing_melee_damage.name, False)))

    flurry_melee_damage_length = len(VEHICLE.vehicle_body.flurry_melee_damage.name)
    if flurry_melee_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % flurry_melee_damage_length, TAG.string_to_bytes(VEHICLE.vehicle_body.flurry_melee_damage.name, False)))

    obstacle_smash_damage_length = len(VEHICLE.vehicle_body.obstacle_smash_damage.name)
    if obstacle_smash_damage_length > 0:
        output_stream.write(struct.pack('<%ssx' % obstacle_smash_damage_length, TAG.string_to_bytes(VEHICLE.vehicle_body.obstacle_smash_damage.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("cmtb", True), 0, 1, 2))

    write_postures(output_stream, TAG, VEHICLE.postures, VEHICLE.postures_header)
    write_tag_ref(output_stream, TAG, VEHICLE.new_hud_interface, VEHICLE.new_hud_interface_header)
    write_dialogue_variant(output_stream, TAG, VEHICLE.dialogue_variants, VEHICLE.dialogue_variants_header)
    write_powered_seats(output_stream, TAG, VEHICLE.powered_seats, VEHICLE.powered_seats_header)
    write_tag_ref(output_stream, TAG, VEHICLE.weapons, VEHICLE.weapons_header)
    write_seats(output_stream, TAG, VEHICLE.seats, VEHICLE.seats_header)

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("!@#$", True), 0, 1, 20))
    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("ulYc", True), 1, 1, 8))

    flip_message_length = len(VEHICLE.vehicle_body.flip_message)
    if flip_message_length > 0:
        output_stream.write(struct.pack('<%ss' % flip_message_length, TAG.string_to_bytes(VEHICLE.vehicle_body.flip_message, False)))

    write_gears(output_stream, TAG, VEHICLE.gears, VEHICLE.gears_header)

    suspension_sound_length = len(VEHICLE.vehicle_body.suspension_sound.name)
    if suspension_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % suspension_sound_length, TAG.string_to_bytes(VEHICLE.vehicle_body.suspension_sound.name, False)))

    crash_sound_length = len(VEHICLE.vehicle_body.crash_sound.name)
    if crash_sound_length > 0:
        output_stream.write(struct.pack('<%ssx' % crash_sound_length, TAG.string_to_bytes(VEHICLE.vehicle_body.crash_sound.name, False)))

    unused_length = len(VEHICLE.vehicle_body.unused.name)
    if unused_length > 0:
        output_stream.write(struct.pack('<%ssx' % unused_length, TAG.string_to_bytes(VEHICLE.vehicle_body.unused.name, False)))

    special_effect_length = len(VEHICLE.vehicle_body.special_effect.name)
    if special_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % special_effect_length, TAG.string_to_bytes(VEHICLE.vehicle_body.special_effect.name, False)))

    unused_effect_length = len(VEHICLE.vehicle_body.unused_effect.name)
    if unused_effect_length > 0:
        output_stream.write(struct.pack('<%ssx' % unused_effect_length, TAG.string_to_bytes(VEHICLE.vehicle_body.unused_effect.name, False)))

    output_stream.write(struct.pack('<4s3I', TAG.string_to_bytes("HVPH", True), 0, 1, 96))

    write_anti_gravity_point(output_stream, TAG, VEHICLE.anti_gravity_point, VEHICLE.anti_gravity_point_header)
    write_friction_points(output_stream, TAG, VEHICLE.friction_points, VEHICLE.friction_points_header)
    write_phantom_shapes(output_stream, TAG, VEHICLE.phantom_shapes, VEHICLE.phantom_shapes_header)
