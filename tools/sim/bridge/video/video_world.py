import ctypes
import numpy as np
import pandas as pd
import cv2 

from multiprocessing import Pipe, Array

from openpilot.tools.sim.lib.camerad import W, H
from openpilot.tools.sim.bridge.common import World
from openpilot.tools.sim.lib.common import SimulatorState, vec3
from pathlib import Path

import cereal.messaging as messaging

MAX_STEER_ANGLE = 0.5

class VideoReader:
  def __init__(self, video_path):
    print(video_path)
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
  # a class to log openpilot data to a csv file, in a buffered io fashion.
  # log_data should be
  def __init__(self, csv_out, buffer_size=1000):
    self.csv_out = csv_out
    self.csv_buffer = []
    self.csv_buffer_size = buffer_size
    self.csv_buffer_counter = 0
  
  def log(self, log_data):
    self.csv_buffer.append(log_data)
    self.csv_buffer_counter += 1
    if self.csv_buffer_counter >= self.csv_buffer_size:
      self.flush()
      self.csv_buffer_counter = 0
  
  def flush(self):
    with open(self.csv_out, 'a') as f:
      for row in self.csv_buffer:
        f.write(','.join([str(x) for x in row]) + '\n')
    self.csv_buffer = []
    print('flushed csv buffer')
    

class VideoWorld(World):
  def __init__(self, video_path=None, telematics_path=None, dual_camera=False):
    super().__init__(dual_camera)
    # self.camera_array = Array(ctypes.c_uint8, W*H*3)
    # self.road_image = np.frombuffer(self.camera_array.get_obj(), dtype=np.uint8).reshape((H, W, 3))
    self.telematics_path = telematics_path
    
    self.telematics_data = pd.read_csv(self.telematics_path)
    self.video_frame = 0

    # load video file using opencv
    self.video = VideoReader(video_path)

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
    # state.velocity = vec3(1,1,1)
    state.bearing = frame_data.yaw
    state.steering_angle = frame_data.steer * self.max_steer_angle
    state.gps.from_xy([frame_data.position_x, frame_data.position_y])
    
    # print(frame_data.accel_x, frame_data.accel_y, frame_data.accel_z)
    
    state.imu.accelerometer = vec3(float(frame_data.accel_x), float(frame_data.accel_y), float(frame_data.accel_z))
    state.imu.gyroscope = vec3(float(frame_data.gyro_x), float(frame_data.gyro_y), float(frame_data.gyro_z))
      
    state.user_gas = frame_data.throttle
    state.user_brake = frame_data.brake
    state.valid=True
    # state.user_torque = frame_data.torque # NOT RECORDED YET
    # state.left_blinker = True
    # state.right_blinker = True    
    pass
  
  
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
    
    ## create a row with all relevant data, 
    csv_out = str(self.telematics_path) + '.out.csv'
    # TODO gas and brake is deprecated
    # print(sm['carControl'])

    steer_op = self.sm['carControl'].actuators.steer
    angle_op = self.sm['carControl'].actuators.steeringAngleDeg
    curvature_op = self.sm['carControl'].actuators.curvature
    throttle_op = self.sm['carControl'].actuators.gas
    brake_op = self.sm['carControl'].actuators.brake
    accel_op = self.sm['carControl'].actuators.accel
    speed_op = self.sm['carControl'].actuators.speed

      # if self._camerad.frame_id > previous_frame: #logging data per frame
    model_meta = self.sm['modelV2'].meta.to_dict()
    try: 
      # Extract data from the dictionary
      # t = model_meta["disengagePredictions"]["t"]
      

      
      
      brake_probs = model_meta["disengagePredictions"]["brakeDisengageProbs"]
      gas_probs = model_meta["disengagePredictions"]["gasDisengageProbs"]
      steer_probs = model_meta["disengagePredictions"]["steerOverrideProbs"]
      brake_3mps_probs = model_meta["disengagePredictions"]["brake3MetersPerSecondSquaredProbs"]
      brake_4mps_probs = model_meta["disengagePredictions"]["brake4MetersPerSecondSquaredProbs"]
      brake_5mps_probs = model_meta["disengagePredictions"]["brake5MetersPerSecondSquaredProbs"]
      hard_brake_probs = model_meta["hardBrakePredicted"]

    except Exception as e:
      brake_5mps_probs = [0.0,0.0,0.0,0.0,0.0]
      hard_brake_probs = False
      print(e)

    # log_data = np.array([self._camerad.frame_id, steer_op, angle_op, 
    #                       curvature_op, throttle_op, brake_op, 
    #                       accel_op, speed_op, hard_brake_probs])
    # log_data = np.append(log_data,brake_5mps_probs)
    
    # previous_frame = self._camerad.frame_id
    


    # print(csv_out)
    


        

        