import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 1. Path to your custom map and params
    map_file = '/home/suwi/ros2_odyssey/full_maze.yaml'
    params_file = '/home/suwi/ros2_odyssey/my_nav2_params.yaml'

    # 2. Get the paths to the official launch files
    rover_bringup_dir = FindPackageShare('rover_bringup').find('rover_bringup')
    nav2_bringup_dir = FindPackageShare('nav2_bringup').find('nav2_bringup')
    slam_toolbox_dir = FindPackageShare('slam_toolbox').find('slam_toolbox')

    # 3. Define the Physics/Gazebo Launch
    physics_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rover_bringup_dir,'launch', 'sim.launch.py'))
    )
    #define slamtoolbox
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')),
        launch_arguments={'use_sim_time': 'True'}.items()
    )

    # 4. Define the Nav2 Brain Launch
    brain_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'use_sim_time': 'True',
            'map': map_file,
            'params_file': params_file,
            'cmd_vel_topic': '/cmd_vel'
        }.items()
    )

    # 5. Define the RViz Eyes Launch (Delayed by 5 seconds to let the brain wake up)
    rviz_cmd = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    rviz_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'rviz_launch.py')),
                launch_arguments={'namespace': '', 'use_namespace': 'False', 'rviz_config': rviz_cmd}.items()
            )
        ]
    )

    # Create the launch description and populate
    ld = LaunchDescription()
    ld.add_action(physics_launch)
    ld.add_action(slam_launch)
    ld.add_action(brain_launch)
    ld.add_action(rviz_launch)

    return ld
