import rclpy
from rclpy.node import Node

class TuningNode(Node):
    def __init__(self):
        super().__init__('dynamic_tuning_node')
        
        # 1. DECLARE the parameters (Creating the dials and setting default values)
        self.declare_parameter('robot_name', 'Suwi_Rover_V1')
        self.declare_parameter('max_speed', 5.0)
        
        # Create a timer that goes off every 1 second
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        # 2. GET the parameters (Read the current position of the dials)
        # Notice how we have to specify if it's a string_value or a double_value!
        current_name = self.get_parameter('robot_name').get_parameter_value().string_value
        current_speed = self.get_parameter('max_speed').get_parameter_value().double_value
        
        # Print the values to the terminal
        self.get_logger().info(f"Robot Name: {current_name} | Max Speed: {current_speed} mph")

def main(args=None):
    rclpy.init(args=args)
    node = TuningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

