# KivyPotentParticles
This 3D fork uses Python 3 is forked from Kivy Particle which is an implementation of [Starling Extension Particle System](https://github.com/PrimaryFeather/Starling-Extension-Particle-System) for Kivy Python framework.
used in https://github.com/expertmm/ParticlePandaPy3 and eventually may be used in KivyGlops

## Features
* Intentionally forked from old version (skitoo/kivy-particle) instead of later garden.particlesystem, to avoid Cython.
* Tested with Kivy 1.9.0 Py3

## Planned Features
* make rotation have 3 axes (change to 3 transforms, and add methods for changing rotation of each)

## Known Issues
* engine.py: some 3D issues are ignored (non-fatally) by _advance_particle
* ParticlePandaPy3 cannot yet use KivyPotentParticles to produce 3D results
* Changes for 3D were reverted for unknown reason (seems to be human error using git) -- see the commit that was lost: https://github.com/expertmm/KivyPotentParticles/commit/7be0058dbba854a9b73ee60d237c921378be0e6e -- see also ParticlePandaPy3

## Changes
(2018-01-08)
* kivyparticle/engine.py: added more checks for 3D; ParticleSystem now has 3D pos instead of inherited pos which has immutable length of 2; _advance_particle corrected to modify particle.pos instead of self.pos
(2018-01-07)
* kivyparticle/engine.py: fixed old bug with unfinished line for 3D mode
(2016-01-10)
* Changed 'Particle: COMPLETE' to 'Particle: nothing to do (num_particles==0)' and dedented it so it would actually have a chance of happening
* Changed rotate instruction to use spin_matrix instead of hard-codex y value (and added set_mode_3d and set_mode_2d to change spin_matrix between 0,1,0 for y-up 3d and 0,0,1 for spinning on screen 2d respectively)
(2016-01-09)
* Changed assertions in test folder to use pos and 0.0
* Changed the Rotate transform self.particles_dict[particle]['rotate'] to y axis (was z)
(2016-02-02)
* create _has_value method for xml variable existence checking especially for sourcePosition
* use pos intead of emitter_x and emitter_y for ParticleSystem
(2016-02-01)
* ran 2to3
* re-labeled second demo preset to "Color Spray" (and renamed file to colorspray.pex) for wider use such as in educational environments
* added existence check in _parse_data for variable before trying to get its value
* set emitter_x, emitter_y to (0.0, 0.0) if sourcePosition not found (which doesn't exist in pex files exported by latest ParticlePanda)

