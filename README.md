# KivyPotentParticles
This 3D fork uses Python 3 is forked from Kivy Particle which is an implementation of [Starling Extension Particle System](https://github.com/PrimaryFeather/Starling-Extension-Particle-System) for Kivy Python framework.
used in https://github.com/expertmm/ParticlePandaPy3 and eventually may be used in KivyGlops
<https://github.com/expertmm/KivyPotentParticles>

## Features
* Intentionally forked from old version (skitoo/kivy-particle) instead of later garden.particlesystem, to avoid Cython.
* Tested with Kivy 1.10.0 for python3

## Planned Features
* make rotation have 3 axes (change to 3 transforms, and add methods for changing rotation of each)

## Known Issues
* engine.py: some 3D issues are ignored (non-fatally) by _advance_particle
* ParticlePandaPy3 cannot yet use KivyPotentParticles to produce 3D results

## Changes
(2018-01-09)
* replaced emitter_*_variance with emitter_variance coordinate list
* now flatten_enable is used by ParticleSystem constructor if present via kwargs (helps 3D mode work better on 2D projection matrix such as an unmodified Kivy Widget)
(2018-01-08)
* kivyparticle/engine.py: added more checks for 3D; ParticleSystem now has 3D pos instead of inherited pos which has immutable length of 2; _advance_particle corrected to modify particle.pos instead of self.pos
* demo/main.py: delayed start of demo so that it knows layout size (for proper centering)
* You can now specify dim_count (2 or 3 for 2D or 3D mode) for ParticleSystem constructor
* removed `start_x, start_y, velocity_x, velocity_y` from Particle in favor of start and velocity coordinate lists
* (moved Particle members' initialization from class member definition to __init__ to ensure values aren't shared between particles) fix particle jumpiness
* demo/media/fire.pex: improved fire color and gravity
  * kivyparticle/engine.py: can now read and utilize `finishGravity` (x, y, and optionally z) (feature specific to KivyPotentParticles) if present in pex file (also `gravity_delta` cached during `_init_particle` for faster processing--for each particle, since varies depending on particle life)
  * kivyparticle/engine.py: renamed gravity list (formerly gravity_x, gravity_y) to start_gravity and added per-particle gravity
* kivyparticle/engine.py repaired ParticleSystem _has_value (it was never working before apparently)
(2018-01-07)
* kivyparticle/engine.py: fixed old bug with unfinished line for 3D mode
(2017-01-13)
* (Changes for 3D had been reverted for unknown reason [seems to be human error using git] -- see the commit that had been lost: https://github.com/expertmm/KivyPotentParticles/commit/7be0058dbba854a9b73ee60d237c921378be0e6e -- see also ParticlePandaPy3]
* applied changes for 3D
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

## Developer Notes
* additive blending is done via `glBlendFunc(GL_SRC_ALPHA, GL_ONE)` via `_set_blend_func` which is added to canvas.before (after drawing is done, `glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)` is done via `_reset_blend_func` which is added to canvas.after)
* tangent_acceleration is acceleration from center
* sun, colorspray, jellyfish, and fire are all emitterType 0 (EMITTER_TYPE_GRAVITY)
* random_variance and random_color_variance are in kivyparticle/utils.py (but must be imported as .utils to avoid other things called utils)
