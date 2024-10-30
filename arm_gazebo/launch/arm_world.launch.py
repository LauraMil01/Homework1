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

    arm_description_path = os.path.join(
        get_package_share_directory('arm_gazebo'))
  
    urdf_arm = os.path.join(arm_description_path, "urdf", "arm.urdf.xacro")

    robot_description_arm = {"robot_description": Command(['xacro ', urdf_arm])}
 
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    
   
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description_arm,
                    {"use_sim_time": True},
            ],
        remappings=[('/robot_description', '/robot_description')]
    )
    

    declared_arguments.append(DeclareLaunchArgument('gz_args', default_value='-r -v 1 empty.sdf',
                              description='Arguments for gz_sim'),)
    
    gazebo_ignition = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                                    'launch',
                                    'gz_sim.launch.py'])]),
            launch_arguments={'gz_args': LaunchConfiguration('gz_args')}.items()
    )

    position = [0.0, 0.0, 0.025]

    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'arm',
                   '-allow_renaming', 'true',
                    "-x", str(position[0]),
                    "-y", str(position[1]),
                    "-z", str(position[2]),],
    )
 
    ign = [gazebo_ignition, gz_spawn_entity]

    #GAZEBO CLASSIC
    gazebo_classic = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("gazebo_ros"), "/launch", "/gazebo.launch.py"]),
        launch_arguments={"gui": "True", 'paused': 'False'}.items(),
    )
    position = [0.0, 0.0, 0.025]
    # Spawn robot. Each argument passed must be a string
    gazeboClassic_spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_entity",
        arguments=["-entity", "monopod", #arguments must always be string because strings are the argument passed by cli
                    "-x", str(position[0]),
                    "-y", str(position[1]),
                    "-z", str(position[2]),
                    '-topic', '/robot_description'],
        output="screen", #-file needs the path, not the string
    )

    classic = [gazebo_classic, gazeboClassic_spawn_robot]
    
    bridge_camera = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '--ros-args', 
            '-r', '/camera:=/videocamera',
        ],
        output='screen'
    )
    
    
    nodes_to_start = [
        #joint_state_publisher_node,
        robot_state_publisher_node,  
        *ign,
        bridge_camera
    ]

    return LaunchDescription(declared_arguments + nodes_to_start) 
