#!/bin/bash
# ./run_bridge.py --dual_camera --simulator video --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/ladderland_autos__2023-11-23_12-55-09.mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/ladderland_autos__2023-11-23_12-55-09.csv"

# ./run_bridge.py --simulator video --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged).mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged)_speed.csv"
./run_bridge.py --simulator video --t0 600 --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged) cropped 20fps.mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged) cropped 20fps_speed.csv"
