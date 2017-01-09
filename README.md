# KivyPotentParticles
This 3D fork uses Python 3 is forked from Kivy Particle which is an implementation of [Starling Extension Particle System](https://github.com/PrimaryFeather/Starling-Extension-Particle-System) for Kivy Python framework.

## Features
* Intentionally forked from old version (skitoo/kivy-particle) instead of later garden.particlesystem, to avoid Cython.
* Tested with Kivy 1.9.0 Py3

used in https://github.com/expertmm/ParticlePandaPy3 and eventually in KivyGlops

## Changes
* (2016-01-09) Changed the Rotate transform self.particles_dict[particle]['rotate'] to y axis (was z), for use in 3D (Y-up) scenes.
* (2016-01-09) Changed assertions in test folder to use pos and 0.0
* (2016-02-02) use pos intead of emitter_x and emitter_y
* (2016-02-02) create _has_value method for xml variable existence checking especially for sourcePosition
* (2016-02-01) set emitter_x, emitter_y to (0.0, 0.0) if sourcePosition not found (which doesn't exist in pex files exported by latest ParticlePanda)
* (2016-02-01) added existence check in _parse_data for variable before trying to get its value
* (2016-02-01) re-labeled second demo preset to "Color Spray" (and renamed file to colorspray.pex) for wider use such as in educational environments
* (2016-02-01) ran 2to3
