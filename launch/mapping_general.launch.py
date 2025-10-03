#!/usr/bin/python3
# -- coding: utf-8 --**

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    
    # Find path
    config_file_dir = os.path.join(get_package_share_directory("fast_livo"), "config")
    rviz_config_file = os.path.join(get_package_share_directory("fast_livo"), "rviz_cfg", "ntu_viral.rviz")

    #Load parameters
    config_cmd = os.path.join(config_file_dir, "NTU_VIRAL.yaml")
    cam_config_cmd = os.path.join(config_file_dir, "camera_NTU_VIRAL.yaml")

    # Param use_rviz
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="False",
        description="Whether to launch Rviz2",
    )

    config_arg = DeclareLaunchArgument(
        'params_file',
        default_value=config_cmd,
        description='Full path to the ROS2 parameters file to use for fast_livo2 nodes',
    )
    cam_config_arg = DeclareLaunchArgument(
        'cam_params_file',
        default_value=cam_config_cmd,
        description='Full path to the ROS2 camera parameters file to use for fast_livo2 nodes',
    )

    params_file = LaunchConfiguration('params_file')
    cam_params_file = LaunchConfiguration('cam_params_file')

    return LaunchDescription([
        use_rviz_arg,
        config_arg,
        cam_config_arg,

        Node(
            package="fast_livo",
            executable="fastlivo_mapping",
            name="laserMapping",
            parameters=[
                params_file,
                cam_params_file,
                {"use_sim_time": True},
            ],
            output="screen"
        ),

        Node(
            condition=IfCondition(LaunchConfiguration("use_rviz")),
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
            output="screen"
        ),
    ])
