# Copyright 2024 The Autoware Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import json


def launch_setup(context, *args, **kwargs):
    """Return Launch Configuration for the TF between the lidar and the camera. """
    tf_file = LaunchConfiguration('tf_file_path').perform(context)
    with open(tf_file, 'r') as f:
        tf_data = json.load(f)

    return [
        Node(
            name="lidar_camera_tf_publisher",
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', str(tf_data['transform']['translation']['x']),
                '--y', str(tf_data['transform']['translation']['y']),
                '--z', str(tf_data['transform']['translation']['z']),
                '--qx', str(tf_data['transform']['rotation']['x']),
                '--qy', str(tf_data['transform']['rotation']['y']),
                '--qz', str(tf_data['transform']['rotation']['z']),
                '--qw', str(tf_data['transform']['rotation']['w']),
                '--frame-id', str(tf_data['header']['frame_id']),
                '--child-frame-id', str(tf_data['child_frame_id'])
            ]),
        Node(
            name="camera_optical_link_publisher",
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',
                '--y', '0.0',
                '--z', '0.0',
                '--qx', '0.5',
                '--qy', '-0.5',
                '--qz', '0.5',
                '--qw', '-0.5',
                '--frame-id', str(tf_data['child_frame_id']),
                '--child-frame-id', str(tf_data['child_frame_id'].replace('camera_link',
                                                                          'camera_optical_link'))
            ])
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("tf_file_path"),
            OpaqueFunction(function=launch_setup),
        ]
    )
