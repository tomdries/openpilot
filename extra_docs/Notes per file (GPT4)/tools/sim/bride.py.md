# Carla Bridge

This script is a bridge between the CARLA simulator and openpilot. It allows openpilot to control a vehicle in the CARLA simulator and receive sensor data from the simulator.

## Usage

```bash
python bridge.py [--joystick] [--high_quality] [--dual_camera] [--town TOWN_NAME] [--spawn_point SPAWN_POINT] [--host HOST] [--port PORT]
```

## Arguments

- `--joystick`: Use a joystick for manual control.
- `--high_quality`: Use high quality graphics.
- `--dual_camera`: Use dual cameras.
- `--town`: The name of the town in CARLA to use. Default is 'Town04_Opt'.
- `--spawn_point`: The spawn point to use. Default is 16.
- `--host`: The host to connect to. Default is '127.0.0.1'.
- `--port`: The port to connect to. Default is 2000.

## Classes

### `VehicleState`

This class represents the state of the vehicle. It includes the speed, angle, bearing, velocity, cruise button state, engagement state, and ignition state.

### `Camerad`

This class handles the camera data. It converts the RGB images from the CARLA simulator to YUV format and sends them to openpilot.

### `CarlaBridge`

This class is the main class that handles the communication between CARLA and openpilot. It sets up the CARLA simulator, spawns the vehicle and sensors, and starts the threads for sending data to openpilot.

## Functions

- `parse_args(add_args=None)`: Parses the command line arguments.
- `steer_rate_limit(old, new)`: Limits the rate of change of the steering angle.
- `imu_callback(imu, vehicle_state)`: Callback function for the IMU sensor.
- `panda_state_function(vs: VehicleState, exit_event: threading.Event)`: Sends the panda state to openpilot.
- `peripheral_state_function(exit_event: threading.Event)`: Sends the peripheral state to openpilot.
- `gps_callback(gps, vehicle_state)`: Callback function for the GPS sensor.
- `fake_driver_monitoring(exit_event: threading.Event)`: Sends fake driver monitoring data to openpilot.
- `can_function_runner(vs: VehicleState, exit_event: threading.Event)`: Sends CAN messages to openpilot.
- `connect_carla_client(host: str, port: int)`: Connects to the CARLA server.

## Main Execution

If the script is run as the main program, it starts the CarlaBridge and either the joystick or keyboard control thread, depending on the command line arguments.