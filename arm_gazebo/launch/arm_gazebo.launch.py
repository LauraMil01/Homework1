from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
import xacro
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
    # Define paths to the launch files
    arm_gazebo_path = os.path.join(
        get_package_share_directory('arm_gazebo'),
        'launch',
        'arm_world.launch.py'
    )
    arm_control_path = os.path.join(
        get_package_share_directory('arm_control'),
        'launch',
        'arm_control.launch.py'
    )

    return LaunchDescription([
        # Launch the Gazebo world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(arm_gazebo_path)
        ),
        
        # Launch the arm controllers in the "arm" namespace
        GroupAction([
            PushRosNamespace('arm'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(arm_control_path)
            ),
        ]),
    ])
