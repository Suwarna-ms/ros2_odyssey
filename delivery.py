#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import sys

# ==============================================================
# MISSION COMMAND: The Map Dictionary
# Add or change these room names and coordinates for your maze!
# ==============================================================
ROOMS = {
    'home': (0.0, 0.0),
    'kitchen': (2.0, 2.0),
    'lab': (-2.0, 1.0),
    'garage': (1.5, -2.0)
}

class DeliveryRobot(Node):
    def __init__(self):
        super().__init__('delivery_robot')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_to_room(self, room_name):
        # Check if the room exists in our dictionary
        if room_name not in ROOMS:
            print(f"❌ Error: I don't know where '{room_name}' is!")
            return False

        x, y = ROOMS[room_name]
        print(f"✅ Route found! Calculating path to {room_name.upper()} at (X:{x}, Y:{y})...")
        
        self.action_client.wait_for_server()
        
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = float(x)
        goal_msg.pose.pose.position.y = float(y)
        goal_msg.pose.pose.orientation.w = 1.0 

        # Send goal and wait for it to be accepted
        future = self.action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            print("❌ Nav2 rejected the route!")
            return False

        print(f"🚚 Driving to {room_name.upper()}...")
        
        # Wait for the robot to arrive
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        
        print(f"🎉 ARRIVED AT {room_name.upper()}! Awaiting next command.\n")
        return True

def main(args=None):
    rclpy.init(args=args)
    robot = DeliveryRobot()

    print("\n=======================================")
    print("🤖 SMART DELIVERY SYSTEM INITIALIZED 🤖")
    print("=======================================")
    print("Available destinations: ", list(ROOMS.keys()))
    print("Type 'exit' to power down.")
    print("=======================================\n")

    while rclpy.ok():
        # Ask the human for a command
        destination = input("Where should I go? > ").strip().lower()
        
        if destination == 'exit':
            print("Powering down...")
            break
            
        # Send the robot!
        robot.send_to_room(destination)

    robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
