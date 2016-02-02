#Kivy Particle

Kivy Particle is an implementation of [Starling Extension Particle System](https://github.com/PrimaryFeather/Starling-Extension-Particle-System) for Kivy Python framework.

(Work in Progress)

# Python 3 fork by expertmm
Intentionally forked from old version (skitoo/kivy-particle) instead of later garden.particlesystem, to avoid Cython.

Tested with Kivy 1.9.0 Py3
## Changes
* (2016-02-02) use pos intead of emitter_x and emitter_y
* (2016-02-02) create _has_value method for xml variable existence checking especially for sourcePosition
* (2016-02-01) set emitter_x, emitter_y to (0.0, 0.0) if sourcePosition not found (which doesn't exist in pex files exported by latest ParticlePanda)
* (2016-02-01) added existence check in _parse_data for variable before trying to get its value
* (2016-02-01) re-labeled second demo preset to "Color Spray" (and renamed file to colorspray.pex) for wider use such as in educational environments
* (2016-02-01) ran 2to3
