from openpilot.tools.sim.bridge.common import SimulatorBridge
from openpilot.tools.sim.bridge.video.video_world import VideoWorld
from pathlib import Path


class VideoBridge(SimulatorBridge):

  def __init__(self, arguments):
    super().__init__(arguments)
    self.video_file = Path(arguments.video_file)

    # self.telematics_file = self.video_file.with_name(self.video_file.stem + '.csv')

    if arguments.telematics_file is None:
      self.telematics_file = None
    else:
      self.telematics_file = Path(arguments.telematics_file)

    self.t0= arguments.t0

    # self.sm = messaging.SubMaster(['modelV2', 'carState'])

    # other init things (self.xxx)

  def spawn_world(self):
    return VideoWorld(self.video_file, self.telematics_file, self.t0, dual_camera=self.dual_camera)

  def print_status(self):
    pass

