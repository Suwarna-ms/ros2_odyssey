import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetClient(Node):
    def __init__(self):
        super().__init__('reset_client')
        
        # Create a Client (A phone)
        self.client_ = self.create_client(Trigger, '/reset_sensor')
        
        # Wait until the server (robot) turns on
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Server not available, waiting...')
            
        self.send_request()

    def send_request(self):
        request = Trigger.Request() # Empty request
        
        self.get_logger().info('Calling the server to reset sensor...')
        self.future = self.client_.call_async(request)

def main(args=None):
    rclpy.init(args=args)
    node = ResetClient()
    
    # Wait for the response
    rclpy.spin_until_future_complete(node, node.future)
    
    # Print the answer we got back
    response = node.future.result()
    node.get_logger().info(f'Robot Answered: Success={response.success}, Message="{response.message}"')
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

