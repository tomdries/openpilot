playback videos and can-data using openpilot
=====================

This fork added a module for supporting playback of video files combined with CAN-bus data. First, install openpilot and tools using the instructions provided in ./tools/README.md. The other sim modules should still work (metadrive, carla) though I would advise to use the original openpilot repository for that purpose.

## Launching openpilot and playback recording
First, start openpilot.
``` bash
poetry shell
./tools/sim/launch_openpilot.sh
```

In another window, start the bridge that loads the video and csv file. Edit the paths in the file to point to the corresponding data

``` bash
poetry shell
./tools/sim/test_bridge.sh
```






