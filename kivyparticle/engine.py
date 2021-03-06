# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Callback, Rotate, PushMatrix, PopMatrix, Translate, Quad
from kivy.graphics.opengl import glBlendFunc, GL_SRC_ALPHA, GL_ONE, GL_ZERO, GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA, GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA, GL_DST_COLOR, GL_ONE_MINUS_DST_COLOR
from kivy.core.image import Image
from kivy.logger import Logger
from xml.dom.minidom import parse as parse_xml
from .utils import random_variance, random_color_variance
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty

import sys
import os
import math

__all__ = ['EMITTER_TYPE_GRAVITY', 'EMITTER_TYPE_RADIAL', 'Particle', 'ParticleSystem']


EMITTER_TYPE_GRAVITY = 0
EMITTER_TYPE_RADIAL = 1

BLEND_FUNC = {0: GL_ZERO,
            1: GL_ONE,
            0x300: GL_SRC_COLOR,
            0x301: GL_ONE_MINUS_SRC_COLOR,
            0x302: GL_SRC_ALPHA,
            0x303: GL_ONE_MINUS_SRC_ALPHA,
            0x304: GL_DST_ALPHA,
            0x305: GL_ONE_MINUS_DST_ALPHA,
            0x306: GL_DST_COLOR,
            0x307: GL_ONE_MINUS_DST_COLOR
}


class Particle(object):

    def __init__(self):
        self.pos = [0.,0.,0.]
        self.rotation = 0
        self.current_time = 0
        self.scale, self.total_time = 1.0, 0.
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.color_delta = [0.0, 0.0, 0.0, 0.0]
        self.start = [0., 0., 0.]
        self.velocity = [0., 0., 0.]
        self.radial_acceleration, self.tangent_acceleration = 0, 0
        self.emit_radius, self.emit_radius_delta = 0, 0
        self.emit_rotation, self.emit_rotation_delta = 0, 0
        self.rotation_delta, self.scale_delta = 0, 0


class ParticleSystem(Widget):
    pos = ListProperty([0.0,0.0,0.0])  # emitter_x, emitter_y
    dim_count = NumericProperty(2)
    max_num_particles = NumericProperty(200)
    life_span = NumericProperty(2)
    texture = ObjectProperty(None)
    texture_path = StringProperty(None)
    life_span_variance = NumericProperty(0)
    start_size = NumericProperty(16)
    start_size_variance = NumericProperty(0)
    end_size = NumericProperty(16)
    end_size_variance = NumericProperty(0)
    emit_angle = NumericProperty(0)
    emit_angle_variance = NumericProperty(0)
    start_rotation = NumericProperty(0)
    start_rotation_variance = NumericProperty(0)
    end_rotation = NumericProperty(0)
    end_rotation_variance = NumericProperty(0)
    emitter_variance = ListProperty([100., 100., 100.])
    start_gravity = ListProperty([0.,0.,0.])
    end_gravity = ListProperty([0.,0.,0.])
    speed = NumericProperty(0)
    speed_variance = NumericProperty(0)
    radial_acceleration = NumericProperty(100)
    radial_acceleration_variance = NumericProperty(0)
    tangential_acceleration = NumericProperty(0)
    tangential_acceleration_variance = NumericProperty(0)
    max_radius = NumericProperty(100)
    max_radius_variance = NumericProperty(0)
    min_radius = NumericProperty(50)
    rotate_per_second = NumericProperty(0)
    rotate_per_second_variance = NumericProperty(0)
    start_color = ListProperty([1., 1., 1., 1.])
    start_color_variance = ListProperty([1., 1., 1., 1.])
    end_color = ListProperty([1., 1., 1., 1.])
    end_color_variance = ListProperty([1., 1., 1., 1.])
    spin_matrix = ListProperty([0,1,0])
    blend_factor_source = NumericProperty(770)
    blend_factor_dest = NumericProperty(1)
    emitter_type = NumericProperty(0)

    update_interval = NumericProperty(1. / 30.)
    _is_paused = BooleanProperty(False)
    flatten_enable = BooleanProperty(False)

    def __init__(self, config, **kwargs):
        super(ParticleSystem, self).__init__(**kwargs)
        for name, value in kwargs.items():
            if name=="dim_count":
                self.dim_count=int(value)
                #print("[ ParticleSystem ] (verbose message) __init__: caller set dimensions to " + str(self.dim_count))
            elif name=="flatten_enable":
                self.flatten_enable=bool(value)
        self.capacity = 0
        self.particles = list()
        self.particles_dict = dict()
        self.emission_time = 0.0
        self.frame_time = 0.0
        self.num_particles = 0

        if config is not None:
            self._parse_config(config)
        self.emission_rate = self.max_num_particles / self.life_span
        self.initial_capacity = self.max_num_particles
        self.max_capacity = self.max_num_particles
        self._raise_capacity(self.initial_capacity)

        with self.canvas.before:
            Callback(self._set_blend_func)
        with self.canvas.after:
            Callback(self._reset_blend_func)

        Clock.schedule_once(self._update, self.update_interval)

    def start(self, duration=sys.maxsize):
        if self.emission_rate != 0:
            self.emission_time = duration

    def stop(self, clear=False):
        self.emission_time = 0.0
        if clear:
            self.num_particles = 0
            self.particles_dict = dict()
            self.canvas.clear()

    def on_max_num_particles(self, instance, value):
        self.max_capacity = value
        if self.capacity < value:
            self._raise_capacity(self.max_capacity - self.capacity)
        elif self.capacity > value:
            self._lower_capacity(self.capacity - self.max_capacity)
        self.emission_rate = self.max_num_particles / self.life_span

    def on_texture(self, instance, value):
        for p in self.particles:
            try:
                self.particles_dict[p]['rect'].texture = self.texture
            except KeyError:
                # if particle isn't initialized yet, you can't change its texture.
                pass

    def on_life_span(self, instance, value):
        self.emission_rate = self.max_num_particles / value

    def _set_blend_func(self, instruction):
        #glBlendFunc(self.blend_factor_source, self.blend_factor_dest)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    def _reset_blend_func(self, instruction):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _parse_config(self, config):
        self._config = parse_xml(config)

        texture_path = self._parse_data('texture', 'name')
        config_dir_path = os.path.dirname(os.path.abspath(config))
        path = os.path.join(config_dir_path, texture_path)
        if os.path.exists(path):
            self.texture_path = path
        else:
            self.texture_path = texture_path

        self.texture = Image(self.texture_path).texture
        self.pos[0] = 0.0  # formerly emitter_x
        self.pos[1] = 0.0  # formerly emitter_y
        self.pos[2] = 0.0
        try_x = None
        try_y = None
        try_z = None
        # NOTE: for 3D x, y, or 0 (what has best effect) is used for z
        if self._has_value('sourcePosition','x'):
            try_x = self._parse_data('sourcePosition', 'x')
            if self._has_value('sourcePosition','y'):
                try_y = self._parse_data('sourcePosition', 'y')
            else:
                print("[ ParticleSystem ] (INPUT ERROR) pex has x but no y")
                try_y = try_x
        if self._has_value('sourcePosition','z'):
            try_z = self._parse_data('sourcePosition', 'z')
        else:
            if self.dim_count > 2:
                try_z = try_x  #xz as ground plane to use 2D pex in 3D
                try_y = 0.0  # on ground
            else:
                try_z = 0.0
        #else ignore -- everything is ok (sourcePosition not present in later versions of pex)
        if try_x is None:
            try_x = 0.
        if try_y is None:
            try_y = 0.
        if try_z is None:
            try_z = 0.
        # ListProperty must remain same len or exception occurs:
        self.pos = [ float(try_x), float(try_y), float(try_z) ]
        self.emitter_variance[0] = float(self._parse_data('sourcePositionVariance', 'x'))
        self.emitter_variance[1] = float(self._parse_data('sourcePositionVariance', 'y'))
        if self.dim_count > 2:
            if self._has_value('sourcePositionVariance','z'):
                self.emitter_variance[2] = float(self._parse_data('sourcePositionVariance', 'z'))
                #print("Using z variance")
            else:
                # reuse other ground dimension to use pex in 3D:
                self.emitter_variance[2] = self.emitter_variance[0]
                #print("Using x for z variance")
        else:
            self.emitter_variance[2] = 0.0
        self.start_gravity[0] = float(self._parse_data('gravity', 'x'))
        self.start_gravity[1] = float(self._parse_data('gravity', 'y'))
        if self.dim_count > 2:
            if self._has_value('gravity','z'):
                self.start_gravity[2] = float(self._parse_data('gravity', 'z'))
            else:
                # self.start_gravity[1] = 0.0  # flatten
                # Reuse x for ground dim z to make 2D pex work with 3D:
                self.start_gravity[2] = self.start_gravity[0]

        if self._has_value('finishGravity','x'):
            self.end_gravity[0] = float(self._parse_data('finishGravity', 'x'))
        else:
            self.end_gravity[0] = self.start_gravity[0]
        if self._has_value('finishGravity','y'):
            self.end_gravity[1] = float(self._parse_data('finishGravity', 'y'))
        else:
            self.end_gravity[1] = self.start_gravity[1]
        if self._has_value('finishGravity','z'):
            self.end_gravity[2] = float(self._parse_data('finishGravity', 'z'))
        else:
            self.end_gravity[2] = self.start_gravity[2]

        self.emitter_type = int(self._parse_data('emitterType'))
        self.max_num_particles = int(self._parse_data('maxParticles'))
        self.life_span = max(0.01, float(self._parse_data('particleLifeSpan')))
        self.life_span_variance = float(self._parse_data('particleLifespanVariance'))
        self.start_size = float(self._parse_data('startParticleSize'))
        self.start_size_variance = float(self._parse_data('startParticleSizeVariance'))
        self.end_size = float(self._parse_data('finishParticleSize'))
        self.end_size_variance = float(self._parse_data('FinishParticleSizeVariance'))
        self.emit_angle = math.radians(float(self._parse_data('angle')))
        self.emit_angle_variance = math.radians(float(self._parse_data('angleVariance')))
        self.start_rotation = math.radians(float(self._parse_data('rotationStart')))
        self.start_rotation_variance = math.radians(float(self._parse_data('rotationStartVariance')))
        self.end_rotation = math.radians(float(self._parse_data('rotationEnd')))
        self.end_rotation_variance = math.radians(float(self._parse_data('rotationEndVariance')))
        self.speed = float(self._parse_data('speed'))
        self.speed_variance = float(self._parse_data('speedVariance'))
        self.radial_acceleration = float(self._parse_data('radialAcceleration'))
        self.radial_acceleration_variance = float(self._parse_data('radialAccelVariance'))
        self.tangential_acceleration = float(self._parse_data('tangentialAcceleration'))
        self.tangential_acceleration_variance = float(self._parse_data('tangentialAccelVariance'))
        self.max_radius = float(self._parse_data('maxRadius'))
        self.max_radius_variance = float(self._parse_data('maxRadiusVariance'))
        self.min_radius = float(self._parse_data('minRadius'))
        self.rotate_per_second = math.radians(float(self._parse_data('rotatePerSecond')))
        self.rotate_per_second_variance = math.radians(float(self._parse_data('rotatePerSecondVariance')))
        self.start_color = self._parse_color('startColor')
        self.start_color_variance = self._parse_color('startColorVariance')
        self.end_color = self._parse_color('finishColor')
        self.end_color_variance = self._parse_color('finishColorVariance')
        self.blend_factor_source = self._parse_blend('blendFuncSource')
        self.blend_factor_dest = self._parse_blend('blendFuncDestination')

    def _parse_data(self, name, attribute='value'):
        elements = self._config.getElementsByTagName(name)
        result = None
        if (elements is not None) and (len(elements)>0):
            result = elements[0].getAttribute(attribute)
        else:
            print("ERROR: '" + str(name) + "' not found in config ")
            # +str(self._config.toxml()))
        return result

    def _has_value(self, name, attribute=None):
        if attribute is None:
            elements = self._config.getElementsByTagName(name)
            result = False
            if (elements is not None) and (len(elements)>0):
                True
            return result
        else:
            elements = self._config.getElementsByTagName(name)
            result = False
            if (elements is not None) and (len(elements)>0):
                tmp = elements[0].getAttribute(attribute)
                if (tmp is not None) and (tmp != ""):
                    #print("[ ParticleSystem ] (verbose message) " + \
                    #      "_has_value got " + name + "." + \
                    #      str(attribute) + ": " + tmp)
                    result = True
            #else:
            #    print("ERROR: '"+str(name)+"' not found in config ")  # +str(self._config.toxml()))
            return result

    def _parse_color(self, name):
        return [float(self._parse_data(name, 'red')), float(self._parse_data(name, 'green')), float(self._parse_data(name, 'blue')), float(self._parse_data(name, 'alpha'))]

    def _parse_blend(self, name):
        value = int(self._parse_data(name))
        return BLEND_FUNC[value]

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False
        Clock.schedule_once(self._update, self.update_interval)

    def _update(self, dt):
        self._advance_time(dt)
        self._render()
        if not self._is_paused:
            Clock.schedule_once(self._update, self.update_interval)

    def _create_particle(self):
        return Particle()

    def _init_particle(self, particle):
        life_span = random_variance(self.life_span, self.life_span_variance)
        if life_span <= 0.0:
            return

        particle.current_time = 0.0
        particle.total_time = life_span
        H_AXIS_I = 1  # secondary ground axis (where x aka 0 is primary)
        V_AXIS_I = 1  # vertical axis
        if self.dim_count > 2:
            H_AXIS_I = 2  # ground is xz plane in 3D mode

        # NOTE: emitter_variance is prepared based on dim_count on load
        for i in range(self.dim_count):
            particle.pos[i] = random_variance(self.pos[i], self.emitter_variance[i])
            particle.start[i] = self.pos[0]

        angle = random_variance(self.emit_angle, self.emit_angle_variance)
        speed = random_variance(self.speed, self.speed_variance)
        particle.velocity[0] = speed * math.cos(angle)
        particle.velocity[H_AXIS_I] = speed * math.sin(angle)

        particle.emit_radius = random_variance(self.max_radius, self.max_radius_variance)
        particle.emit_radius_delta = (self.max_radius - self.min_radius) / life_span

        particle.emit_rotation = random_variance(self.emit_angle, self.emit_angle_variance)
        particle.emit_rotation_delta = random_variance(self.rotate_per_second, self.rotate_per_second_variance)

        particle.radial_acceleration = random_variance(self.radial_acceleration, self.radial_acceleration_variance)
        particle.tangent_acceleration = random_variance(self.tangential_acceleration, self.tangential_acceleration_variance)

        start_size = random_variance(self.start_size, self.start_size_variance)
        end_size = random_variance(self.end_size, self.end_size_variance)

        start_size = max(0.1, start_size)
        end_size = max(0.1, end_size)

        particle.scale = start_size / self.texture.width
        particle.scale_delta = ((end_size - start_size) / life_span) / self.texture.width

        # colors
        start_color = random_color_variance(self.start_color, self.start_color_variance)
        end_color = random_color_variance(self.end_color, self.end_color_variance)

        particle.color_delta = [(end_color[i] - start_color[i]) / life_span for i in range(4)]
        particle.color = start_color

        # gravity delta
        particle.gravity = [self.start_gravity[i] for i in range(3)]
        particle.gravity_delta = [(self.end_gravity[i] - self.start_gravity[i]) / life_span for i in range(3)]
        #print("gravity_delta[1] = (" + str(self.end_gravity[1]) + " - " + str(self.start_gravity[1]) + ") / " + str(life_span))  # debug only

        # rotation
        start_rotation = random_variance(self.start_rotation, self.start_rotation_variance)
        end_rotation = random_variance(self.end_rotation, self.end_rotation_variance)
        particle.rotation = start_rotation
        particle.rotation_delta = (end_rotation - start_rotation) / life_span

    def _advance_particle(self, particle, passed_time):
        if self.flatten_enable:
            particle.start[2] = 0.0
            particle.pos[2] = 0.0
            particle.velocity[2] = 0.0
            particle.gravity[2] = 0.0
            particle.gravity_delta[2] = 0.0
            self.pos[2] = 0.0

        H_AXIS_I = 1  # secondary ground axis (where x aka 0 is primary)
        V_AXIS_I = 1  # vertical axis
        if self.dim_count > 2:
            # rotate around y in 3D mode (uses z as 2nd ground axis):
            H_AXIS_I = 2  # ground is xz plane in 3D mode
        passed_time = min(passed_time, particle.total_time - particle.current_time)
        particle.current_time += passed_time

        if self.emitter_type == EMITTER_TYPE_RADIAL:
            particle.emit_rotation += particle.emit_rotation_delta * passed_time
            particle.emit_radius -= particle.emit_radius_delta * passed_time
            particle.pos[0] = self.pos[0] - math.cos(particle.emit_rotation) * particle.emit_radius
            particle.pos[V_AXIS_I] = self.pos[V_AXIS_I]
            particle.pos[H_AXIS_I] = self.pos[H_AXIS_I] - math.sin(particle.emit_rotation) * particle.emit_radius
            if particle.emit_radius < self.min_radius:
                particle.current_time = particle.total_time
        else:
            distance = [0., 0., 0.]
            for i in range(self.dim_count):
                distance[i] = particle.pos[i] - particle.start[i]
            distance_scalar = math.sqrt(distance[0] * distance[0] + distance[H_AXIS_I] * distance[H_AXIS_I])
            if distance_scalar < 0.01:
                distance_scalar = 0.01

            radial = [0., 0., 0.]
            tangential = [0., 0., 0.]
            new_pos = [0., 0., 0.]  # formerly new_y

            #for i in range(self.dim_count):
            #    radial[i] = distance[i] / distance_scalar
            #    tangential[i] = radial[i]
            # use only ground axes:
            radial[0] = distance[0] / distance_scalar
            radial[H_AXIS_I] = distance[H_AXIS_I] / distance_scalar
            tangential[0] = radial[0]
            tangential[H_AXIS_I] = radial[H_AXIS_I]

            radial[0] *= particle.radial_acceleration
            radial[H_AXIS_I] *= particle.radial_acceleration

            new_pos[H_AXIS_I] = tangential[0]
            tangential[0] = -tangential[H_AXIS_I] * particle.tangent_acceleration
            tangential[H_AXIS_I] = new_pos[H_AXIS_I] * particle.tangent_acceleration

            #gravity = [0., 0., 0.]

            # NOTE: gravity is already processed for dim_count on load
            #gravity[0] = self.gravity[0]
            #if self.gravity_z is not None:
            #    gravity[H_AXIS_I] = self.gravity_z
            #else:
            #    gravity[H_AXIS_I] = self.gravity_x
            #gravity[V_AXIS_I] = self.gravity_y

            for i in range(self.dim_count):
                particle.gravity[i] += particle.gravity_delta[i] * passed_time
                #print("particle.gravity[" + str(i) + "]: " + str(particle.gravity[i]) + " += " + str(particle.gravity_delta[i]) + " * " + str(passed_time))
                particle.velocity[i] += passed_time * (particle.gravity[i] + radial[i] + tangential[i])
                particle.pos[i] += particle.velocity[i] * passed_time

        particle.scale += particle.scale_delta * passed_time
        particle.rotation += particle.rotation_delta * passed_time

        particle.color = [particle.color[i] + particle.color_delta[i] * passed_time for i in range(4)]

    def _raise_capacity(self, by_amount):
        old_capacity = self.capacity
        new_capacity = min(self.max_capacity, self.capacity + by_amount)

        for i in range(int(new_capacity - old_capacity)):
            self.particles.append(self._create_particle())

        self.num_particles = int(new_capacity)
        self.capacity = new_capacity

    def _lower_capacity(self, by_amount):
        old_capacity = self.capacity
        new_capacity = max(0, self.capacity - by_amount)

        for i in range(int(old_capacity - new_capacity)):
            try:
                self.canvas.remove(self.particles_dict[self.particles.pop()]['rect'])
            except:
                pass

        self.num_particles = int(new_capacity)
        self.capacity = new_capacity

    def _advance_time(self, passed_time):
        particle_index = 0

        # advance existing particles
        while particle_index < self.num_particles:
            particle = self.particles[particle_index]
            if particle.current_time < particle.total_time:
                self._advance_particle(particle, passed_time)
                particle_index += 1
            else:
                if particle_index != self.num_particles - 1:
                    next_particle = self.particles[self.num_particles - 1]
                    self.particles[self.num_particles - 1] = particle
                    self.particles[particle_index] = next_particle
                self.num_particles -= 1
        if self.num_particles == 0:
            Logger.debug('Particle: nothing to do (num_particles==0)')

        # create and advance new particles
        if self.emission_time > 0:
            time_between_particles = 1.0 / self.emission_rate
            self.frame_time += passed_time

            while self.frame_time > 0:
                if self.num_particles < self.max_capacity:
                    if self.num_particles == self.capacity:
                        self._raise_capacity(self.capacity)

                    particle = self.particles[self.num_particles]
                    self.num_particles += 1
                    self._init_particle(particle)
                    self._advance_particle(particle, self.frame_time)

                self.frame_time -= time_between_particles

            if self.emission_time != sys.maxsize:
                self.emission_time = max(0.0, self.emission_time - passed_time)

    def set_mode_3d():
        self.spin_matrix = [0,1,0]  # spin on y-axis since assuming 3D with y-up
        self.dim_count = 3

    def set_mode_2d():
        self.spin_matrix=[0,0,1]  # spin on z-axis to move on screen plane
        self.dim_count = 2

    def _render(self):
        if self.num_particles == 0:
            return
        for i in range(self.num_particles):
            particle = self.particles[i]
            size = (self.texture.size[0] * particle.scale, self.texture.size[1] * particle.scale)
            if particle not in self.particles_dict:
                self.particles_dict[particle] = dict()
                color = particle.color[:]
                with self.canvas:
                    self.particles_dict[particle]['color'] = Color(color[0], color[1], color[2], color[3])
                    PushMatrix()
                    self.particles_dict[particle]['translate'] = Translate()
                    self.particles_dict[particle]['rotate'] = Rotate()
                    self.particles_dict[particle]['rotate'].set(particle.rotation, self.spin_matrix[0], self.spin_matrix[1], self.spin_matrix[2])
                    self.particles_dict[particle]['rect'] = Quad(texture=self.texture, points=(-size[0] * 0.5, -size[1] * 0.5, size[0] * 0.5, -size[1] * 0.5, size[0] * 0.5,  size[1] * 0.5, -size[0] * 0.5,  size[1] * 0.5))
                    if self.dim_count > 2:
                        self.particles_dict[particle]['translate'].xyz = (particle.pos[0], particle.pos[1], particle.pos[2])
                    else:
                        self.particles_dict[particle]['translate'].xy = (particle.pos[0], particle.pos[1])
                    PopMatrix()
            else:
                self.particles_dict[particle]['rotate'].angle = particle.rotation
                if self.dim_count > 2:
                    self.particles_dict[particle]['translate'].xyz = (particle.pos[0], particle.pos[1], particle.pos[2])
                else:
                    self.particles_dict[particle]['translate'].xy = (particle.pos[0], particle.pos[1])
                self.particles_dict[particle]['color'].rgba = particle.color
                self.particles_dict[particle]['rect'].points = (-size[0] * 0.5, -size[1] * 0.5, size[0] * 0.5, -size[1] * 0.5, size[0] * 0.5,  size[1] * 0.5, -size[0] * 0.5,  size[1] * 0.5)
