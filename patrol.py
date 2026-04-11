#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

# ==============================================================
# MISSION COMMAND: The Patrol Route
# Edit these (X, Y) coordinates to match safe spots on your map!
# ==============================================================
WAYPOINTS = [
    (2.0, 0.0),   # Stop 1
    (2.0, 2.0),   # Stop 2
    (0.0, 2.0),   # Stop 3
    (0.0, 0.0)    # Stop 4 (Returns home, then loops!)
]

class PatrolCommander(Node):
    def __init__(self):
        super().__init__('patrol_commander')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.current_waypoint_index = 0

    def start_patrol(self):
        self.get_logger().info('Waiting for Nav2 Brain...')
        self.action_client.wait_for_server()
        self.send_next_goal()

    def send_next_goal(self):
        # Get the current coordinate from the list
        x, y = WAYPOINTS[self.current_waypoint_index]
        self.get_logger().info(f'--- Driving to Waypoint {self.current_waypoint_index + 1}: X={x}, Y={y} ---')

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = float(x)
        goal_msg.pose.pose.position.y = float(y)
        goal_msg.pose.pose.orientation.w = 1.0 

        self.send_goal_future = self.action_client.send_goal_async(goal_msg)
        self.send_goal_future.add_done_callback(self.goal_accepted_callback)

    def goal_accepted_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Waypoint rejected! Stopping patrol.')
            return

        # Wait for the robot to actually arrive
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.goal_completed_callback)

    def goal_completed_callback(self, future):
        self.get_logger().info('Arrived at waypoint! Moving to the next one...')
        
        # Advance to the next waypoint, loop back to 0 if at the end
        self.current_waypoint_index = (self.current_waypoint_index + 1) % len(WAYPOINTS)
        
        # Trigger the next drive
        self.send_next_goal()

def main(args=None):
    rclpy.init(args=args)
    node = PatrolCommander()
    node.start_patrol()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
