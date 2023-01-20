# Adapted from https://github.com/stepjam/RLBench/blob/master/rlbench/utils.py

import os
import pickle
import numpy as np
from PIL import Image

from rlbench.backend.utils import image_to_float_array
from pyrep.objects import VisionSensor

import pprint

# constants
EPISODE_FOLDER = 'episode%d'

CAMERA_TOP = 'top'
CAMERA_FRONT = 'front'
CAMERA_SIDE_1 = 'side_1'
CAMERA_SIDE_2 = 'side_2'
CAMERAS = [CAMERA_TOP, CAMERA_FRONT, CAMERA_SIDE_1, CAMERA_SIDE_2]

IMAGE_RGB = 'rgb'
IMAGE_DEPTH = 'depth'
IMAGE_TYPES = [IMAGE_RGB, IMAGE_DEPTH]
IMAGE_FORMAT  = '%d.png'
LOW_DIM_PICKLE = 'obs.pkl'
VARIATION_NUMBER_PICKLE = 'variation_number.pkl'

DEPTH_SCALE = 255

# functions
def get_stored_demo(data_path, index):
  episode_path = os.path.join(data_path, EPISODE_FOLDER % index)
  
  # low dim pickle file
  with open(os.path.join(episode_path, LOW_DIM_PICKLE), 'rb') as f:
    obs = pickle.load(f)

#   print('Observation:')
#   pprint.pprint(obs[0])
#   pprint.pprint(obs[0].__dict__)

  num_steps = len(obs)
  for i in range(num_steps):
    obs[i].top_rgb = np.array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_TOP, IMAGE_RGB), IMAGE_FORMAT % i)))
    obs[i].front_rgb = np.array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_FRONT, IMAGE_RGB), IMAGE_FORMAT % i)))
    obs[i].side_1_rgb = np.array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_SIDE_1, IMAGE_RGB), IMAGE_FORMAT % i)))
    obs[i].side_2_rgb = np.array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_SIDE_2, IMAGE_RGB), IMAGE_FORMAT % i)))

    obs[i].top_depth = image_to_float_array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_TOP, IMAGE_DEPTH), IMAGE_FORMAT % i)), DEPTH_SCALE)
    near = obs[i].misc['%s_camera_near' % (CAMERA_TOP)]
    far = obs[i].misc['%s_camera_far' % (CAMERA_TOP)]
    obs[i].top_depth = near + obs[i].top_depth * (far - near)

    obs[i].front_depth = image_to_float_array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_FRONT, IMAGE_DEPTH), IMAGE_FORMAT % i)), DEPTH_SCALE)
    near = obs[i].misc['%s_camera_near' % (CAMERA_FRONT)]
    far = obs[i].misc['%s_camera_far' % (CAMERA_FRONT)]
    obs[i].front_depth = near + obs[i].front_depth * (far - near)

    obs[i].side_1_depth = image_to_float_array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_SIDE_1, IMAGE_DEPTH), IMAGE_FORMAT % i)), DEPTH_SCALE)
    near = obs[i].misc['%s_camera_near' % (CAMERA_SIDE_1)]
    far = obs[i].misc['%s_camera_far' % (CAMERA_SIDE_1)]
    obs[i].side_1_depth = near + obs[i].side_1_depth * (far - near)

    obs[i].side_2_depth = image_to_float_array(Image.open(os.path.join(episode_path, '%s_%s' % (CAMERA_SIDE_2, IMAGE_DEPTH), IMAGE_FORMAT % i)), DEPTH_SCALE)
    near = obs[i].misc['%s_camera_near' % (CAMERA_SIDE_2)]
    far = obs[i].misc['%s_camera_far' % (CAMERA_SIDE_2)]
    obs[i].side_2_depth = near + obs[i].side_2_depth * (far - near)

    obs[i].top_point_cloud = VisionSensor.pointcloud_from_depth_and_camera_params(obs[i].top_depth, 
                                                                                    obs[i].misc['top_camera_extrinsics'],
                                                                                    obs[i].misc['top_camera_intrinsics'])
    obs[i].front_point_cloud = VisionSensor.pointcloud_from_depth_and_camera_params(obs[i].front_depth, 
                                                                                            obs[i].misc['front_camera_extrinsics'],
                                                                                            obs[i].misc['front_camera_intrinsics'])
    obs[i].side_1_point_cloud = VisionSensor.pointcloud_from_depth_and_camera_params(obs[i].side_1_depth, 
                                                                                             obs[i].misc['side_1_camera_extrinsics'],
                                                                                             obs[i].misc['side_1_camera_intrinsics'])
    obs[i].side_2_point_cloud = VisionSensor.pointcloud_from_depth_and_camera_params(obs[i].side_2_depth, 
                                                                                           obs[i].misc['side_2_camera_extrinsics'],
                                                                                           obs[i].misc['side_2_camera_intrinsics'])
    
  return obs

obs = get_stored_demo('data', 0)
pprint.pprint(obs[0].__dict__)
