# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import kivy
kivy.require('1.5.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivyparticle import ParticleSystem


class DemoParticle(Widget):
    
    def __init__(self, **kwargs):
        super(DemoParticle, self).__init__(**kwargs)
        self.dim_count = 2
        self.systems = {}
        self.create_particle_systems(self.dim_count)
        self.current = None
        Clock.schedule_once(self._app_loaded, 1.0)
        #If _show is called earlier (such as after .1, or .5 on some
        # computers), window size may not be calculated yet and
        # therefore object will not be centered. 
        
    def _app_loaded(self, dt):
        #dt is passed time according to kivy-particle (kivyparticle/engine.py)
        self._show("sun")
        
        
    def create_particle_systems(self, d):
        self.systems["sun"] = ParticleSystem('media/sun.pex', dim_count=d)
        self.systems["colorspray"] = ParticleSystem('media/colorspray.pex', dim_count=d)
        self.systems["jellyfish"] = ParticleSystem('media/jellyfish.pex', dim_count=d)
        self.systems["fire"] = ParticleSystem('media/fire.pex', dim_count=d)

    def on_touch_down(self, touch):
        self.current.pos[0] = float(touch.x)
        self.current.pos[1] = float(touch.y)

    def on_touch_move(self, touch):
        self.current.pos[0] = float(touch.x)
        self.current.pos[1] = float(touch.y)

    def show_sun(self, b):
        self._show("sun")

    def show_colorspray(self, b):
        self._show("colorspray")

    def show_jellyfish(self, b):
        self._show("jellyfish")

    def show_fire(self, b):
        self._show("fire")
    
    def toggle_dimensions(self, instance):
        if self.dim_count == 2:
            self.dim_count = 3
        else:
            self.dim_count = 2
        self.create_particle_systems(self.dim_count)
        self.mode_button.text = 'Mode is ' + str(self.dim_count) + \
                                 "D\n(click to change)"
        prev_system_name = self.current_name
        self._show(None)
        self._show(prev_system_name)

    def _show(self, name):
        if self.current:
            self.remove_widget(self.current)
            self.current.stop(True)
        self.current_name = name
        if name is not None:
            self.current = self.systems[name]
            self.current.pos[0] = self.width/2.  # 300.0
            self.current.pos[1] = self.height/2.  # 300
            self.add_widget(self.current)
            self.current.start()
        else:
            self.current = None


class DemoParticleApp(App):
    def build(self):
        root = GridLayout(cols=2)
        paint = DemoParticle(size_hint_x=None, width=600)
        root.add_widget(paint)
        buttons = BoxLayout(orientation='vertical')
        root.add_widget(buttons)

        sun = Button(text='Sun')
        sun.bind(on_press=paint.show_sun)
        buttons.add_widget(sun)

        colorspray = Button(text='Color Spray')
        colorspray.bind(on_press=paint.show_colorspray)
        buttons.add_widget(colorspray)

        jellyfish = Button(text='JellyFish')
        jellyfish.bind(on_press=paint.show_jellyfish)
        buttons.add_widget(jellyfish)

        fire = Button(text='Fire')
        fire.bind(on_press=paint.show_fire)
        buttons.add_widget(fire)

        paint.mode_button = Button(text='Mode is ' + str(paint.dim_count) + \
                                   "D\n(click to change)")
        paint.mode_button.bind(on_press=paint.toggle_dimensions)
        buttons.add_widget(paint.mode_button)

        return root


if __name__ == '__main__':
    DemoParticleApp().run()
