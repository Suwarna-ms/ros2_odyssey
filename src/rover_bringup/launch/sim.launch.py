import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    xacro_file = '/home/suwi/ros2_odyssey/src/rover_description/urdf/suwi_rover.xacro'
    doc = xacro.process_file(xacro_file)
    robot_description = {'robot_description': doc.toxml()}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        # THE FIX IS ON THIS LINE BELOW:
        parameters=[robot_description, {'use_sim_time': True}] 
    )
     
    world_path = '/home/suwi/ros2_odyssey/src/rover_bringup/worlds/suwi_maze.world'
    
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path],
        output='screen'
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'suwi_rover', '-z', '0.5'],
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity
    ])
