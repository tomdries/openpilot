# Code Documentation (GPT-3.5 16k model)

## Included Libraries
- sys/time.h: This library provides functions for working with time and timing functions.
- sys/resource.h: This library provides functions for manipulating process resource limits.
- cmath: This library provides mathematical functions and operations.
- locationd.h: This is a custom header file that contains class definitions and function declarations for the Localizer class.
- Eigen: This is a library for linear algebra and vector math.

## Namespaces
- EKFS: This namespace contains classes and functions specific to the Extended Kalman Filter System.
- Eigen: This namespace contains classes and functions for linear algebra and vector math.

## Global Variables
- ExitHandler do_exit: An instance of the ExitHandler class, used to handle program exits.
- Constants related to sanity checks and thresholds for various measurements: These variables represent various thresholds and constants used in the code for sanity checks and calculations.

## Helper Functions
- floatlist2vector: A helper function that converts a list of floats into a VectorXd object using Eigen library.
- quat2vector: A helper function that converts a Quaterniond object into a Vector4d object using Eigen library.
- vector2quat: A helper function that converts a VectorXd object into a Quaterniond object using Eigen library.
- init_measurement: A helper function that initializes a LiveLocationKalman::Measurement object with given values, standard deviations, and validity.
- rotate_cov: A helper function that rotates a covariance matrix by multiplying it with a rotation matrix.
- rotate_std: A helper function that rotates a vector of standard deviations by rotating the corresponding covariance matrix.

## Class: Localizer
### Constructors:
- Localizer(LocalizerGnssSource gnss_source): Initializes an instance of the Localizer class with the given GNSS source.

### Methods:
- build_live_location: Builds a LiveLocationKalman message object using the current state of the Kalman filter.
- get_position_geodetic: Returns the geodetic coordinates of the current position estimate.
- get_state: Returns the current state vector of the Kalman filter.
- get_stdev: Returns the standard deviations of the current state estimates.
- are_inputs_ok: Checks if the inputs from critical services are valid.
- observation_timings_invalid_reset: Resets the flag indicating invalid observation timings.
- handle_sensor: Handles incoming sensor readings, including accelerometer and gyroscope.
- input_fake_gps_observations: Generates fake GPS observations to prevent the error estimate of the position from blowing up in the absence of GPS fix.
- handle_gps: Handles incoming GPS location data from either Quectel or Ublox GPS sensor.
- handle_gnss: (Currently commented out) Handles incoming GNSS measurements from either Quectel or Ublox GNSS receiver.
- handle_car_state: Handles incoming car state data, including the vehicle speed and standstill status.
- handle_cam_odo: Handles incoming camera odometry data.
- handle_live_calib: Handles incoming live calibration data.
- reset_kalman: Resets the Kalman filter by initializing the state vector and covariance matrix.
- finite_check: Checks if there are any non-finite values in the state vector or covariance matrix, and performs a reset if necessary.
- time_check: Checks if there is a large gap in time between the current time and the filter time, and performs a reset if necessary.
- update_reset_tracker: Updates the reset tracker variable, which keeps track of the number of resets performed.
- handle_msg_bytes: Handles incoming message data in byte format.
- handle_msg: Handles incoming message data in cereal::Event format.
- is_gps_ok: Checks if the GPS fix is considered valid based on the time since the last GPS message.
- critical_services_valid: Checks if the inputs from critical services are valid (based on the input_invalid_threshold).
- is_timestamp_valid: Checks if the current observation timestamp is valid based on the filter time.
- determine_gps_mode: Determines the GPS mode based on the current position standard deviation and the current GPS mode.
- configure_gnss_source: Configures the GNSS source for the localizer based on the LocalizerGnssSource enum value passed as argument.
- locationd_thread: The main thread function for the Localizer class, which handles incoming messages and updates the Kalman filter.

## Main Function
- The main function creates an instance of the Localizer class and starts the locationd_thread function. It also sets the real-time priority of the program to 5.