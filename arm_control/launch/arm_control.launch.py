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

def generate_launch_description():
    declared_arguments = []

    arm_control_path = os.path.join(
        get_package_share_directory('arm_control'))

  
    declared_arguments.append(
        DeclareLaunchArgument(
            'config',
            default_value= os.path.join(
                arm_control_path,
                'config',
                'arm_control.yaml'
            ),
            description='YAML configuration file'
        ),
    )


    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    ) #among the controller of controller_manager you are saying to launchg the joint_state_broadcaster

    JointPositionController = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["JointPositionController", "--controller-manager", "/controller_manager"],  
    ) 
   
    #teoricamente il prof non li fa partire
    nodes_to_start = [
        joint_state_broadcaster,
        JointPositionController
    ]



    return LaunchDescription(declared_arguments + nodes_to_start) 
