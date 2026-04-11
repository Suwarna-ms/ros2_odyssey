#import section
import rclpy 
from rclpy.node import Node
from std_msgs.msg import String

#class section
class HealthPublisher(Node):
     def __init__(self):
         super().__init__('health_publisher')
         
         #creating a radio transmitter (publisher)
         self.publisher_ = self.create_publisher(String, '/health_talker', 10)

         #creating a timer that goes off every 1.0 seconds 
         self.timer = self.create_timer(1.0, self.timer_callback)
     def timer_callback(self):
         msg = String()              # Create an empty message box
         msg.data="System Healthy"   # Put text inside the box
         self.publisher_.publish(msg)        # Send the box out into the world
         self.get_logger().info('publishing: "%s"' % msg.data)    # Print to terminal

def main(args=None):
    rclpy.init(args=args)           # Turn on ROS2
    node = HealthPublisher()      # Build our robot from the blueprint!
    rclpy.spin(node)                # "Spin" keeps the node running forever
 
    node.destroy_node()             # If we stop it, destroy it cleanly
    rclpy.shutdown()                # Turn off ROS2
    
if __name__ == '__main__':
   main()
       
    
