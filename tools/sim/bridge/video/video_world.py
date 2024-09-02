import numpy as np
import pandas as pd
import cv2
import csv
from time import time
from openpilot.tools.sim.lib.camerad import W, H
from openpilot.tools.sim.lib.video_helpers import parse_struct, HEADER_META, HEADER_CALIBRATION, HEADER_LATERALPLAN, HEADER_LONGITUDINALPLAN, HEADER_CARSTATE
from openpilot.tools.sim.bridge.common import World
from openpilot.tools.sim.lib.common import SimulatorState, vec3
import cereal.messaging as messaging

MAX_STEER_ANGLE = 0.5

class VideoReader:
    def __init__(self, video_path, t_start):
        self.video_file = cv2.VideoCapture(str(video_path))
        if not self.video_file.isOpened():
            raise ValueError("Error opening video file")

        fps = self.video_file.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            raise ValueError("Could not determine video frame rate")
        self.start_frame = int(fps * t_start)
        self.video_file.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

        ret, self.frame = self.video_file.read()

        if not ret:
            raise ValueError("Could not read the first frame of the video")

    def read(self):
        ret, frame = self.video_file.read()
        if ret:
            return frame
        else:
            print("End of video")
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
  def __init__(self, video_path=None, telematics_path=None, t_start=0, dual_camera=False):
    super().__init__(dual_camera)
    self.t0_world = time()
    if telematics_path is not None:
      self.telematics_path = telematics_path
      self.telematics_data = pd.read_csv(self.telematics_path)
      ALLOWED_TELEMATICS_COLUMNS = ['frame', 'vehicle_speed', 'steer', 'throttle', 'brake', 'yaw', 'position_x', 'position_y',
                                    'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'blinker_left', 'blinker_right']
      columns = [x for x in self.telematics_data.columns if x in ALLOWED_TELEMATICS_COLUMNS]
      self.telematics_data = self.telematics_data[columns]

    # load video file using opencv
    self.video = VideoReader(video_path, t_start)
    self.video_frame = self.video.start_frame

    csv_header = (
                 ['logging_time', 'frame_nr']
                 + [f'meta.{x}' for x in HEADER_META]
                 + [f'longitudinalPlan.{x}' for x in HEADER_LONGITUDINALPLAN]
                 + [f'lateralPlan.{x}' for x in HEADER_LATERALPLAN]
                 + ['lead1', 'lead2', 'lead3']
                 + ['vEgo']
                 + ['leftBlinker']
                 + ['rightBlinker']
    )

    self.csv_logger = CsvLogger(str(telematics_path) + '.out.csv',
                                buffer_size = 200,
                                header = csv_header
                                )

    self.calibration_logger = CsvLogger(str(telematics_path) + '.calibration.csv',
                                        buffer_size = 50,
                                        header = ['logging_time', 'frame_nr'] + HEADER_CALIBRATION,
                                        )

    if dual_camera:
      video_path_wide = video_path.with_name(video_path.stem + '_wide' + video_path.suffix)
      self.video_wide = VideoReader(video_path_wide, t_start)

    self.road_image = np.zeros((H, W, 3), dtype=np.uint8)
    self.wide_road_image = np.zeros((H, W, 3), dtype=np.uint8)
    self.max_steer_angle = MAX_STEER_ANGLE
    self.sm = messaging.SubMaster(['carState','carControl','lateralPlan','longitudinalPlan', 'controlsState', 'modelV2', 'liveCalibration'])

    if telematics_path is not None:
      print(f"VideoWorld initialized with telematics data: {self.telematics_data.columns.values}")
    else:
      print("VideoWorld initialized without telematics data")

  def apply_controls(self, steer_angle, throttle_out, brake_out):
    # in the simulator mode, this is used to apply controls to the simulated vehicle.
    pass

  def read_sensors(self, state:SimulatorState):
    state.is_engaged = True
    state.valid=True

    if self.video_frame < len(self.telematics_data):
      state.is_engaged = True # sets openpilot to be engaged as driving, test this feature
      state.valid=True

      frame_data = self.telematics_data.iloc[self.video_frame]
      if "vehicle_speed" in frame_data:
        state.velocity = vec3(float(frame_data.vehicle_speed), 0., 0.)
      if "yaw" in frame_data:
        state.bearing = frame_data.yaw
      if "steer" in frame_data:
        state.steering_angle = frame_data.steer * self.max_steer_angle
      if "position_x" in frame_data:
        state.gps.from_xy([frame_data.position_x, frame_data.position_y])
      if "accel_x" in frame_data:
        state.imu.accelerometer = vec3(float(frame_data.accel_x), float(frame_data.accel_y), float(frame_data.accel_z))
      if "gyro_x" in frame_data:
        state.imu.gyroscope = vec3(float(frame_data.gyro_x), float(frame_data.gyro_y), float(frame_data.gyro_z))
      if "throttle" in frame_data:
        state.user_gas = frame_data.throttle
      if "brake" in frame_data:
        state.user_brake = frame_data.brake
      if "torque" in frame_data:
        state.user_torque = frame_data.torque # currently set to 0 as not recorded in carla
      if "blinker_left" in frame_data:
        state.left_blinker = frame_data.blinker_left
        state.right_blinker = frame_data.blinker_right
    else:
      self.close()

  def read_cameras(self):
    self.road_image = self.video.read()
    if self.dual_camera:
      self.wide_road_image = self.video_wide.read()

  def tick(self):
    self.video_frame += 1

  def reset(self):
    pass

  def close(self):
      self.csv_logger.flush()
      print("World closed")

  def log_openpilot_data(self, simulator_state: SimulatorState):
    # see cereal/log.capnp for the structure of the messages
    self.sm.update()

    # calibration logging
    calibration_log_freq = 10
    if self.video_frame % calibration_log_freq == 0:
      csv_line_calib = [time()] + [self.video_frame] + [str(self.sm['liveCalibration'].calStatus),
                                                        self.sm['liveCalibration'].calCycle,
                                                        self.sm['liveCalibration'].calPerc,
                                                        self.sm['liveCalibration'].validBlocks,
                                                        str(self.sm['liveCalibration'].extrinsicMatrix),
                                                        str(self.sm['liveCalibration'].rpyCalib),
                                                        str(self.sm['liveCalibration'].rpyCalibSpread),
                                                        str(self.sm['liveCalibration'].wideFromDeviceEuler),
                                                        str(self.sm['liveCalibration'].height)]
      self.calibration_logger.log(csv_line_calib)

    # meta logging
    meta_keys, meta_values = parse_struct(self.sm['modelV2'].meta.to_dict())
    longitudinalplan_keys, longitudinalplan_values = parse_struct(self.sm['longitudinalPlan'].to_dict(),remove_deprecated=True)
    lateralplan_keys, lateralplan_values = parse_struct(self.sm['lateralPlan'].to_dict(),remove_deprecated=True)


    csv_line = [time()] + [self.video_frame]

    if meta_keys == HEADER_META: # if expected format
       csv_line += meta_values
    else:
       csv_line += ['header mismatch']*len(HEADER_META)

    if longitudinalplan_keys == HEADER_LONGITUDINALPLAN:
      csv_line += longitudinalplan_values
    else:
      csv_line += ['header mismatch']*len(HEADER_LONGITUDINALPLAN)

    if lateralplan_keys == HEADER_LATERALPLAN:
      csv_line += lateralplan_values
    else:
      csv_line += ['header mismatch']*len(HEADER_LATERALPLAN)

    # leads
    if len(self.sm['modelV2'].leadsV3) > 0:
      lead1 = str(self.sm['modelV2'].leadsV3[0].to_dict())
      lead2 = str(self.sm['modelV2'].leadsV3[1].to_dict())
      lead3 = str(self.sm['modelV2'].leadsV3[2].to_dict())
      csv_line += [lead1, lead2, lead3]
    else:
      csv_line += ['']*3

    csv_line += [self.sm['carState'].vEgo]
    csv_line += [self.sm['carState'].leftBlinker]
    csv_line += [self.sm['carState'].rightBlinker]

    self.csv_logger.log(csv_line)

