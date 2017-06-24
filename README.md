# KivyPotentParticles
This 3D fork uses Python 3 is forked from Kivy Particle which is an implementation of [Starling Extension Particle System](https://github.com/PrimaryFeather/Starling-Extension-Particle-System) for Kivy Python framework.
used in https://github.com/expertmm/ParticlePandaPy3 and eventually in KivyGlops

## Features
* Intentionally forked from old version (skitoo/kivy-particle) instead of later garden.particlesystem, to avoid Cython.
* Tested with Kivy 1.9.0 Py3

## Known Issues
* ParticlePandaPy3 cannot yet use KivyPotentParticles to produce 3D results
* Changes for 3D were reverted for unknown reason (seems to be human error using git) -- see the commit that was lost: https://github.com/expertmm/KivyPotentParticles/commit/7be0058dbba854a9b73ee60d237c921378be0e6e -- see also ParticlePandaPy3

## Planned Features
* make rotation have 3 axes (change to 3 transforms, and add methods for changing rotation of each)




## Changes
* (2016-01-10) Changed rotate instruction to use spin_matrix instead of hard-codex y value (and added set_mode_3d and set_mode_2d to change spin_matrix between 0,1,0 for y-up 3d and 0,0,1 for spinning on screen 2d respectively)
* (2016-01-10) Changed 'Particle: COMPLETE' to 'Particle: nothing to do (num_particles==0)' and dedented it so it would actually have a chance of happening
* (2016-01-09) Changed the Rotate transform self.particles_dict[particle]['rotate'] to y axis (was z)
* (2016-01-09) Changed assertions in test folder to use pos and 0.0
* (2016-02-02) use pos intead of emitter_x and emitter_y
* (2016-02-02) create _has_value method for xml variable existence checking especially for sourcePosition
* (2016-02-01) set emitter_x, emitter_y to (0.0, 0.0) if sourcePosition not found (which doesn't exist in pex files exported by latest ParticlePanda)
* (2016-02-01) added existence check in _parse_data for variable before trying to get its value
* (2016-02-01) re-labeled second demo preset to "Color Spray" (and renamed file to colorspray.pex) for wider use such as in educational environments
* (2016-02-01) ran 2to3
