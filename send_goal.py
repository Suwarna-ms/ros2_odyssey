#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class AutonomousCommander(Node):
    def __init__(self):
        super().__init__('autonomous_commander')
        # Create an Action Client that connects to the Nav2 brain
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_destination(self, x_coord, y_coord):
        self.get_logger().info('Waiting for Nav2 Brain to wake up...')
        self.action_client.wait_for_server()

        self.get_logger().info(f'Brain Found! Calculating route to X: {x_coord}, Y: {y_coord}...')
        
        # Create the Goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        # Set the X and Y coordinates
        goal_msg.pose.pose.position.x = float(x_coord)
        goal_msg.pose.pose.position.y = float(y_coord)
        
        # Set orientation (W=1.0 means face straight ahead)
        goal_msg.pose.pose.orientation.w = 1.0 

        # Send the goal to Nav2
        self.send_goal_future = self.action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Nav2 REJECTED the route! (Is it in a wall?)')
            return

        self.get_logger().info('Nav2 ACCEPTED the route! Driving now...')

def main(args=None):
    rclpy.init(args=args)
    
    # Start the node
    node = AutonomousCommander()
    
    # ==============================================================
    # MISSION COMMAND: Change these numbers to change the destination!
    # X and Y are in meters relative to the center of your map.
    # ==============================================================
    node.send_destination(x_coord=2.0, y_coord=1.0) 
    
    # Keep the script running while the robot drives
    rclpy.spin(node)

if __name__ == '__main__':
    main()
