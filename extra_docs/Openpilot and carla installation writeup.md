Here's a quick write-up of how I got things working, may be useful to others here. I tested everything on ubuntu 20.04 installation with a GeForce RTX 3090. For me, the following works, however there are still some quirks:

- install openpilot tools, follow [openpilot tools readme](https://github.com/commaai/openpilot/tree/master/tools#readme))
- I tested everything outside the docker environment. To do this I take the three step approach: (see also  [openpilot sim readme](https://github.com/commaai/openpilot/tree/master/tools/sim):
	- terminal 1: `./start_carla.sh`
	- terminal 2: `poetry shell` followed by `./launch_openpilot.sh`
	- terminal 3: `poetry shell` followed by `./bridge.py --high_quality --dual_camera`. Also worked without `--high_quality` but never without `--dual_camera` (as this lediaves you with a blank screen)
- To drive manually, hold w when the bridge.py terminal is active
- To engage openpilot without getting `openpilot unavailable` warnings, initiatie it by pressing 2 (pressing 1 gives the error). Both 1 and 2 can later be used to adjust reference speed.

I ran into some issues along the way, I fixed those with some solutions found in the github issues:

- The model was not working, so I could not engage openpilot. The [fix suggested by jackhong12](https://github.com/commaai/openpilot/issues/23666#issuecomment-1045520664) worked, but I received an error when running `autogen.sh` . That was fixed with `sudo apt-get update` and then `sudo apt-get install -y automake autoconf libtool pkg-config`
- The car now was able to drive itself until the first corner, then I saw the notification "Take control immediately: Vehicle Parameter identification failed". When I tried to engage openpilot again, I got "Openpilot unavailable: Vehicle parameter identification failed.". I fixed this issue by uncommenting the code responsible for this warning, as suggested by [PhilWallace](https://github.com/commaai/openpilot/issues/27282#issuecomment-1433290959)

 It now works, but the experience is still buggy. Autopilot feels like it should perform better, though I have nothing to compare it to. I included a video for you to judge. I feel it's steering too much towards the inside of lanes, when in corners, and it's generally unstable. I suspect it has to do with the uncommenting of the vehicle parameter data. My first guess is that the controller may not receive car state parameters needed to stabilize because I uncommented the warning. Hypothesis 2 is that the system is executing too slow and causes lags making it unstable. (However, I'm testing this with a decent GPU - so Carla should not be causing too much overhead). Hypothesis 3: Openpilot isn't as good as I was hoping - at least not in the simulation setting - which would be a bummer.

Some remaining issues: 
- I used --joystick mode with a Logitech G923 Racing Wheel. Had to `pip install evdev` to the env activated by poetry shell. However, only the openpilot increase and decrease reference speed buttons (1 and 2 in keyboard mode) worked. No gas pedal, no steering commands are coming through

I'm not familiar enough yet with the code base to propose fixes but I'll do a bit of code studying over the coming weeks as I have the intend to use openpilot in a research project. If there are any pointers from a more experienced developer to fix these issues quickly, let me know. 