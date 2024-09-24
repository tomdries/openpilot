
# Lokin's video
# ./run_bridge.py --simulator video --t0 600 --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged) cropped 20fps.mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/01 VideoData/02 (merged) cropped 20fps_speed.csv"

# # ladderland
# ./run_bridge.py --simulator video --t0 0 --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/ladderland_autos__2023-11-23_12-55-09.mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/ladderland_autos__2023-11-23_12-55-09.csv"

# olger video 
# ./run_bridge.py --simulator video --t0 0 --video_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/02 Experiments Olger/poging 4/video cropped 20fps.mp4" --telematics_file "/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/02 Experiments Olger/poging 4/openpilot.csv"

## redlight recordings town01

condition='surprise6'  #['late_50_9', 'late_50_9_2', 'late_50_7', 'slowgood_60_1','slow_unknown', 'slow_unknown2']['door_rood', 'groen_en_speedtest', 'laat_remmen', 'vroeg_remmen_1', 'vroeg_remmen_slow_approach' ]
video_file="/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/02 Experiments Olger/redbus/${condition}_stretched.mp4"
telematics_file="/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/Files/02 Experiments Olger/redbus/${condition}_openpilot_df.csv"

./run_bridge.py --simulator video --t0 0 \
--video_file "$video_file" \
--telematics_file "$telematics_file"    

