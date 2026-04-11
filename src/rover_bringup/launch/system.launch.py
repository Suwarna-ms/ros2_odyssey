from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        
        # 1. Start the Heartbeat Node
        Node(
            package='heartbeat_pkg',
            executable='health_talker',
            name='heartbeat',
            # REMAPPING: Change the topic name on the fly!
            remappings=[
                ('/heartbeat', '/system_status')
            ]
        ),
        
        # 2. Start the Parameter Tuning Node
        Node(
            package='parameters_py',
            executable='tune',
            name='robot_tuner',
            # We can even set parameters directly from the launch file!
            parameters=[
                {'robot_name': 'Suwi_Conductor_Rover'},
                {'max_speed': 15.0}
            ]
        )
    ])
