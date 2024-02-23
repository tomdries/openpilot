import numpy as np
import pandas as pd
import cv2
import csv
from time import time
from openpilot.tools.sim.lib.camerad import W, H
from openpilot.tools.sim.lib.video_helpers import parse_struct, HEADER_META
from openpilot.tools.sim.bridge.common import World
from openpilot.tools.sim.lib.common import SimulatorState, vec3
import cereal.messaging as messaging

MAX_STEER_ANGLE = 0.5

class VideoReader:
  def __init__(self, video_path):
    self.video_file = cv2.VideoCapture(str(video_path))
    if not self.video_file.isOpened():
      raise ValueError("Error opening video file")
    self.frame = 0

  def read(self):
    self.frame += 1
    ret, frame = self.video_file.read()
    if ret:
      # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      frame_rgb = frame
      return frame_rgb
    else:
      self.close()
      return None

  def close(self):
    self.video_file.release()


class CsvLogger:
    def __init__(self, csv_out, header=None, buffer_size=1000):
        # Create a new CSV file (even if exists) and write the header
        with open(csv_out, 'w', newline='') as f:
            writer = csv.writer(f)
            if header is not None:
                writer.writerow(header)

        self.csv_out = csv_out
        self.csv_buffer = []
        self.csv_buffer_size = buffer_size

    def log(self, log_data):
        self.csv_buffer.append(log_data)
        if len(self.csv_buffer) >= self.csv_buffer_size:
            self.flush()

    def flush(self):
        with open(self.csv_out, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.csv_buffer)
        self.csv_buffer.clear()  # Clear the buffer after flushing


class VideoWorld(World):
  def __init__(self, video_path=None, telematics_path=None, dual_camera=False):
    super().__init__(dual_camera)

    self.telematics_path = telematics_path
    self.t0_world = time()
    self.telematics_data = pd.read_csv(self.telematics_path)
    self.video_frame = 0

    # load video file using opencv
    self.video = VideoReader(video_path)
    self.csv_logger = CsvLogger(str(telematics_path) + '.out.csv',
                                buffer_size = 200,
                                header = ['logging_time', 'frame_nr'] + HEADER_META,
                                )

    if dual_camera:
      video_path_wide = video_path.with_name(video_path.stem + '_wide' + video_path.suffix)
      self.video_wide = VideoReader(video_path_wide)

    self.road_image = np.zeros((H, W, 3), dtype=np.uint8)
    self.wide_road_image = np.zeros((H, W, 3), dtype=np.uint8)
    self.max_steer_angle = MAX_STEER_ANGLE

    self.sm = messaging.SubMaster(['carControl', 'controlsState', 'modelV2'])


  def apply_controls(self, steer_angle, throttle_out, brake_out):
    # in the simulator mode, this is used to apply controls to the simulated vehicle.
    pass


  def read_sensors(self, state:SimulatorState):
    frame_data = self.telematics_data.iloc[self.video_frame]
    state.velocity = vec3(float(frame_data.vehicle_speed), 0., 0.)
    state.bearing = frame_data.yaw
    state.steering_angle = frame_data.steer * self.max_steer_angle
    state.gps.from_xy([frame_data.position_x, frame_data.position_y])
    state.imu.accelerometer = vec3(float(frame_data.accel_x), float(frame_data.accel_y), float(frame_data.accel_z))
    state.imu.gyroscope = vec3(float(frame_data.gyro_x), float(frame_data.gyro_y), float(frame_data.gyro_z))
    state.user_gas = frame_data.throttle
    state.user_brake = frame_data.brake
    state.valid=True
    # state.user_torque = 0 # currently set to 0 as not recorded in carla
    # state.left_blinker = False # currently set to False as not recorded in carla
    # state.right_blinker = False # currently set to False as not recorded in carla

  def read_cameras(self):
    self.road_image = self.video.read()
    if self.dual_camera:
      self.wide_road_image = self.video_wide.read()

  def tick(self):
    self.video_frame += 1

  def reset(self):
    pass

  def close(self):
    pass

  def log_openpilot_data(self, simulator_state: SimulatorState):
    # see cereal/log.capnp for the structure of the messages
    self.sm.update()

    meta_keys, meta_values = parse_struct(self.sm['modelV2'].meta.to_dict())
    if meta_keys == HEADER_META: # if expected format
      csv_line = [time()] + [self.video_frame] + meta_values
      self.csv_logger.log(csv_line)
    else: 
      print(f"Not logging frame {self.video_frame}; metadata in unexpected format")