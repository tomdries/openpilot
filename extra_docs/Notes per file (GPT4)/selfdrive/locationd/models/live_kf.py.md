# LiveKalman

This code defines a LiveKalman class that represents an Extended Kalman Filter (EKF) used for real-time vehicle state estimation. It is responsible for generating C++ code for the EKF and handling the filter's state and covariance matrices, process noise, and observation noise.

## Key Functions and Classes

### numpy2eigenstring(arr)
Converts a NumPy array into a string representation of an Eigen vector.

### States
This class defines slices for various states and state errors, which are used to access specific parts of the state and covariance matrices.

### LiveKalman
This class contains the initial state and covariance matrices, process noise, observation noise, and functions for generating C++ code for the EKF.

#### generate_code(generated_dir)
Generates C++ code for the EKF, including the state transition function, observation functions, and Jacobians. It also writes constants to a header file for use in the C++ code.

## Constants and Variables

### EARTH_GM
Gravitational constant times the mass of the Earth (m^3/s^2).

### initial_x
Initial state vector.

### initial_P_diag
Initial diagonal elements of the state covariance matrix.

### reset_orientation_diag
State covariance when resetting midway in a segment.

### fake_gps_pos_cov_diag, fake_gps_vel_cov_diag
Fake GPS position and velocity observation covariance, used to control the uncertainty estimate of the filter.

### Q_diag
Process noise covariance diagonal elements.

### obs_noise_diag
Dictionary containing observation noise for different observation types.

## Filter Model

The EKF state is composed of the following variables:
- ECEF position (x, y, z)
- ECEF orientation (quaternion)
- ECEF velocity (vx, vy, vz)
- Angular velocity (roll, pitch, yaw rates) in device frame
- Gyroscope bias (roll, pitch, yaw biases)
- Acceleration in device frame
- Accelerometer bias

The state transition function is derived from the time derivative of the state, which is a function of the state and the input control variables (angular velocity, acceleration, and biases). The state transition function is discretized using a first-order integrator.

The observation functions relate the state variables to the various types of observations, such as phone gyroscope, phone accelerometer, ECEF position, ECEF velocity, and ECEF orientation from GPS.

The Jacobians of the state transition function and observation functions are computed symbolically using the SymPy library, and the resulting expressions are used to generate C++ code for the EKF.