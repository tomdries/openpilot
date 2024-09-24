folder='/home/tom/Replication Dropbox/Tom Driessen/01 Carla Openpilot/recordings/' # record your own or grab from 4TU repository
condition='surprise_2'  # aggressive, surprise, calm, aggressive_2, surprise_2, calm_2
video_file="${folder}${condition}_stretched.mp4"
telematics_file="${folder}${condition}_openpilot_df.csv"

./run_bridge.py --simulator video --t0 0 \
--video_file "$video_file" \
--telematics_file "$telematics_file"    

