HEADER_META=['engagedProb', 'desirePrediction_0', 'desirePrediction_1', 'desirePrediction_2', 'desirePrediction_3', 'desirePrediction_4', 'desirePrediction_5', 'desirePrediction_6', 'desirePrediction_7', 'desirePrediction_8', 'desirePrediction_9', 'desirePrediction_10', 'desirePrediction_11', 'desirePrediction_12', 'desirePrediction_13', 'desirePrediction_14', 'desirePrediction_15', 'desirePrediction_16', 'desirePrediction_17', 'desirePrediction_18', 'desirePrediction_19', 'desirePrediction_20', 'desirePrediction_21', 'desirePrediction_22', 'desirePrediction_23', 'desirePrediction_24', 'desirePrediction_25', 'desirePrediction_26', 'desirePrediction_27', 'desirePrediction_28', 'desirePrediction_29', 'desirePrediction_30', 'desirePrediction_31', 'brakeDisengageProbDEPRECATED', 'gasDisengageProbDEPRECATED', 'steerOverrideProbDEPRECATED', 'desireState_0', 'desireState_1', 'desireState_2', 'desireState_3', 'desireState_4', 'desireState_5', 'desireState_6', 'desireState_7', 'disengagePredictions_t_0', 'disengagePredictions_t_1', 'disengagePredictions_t_2', 'disengagePredictions_t_3', 'disengagePredictions_t_4', 'disengagePredictions_brakeDisengageProbs_0', 'disengagePredictions_brakeDisengageProbs_1', 'disengagePredictions_brakeDisengageProbs_2', 'disengagePredictions_brakeDisengageProbs_3', 'disengagePredictions_brakeDisengageProbs_4', 'disengagePredictions_gasDisengageProbs_0', 'disengagePredictions_gasDisengageProbs_1', 'disengagePredictions_gasDisengageProbs_2', 'disengagePredictions_gasDisengageProbs_3', 'disengagePredictions_gasDisengageProbs_4', 'disengagePredictions_steerOverrideProbs_0', 'disengagePredictions_steerOverrideProbs_1', 'disengagePredictions_steerOverrideProbs_2', 'disengagePredictions_steerOverrideProbs_3', 'disengagePredictions_steerOverrideProbs_4', 'disengagePredictions_brake3MetersPerSecondSquaredProbs_0', 'disengagePredictions_brake3MetersPerSecondSquaredProbs_1', 'disengagePredictions_brake3MetersPerSecondSquaredProbs_2', 'disengagePredictions_brake3MetersPerSecondSquaredProbs_3', 'disengagePredictions_brake3MetersPerSecondSquaredProbs_4', 'disengagePredictions_brake4MetersPerSecondSquaredProbs_0', 'disengagePredictions_brake4MetersPerSecondSquaredProbs_1', 'disengagePredictions_brake4MetersPerSecondSquaredProbs_2', 'disengagePredictions_brake4MetersPerSecondSquaredProbs_3', 'disengagePredictions_brake4MetersPerSecondSquaredProbs_4', 'disengagePredictions_brake5MetersPerSecondSquaredProbs_0', 'disengagePredictions_brake5MetersPerSecondSquaredProbs_1', 'disengagePredictions_brake5MetersPerSecondSquaredProbs_2', 'disengagePredictions_brake5MetersPerSecondSquaredProbs_3', 'disengagePredictions_brake5MetersPerSecondSquaredProbs_4', 'hardBrakePredicted']

HEADER_CALIBRATION=['calStatus', ' calCycle', 'calPerc', 'validBlocks', 'extrinsicMatrix', 'rpyCalib', 'rpyCalibSpread', 'wideFromDeviceEuler','height']

import cv2

# class VideoReader:
#   def __init__(self, video_path):
#     self.video_file = cv2.VideoCapture(str(video_path))
#     if not self.video_file.isOpened():
#       raise ValueError("Error opening video file")
#     self.frame = 0

#   def read(self, shape_out = (H,W)):
#     self.frame += 1
#     ret, frame = self.video_file.read()
#     if ret:
#       # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#       frame_rgb = frame
#       print(frame_rgb.shape)
#       return frame_rgb
#     else:
#       self.close()
#       return None

#   def close(self):
#     self.video_file.release()

# class VideoReader:
#     def __init__(self, video_path, output_width, output_height):
#         self.video_file = cv2.VideoCapture(str(video_path))
#         if not self.video_file.isOpened():
#             raise ValueError("Error opening video file")
#         self.frame = 0
#         # Desired output dimensions
#         self.output_height = output_height
#         self.output_width = output_width

#     def read(self, method="stretch"):
#         self.frame += 1
#         ret, frame = self.video_file.read()
#         if ret:
#             # Optionally convert to RGB
#             # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame_rgb = frame
#             # Check if resizing is necessary
#             if frame_rgb.shape[1] == self.output_width and frame_rgb.shape[0] == self.output_height:
#                 return frame_rgb  # Return the original frame if it already matches the target dimensions
#             # Resize the frame based on the method
#             resized_frame = self.resize_frame(frame_rgb, self.output_width, self.output_height, method)
#             return resized_frame
#         else:
#             self.close()
#             return None

#     def resize_frame(self, frame, width, height, method):
#         if method == "stretch":
#             # Stretch the frame to the target dimensions
#             resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
#         elif method == "crop":
#             # Maintain the aspect ratio and crop the excess
#             resized_frame = self.crop_to_aspect_ratio(frame, width, height)
#         else:
#             raise ValueError("Invalid resize method specified")
#         return resized_frame

#     def crop_to_aspect_ratio(self, frame, target_width, target_height):
#         original_height, original_width = frame.shape[:2]
#         target_aspect = target_width / target_height
#         original_aspect = original_width / original_height

#         if original_aspect > target_aspect:
#             # Crop the width
#             new_width = int(target_aspect * original_height)
#             offset = (original_width - new_width) // 2
#             cropped = frame[:, offset:offset+new_width]
#         else:
#             # Crop the height
#             new_height = int(original_width / target_aspect)
#             offset = (original_height - new_height) // 2
#             cropped = frame[offset:offset+new_height, :]
#         # Resize cropped image to target dimensions
#         resized_cropped = cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)
#         return resized_cropped

#     def close(self):
#         self.video_file.release()


def flatten_data(data, prefix=''):
    """
    Flatten nested dictionaries and lists into a flat dictionary where each key represents the path to the value.
    """
    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            items.extend(flatten_data(value, prefix=prefix + key + '_'))
    elif isinstance(data, list):
        for i, value in enumerate(data):
            items.extend(flatten_data(value, prefix=prefix + str(i) + '_'))
    else:
        items.append((prefix[:-1], data))

    return items


def parse_struct(data):
    items = flatten_data(data)
    header = [x[0] for x in items]
    values = [x[1] for x in items]
    return header, values
