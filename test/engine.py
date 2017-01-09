# -*- coding: utf-8 -*-

from kivyparticle import ParticleSystem
from kivy.graphics.opengl import GL_ONE, GL_SRC_ALPHA
import unittest
import math


class TestParticleSystem(unittest.TestCase):
    def setUp(self):
        self.s = ParticleSystem('test/media/config.pex')

    def test_config(self):
        self.assertEqual((32, 32), self.s.texture.size)
        self.assertEqual(0.00, self.s.pos[0])  # formerly 160.55, self.s.emitter_x
        self.assertEqual(0.00, self.s.pos[1])  # formerly 428.95, self.s.emitter_y
        self.assertEqual(104.41, self.s.emitter_x_variance)
        self.assertEqual(0.00, self.s.emitter_y_variance)
        self.assertEqual(0.00, self.s.gravity_x)
        self.assertEqual(0.00, self.s.gravity_y)
        self.assertEqual(0, self.s.emitter_type)
        self.assertEqual(300, self.s.max_num_particles)
        self.assertEqual(2.0, self.s.life_span)
        self.assertEqual(1.9, self.s.life_span_variance)
        self.assertEqual(70.0, self.s.start_size)
        self.assertEqual(49.53, self.s.start_size_variance)
        self.assertEqual(10.0, self.s.end_size)
        self.assertEqual(0.0, self.s.end_size_variance)
        self.assertEqual(math.radians(270.37), self.s.emit_angle)
        self.assertEqual(math.radians(15.0), self.s.emit_angle_variance)
        self.assertEqual(0.0, self.s.start_rotation)
        self.assertEqual(0.0, self.s.start_rotation_variance)
        self.assertEqual(0.0, self.s.end_rotation)
        self.assertEqual(0.0, self.s.end_rotation_variance)
        self.assertEqual(90.0, self.s.speed)
        self.assertEqual(30.0, self.s.speed_variance)
        self.assertEqual(0.0, self.s.radial_acceleration)
        self.assertEqual(0.0, self.s.radial_acceleration_variance)
        self.assertEqual(0.0, self.s.tangential_acceleration)
        self.assertEqual(0.0, self.s.tangential_acceleration_variance)
        self.assertEqual(100.0, self.s.max_radius)
        self.assertEqual(0.0, self.s.max_radius_variance)
        self.assertEqual(0.0, self.s.min_radius)
        self.assertEqual(0.0, self.s.rotate_per_second)
        self.assertEqual(0.0, self.s.rotate_per_second_variance)
        self.assertEqual([1.0, 0.31, 0.0, 0.62], self.s.start_color)
        self.assertEqual([0.0, 0.0, 0.0, 0.0], self.s.start_color_variance)
        self.assertEqual([1.0, 0.31, 0.0, 0.0], self.s.end_color)
        self.assertEqual([0.0, 0.0, 0.0, 0.0], self.s.end_color_variance)
        self.assertEqual(GL_SRC_ALPHA, self.s.blend_factor_source)
        self.assertEqual(GL_ONE, self.s.blend_factor_dest)
