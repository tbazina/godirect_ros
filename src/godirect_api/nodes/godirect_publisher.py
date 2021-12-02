#!/usr/bin/env python
## Configure and capture grip force signal from Vernier Go Direct Hand
# Dynamometer device. Stream acquired force signal to the topic grip_force_stream.

import rospy
import traceback
from godirect_api.gdx_class import gdx
from godirect_ros.msg import GripForce

def publish_grip_force():
  """
  Configure and capture grip force signal from Vernier Go Direct Hand
  Dynamometer device. Stream acquired force signal to the topic grip_force_stream.

  ROS parameters:
    device_name (str): Dynamometer name and ID
    selected_sensor (int): Sensor to sample (works only for 1 - Force)
    sampling_rate (int): Dynamometer sampling rate (max 1000 Hz)
    zero_signal (bool): Use first 0.5 sec to zero the response
    queue_size (int): Size of the queue for asynchronous publishing on topic
  """
  # Initialize node and Publisher
  rospy.init_node(
    'godirect_publisher',
    anonymous=False,
    log_level=rospy.DEBUG,
    )
  try:
    # Get godirect parameters
    device_name = rospy.get_param('~device_name')
    selected_sensor = rospy.get_param('~selected_sensor', 1) # Force
    measurement_type = rospy.get_param('~measurement_type', 'grip') # grip/pinch
    sampling_rate = rospy.get_param('~sampling_rate', 50) # Hz
    calibrate_signal = rospy.get_param('~calibrate_signal', 0.5)
    queue_size = rospy.get_param('~queue_size', 10)
    # Initialize publisher with queue size
    pub = rospy.Publisher('grip_force_stream', GripForce, queue_size=queue_size)
    ####################################
    # Initialize GDX-HD
    Gdx = gdx(device_name)
    with Gdx as gdx_hd:
      # Return the device info
      gdx_hd.device_info()
      # Activate Force sensor
      gdx_hd.select_sensors(sensors=selected_sensor)
      # Return selected sensor info
      gdx_hd.enabled_sensor_info()
      # Start collecting data from selected sensor
      gdx_hd.start(sampling_rate=sampling_rate) 
      # Calibrate sensors
      gdx_hd.calibrate_sensor(seconds=calibrate_signal)
      # Read and publish data points to topic
      gdx_hd.read(publisher=pub, measurement_type=measurement_type)
  except rospy.ROSInterruptException:
    rospy.logwarn('User interrupted execution!')
  except rospy.ROSException:
    rospy.logerr("Could not get parameter names!")
  except Exception as e:
    rospy.logerr(f'Caught Exception: {e}\nExiting!')
    rospy.logerr(traceback.format_exc())